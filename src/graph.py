from typing import TypedDict
from langgraph.graph import StateGraph ,START,END

from src.agent import generate_sql
from src.database import run_sql

# State stores information while the workflow runs.

class AgentState(TypedDict):
    question:str
    sql:str
    results:list

##converting users question into sql

def make_sql(state: AgentState):
    sql = generate_sql(state["question"])
    return {"sql": sql}


# Step 2: Check the query and run it.
def execute_sql(state: AgentState):
    sql = state["sql"].strip()


    # SQLite's read-only connection provides another safeguard.
    results = run_sql(sql)
    return {"results": results}
        
## workflow
workflow=StateGraph(AgentState)

workflow.add_node("make_sql",make_sql)
workflow.add_node("execute_sql",execute_sql)

##Run SQL generation first, then execute the query

workflow.add_edge(START,"make_sql")
workflow.add_edge("make_sql","execute_sql")
workflow.add_edge("execute_sql",END)

##complie
app=workflow.compile()
