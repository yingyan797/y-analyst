def create_query_to_db_request_desc_prompt(schema, query, context):
    return f"""
You are a data analyst AI. Analyze the user's query directly or consult to database for more detail.

User Query: {query}

Context: {context}

Database Schema: {schema}

Task: Determine if you can answer the question directly or need database consultation.

If you can answer directly (general questions, explanations, definitions), set data_needed to false and provide the answer.
If you need database data, set data_needed to true and create database request forms. Specify which tables jointly contain the peices of information needed and describe how to obtain the data attributes.

Output Format:
{{
    "data_needed": true/false,
    "direct_answer": "Your direct answer if data_needed is false",
    "requests": [
        {{
            "attributes": ["column1", "column2"],
            "relevant_tables": ["table1", "table2"],
            "request_description": "Join, filter, aggregate operations needed"
        }}
    ]
}}

Provide only the JSON response.
"""

def create_db_request_to_sqlite_query_prompt(db_requests, schema):
    return f"""
You are a SQL expert. Convert database request forms into valid SQLite queries.

Database Schema: {schema}

Database Requests: {db_requests}

Task: For each database request form, generate a corresponding SQLite query that:
1. Selects the specified attributes
2. Uses the relevant tables
3. Implements the data processing operations described

Guidelines:
- Use proper SQLite syntax
- Include necessary JOINs based on table relationships
- Apply filters with WHERE clauses
- Use aggregation functions (MIN, MAX, AVG, COUNT, SUM) as needed
- Add GROUP BY and ORDER BY clauses when specified
- Use table aliases for readability
- Ensure column references are properly qualified

Output Format:
[
  {{
    "query": "SELECT column1, MAX(column2) FROM table1 t1 JOIN table2 t2 ON t1.id = t2.table1_id WHERE condition GROUP BY column1 ORDER BY column1",
    "description": "Brief explanation of what this query does"
  }}
]

Provide only the JSON array of SQLite queries.
"""

def create_answer_from_data_prompt(user_query, query_results, context):
    return f"""
You are a data analyst AI. Answer the user's question based on the data retrieved from database queries.

Original User Query: {user_query}

Context: {context}

Query Results: {query_results}

Task: Provide a comprehensive answer to the user's question using the data provided.

Guidelines:
- Directly address the user's question
- Use specific numbers and facts from the query results
- Provide insights and patterns found in the data
- Explain any calculations or comparisons made
- If multiple queries were executed, synthesize information across all results
- Use clear, non-technical language for the user
- Highlight key findings and trends
- If data is insufficient to fully answer the question, clearly state what's missing

Format your response as a clear, informative answer that helps the user understand their data.
"""