def create_query_to_db_request_desc_prompt(schema, query, context):
    return f"""
You are a data analyst AI. Analyze the user's query and database schema to create structured database request forms.

User Query: {query}

Context: {context}

Database Schema: {schema}

Task: Create a list of database request forms. Each form should specify:

1. **attributes**: List of column names needed from the database
2. **relevant_tables**: List of table names that contain the required data
3. **request_description**: Detailed description of data processing operations needed (joins, filters, aggregations like min/max/avg, grouping, sorting, etc.)

Output Format:
[
  {{
    "attributes": ["column1", "column2", "table2.column3"],
    "relevant_tables": ["table1", "table2"],
    "request_description": "Join table1 and table2 on common_id, filter by condition, calculate max(value), group by category"
  }}
]

Analyze the query step by step:
1. Identify the set of information relevant or helpful for answering what the user asks
2. Determine which tables contain each piece of information
3. Specify exact column names needed
4. Describe the data processing operations required

Provide only the JSON array of request forms.
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