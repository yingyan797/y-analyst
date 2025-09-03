import sqlite3, json, dotenv, os
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langchain.chat_models.base import init_chat_model

import prompts as pr

class DatabaseSchemaAnalyzer:
    def __init__(self, db_path):
        self.db_path = db_path
    
    def create_schema_overview(self):
        """Create an overview of database schema including all table names and columns"""
        schema_overview = {}
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get all table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                # Get column information for each table
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                
                schema_overview[table_name] = [
                    {
                        'name': col[1],
                        'type': col[2],
                        'not_null': bool(col[3]),
                        'primary_key': bool(col[5])
                    }
                    for col in columns
                ]
        
        return schema_overview
    
    def get_raw_data(self, queries):
        with sqlite3.connect(self.db_path) as conn:
            for query_info in queries:
                cursor = conn.cursor()
                cursor.execute(query_info["query"])
                data = cursor.fetchall()
                yield (query_info, data)

class AIModel:
    def __init__(self, is_simulation) -> None:
        self.is_simulation = is_simulation
        os.environ["GOOGLE_API_KEY"] = dotenv.get_key(".env","gemini_api")
        self.model = init_chat_model(
            model="gemini-2.0-flash-lite",
            model_provider="google_genai"
        )

    def invoke(self, prompt):
        if self.is_simulation:
            if "Implements the data processing operations described" in prompt:
                return '''
                [
                    {"query": "select product_id, review_text from reviews", "description": "simulate"},
                    {"query": "select name, city from suppliers", "description": "simulate"}
                ]'''
            return ''' {"info": "simulate response"}'''
        response = self.model.invoke(prompt).content
        return response
            
class DataAnalysisAgent:
    def __init__(self, db_path, llm):
        self.db_path = db_path
        self.llm = llm
        self.schema_analyzer = DatabaseSchemaAnalyzer(db_path)
        self.schema = self.schema_analyzer.create_schema_overview()
        self.graph = self._build_graph()
    
    def _parse_json_from_response(self, response_text):
        """Extract JSON from AI response using bracket matching"""
        text = response_text.strip()
        
        # Find first opening bracket
        start_idx = -1
        for i, char in enumerate(text):
            if char in '[{':
                start_idx = i
                break
        
        if start_idx == -1:
            return None
        
        # Match brackets to find end
        bracket_count = 0
        start_bracket = text[start_idx]
        end_bracket = ']' if start_bracket == '[' else '}'
        
        for i in range(start_idx, len(text)):
            if text[i] == start_bracket:
                bracket_count += 1
            elif text[i] == end_bracket:
                bracket_count -= 1
                if bracket_count == 0:
                    json_str = text[start_idx:i+1]
                    try:
                        return json.loads(json_str)
                    except:
                        return None
        
        return None
    
    def _build_graph(self):
        workflow = StateGraph(Dict[str, Any])
        
        workflow.add_node("analyze_query", self._analyze_query)
        workflow.add_node("generate_sql", self._generate_sql)
        workflow.add_node("execute_queries", self._execute_queries)
        workflow.add_node("generate_answer", self._generate_answer)
        workflow.add_node("pause", self._pause)
        
        workflow.set_entry_point("analyze_query")
        workflow.add_conditional_edges(
            "analyze_query", 
            lambda state: bool(state["data_needed"]) and not(state["db_requests"]),                         
            {True: "generate_sql", False: "pause"}
        )
        workflow.add_edge("generate_sql", "execute_queries")
        workflow.add_edge("execute_queries", "generate_answer")
        workflow.add_edge("generate_answer", "pause")
        
        return workflow.compile()
    
    def _pause(self, state):
        return state
    
    def _analyze_query(self, state: Dict[str, Any]) -> Dict[str, Any]:
        prompt = pr.create_query_to_db_request_desc_prompt(
            self.schema, state["user_query"], state.get("context", "")
        )
        response = self.llm.invoke(prompt)
        answer_construct = self._parse_json_from_response(response)
        return {**state, 
                "data_needed": answer_construct["data_needed"], 
                "final_answer": answer_construct["direct_answer"], 
                "db_requests": answer_construct["requests"]
            }
    
    def _generate_sql(self, state: Dict[str, Any]) -> Dict[str, Any]:
        prompt = pr.create_db_request_to_sqlite_query_prompt(
            state["db_requests"], self.schema
        )
        response = self.llm.invoke(prompt)
        print(response)
        sql_queries = self._parse_json_from_response(response) or []
        return {**state, "sql_queries": sql_queries}
    
    def _execute_queries(self, state: Dict[str, Any]) -> Dict[str, Any]:
        results = []
        for query_info, data in self.schema_analyzer.get_raw_data(state["sql_queries"]):
            results.append({
                "query": query_info["query"],
                "description": query_info["description"],
                "results": data
            })
        return {**state, "query_results": results}
    
    def _generate_answer(self, state: Dict[str, Any]) -> Dict[str, Any]:
        prompt = pr.create_answer_from_data_prompt(
            state["user_query"], state["query_results"], state.get("context", "")
        )
        response = self.llm.invoke(prompt)
        return {**state, "final_answer": response}
    
    def answer_question(self, user_query: str, context: str = "") -> str:
        initial_state = {
            "user_query": user_query,
            "context": context
        }
        result = self.graph.invoke(initial_state)
        return result["final_answer"]
    
if __name__ == "__main__":
    agent = DataAnalysisAgent("data_engineering/exp.sqlite", AIModel(False))
    print(agent.answer_question("How to write a resume for software engineer", ""))
    # print(agent.answer_question("Which suppliers doesn't receive any review score of 4", "context"))
    # with open("debug.json", "r") as f:
    #     response = f.read()
    
    # print(agent._parse_json_from_response(response)[0])
