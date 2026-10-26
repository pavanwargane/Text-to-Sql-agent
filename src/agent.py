import os

from google import genai
from dotenv import load_dotenv

from src.database import get_schema

load_dotenv()

client= genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model= os.getenv("GEMINI_MODEL")

def generate_sql(question):
    prompt=f"""

Convert the user's question into one SQLite SELECT query.

    1.Use only the table and columns shown below.
    2.Return only SQL, without Markdown.
    3.Never generate commands that change data.
    4.never guess the data 
    5.dont execute INSERT,UPDATE,DELETE,ATTACH queries.
    6.use only SELECT statement
    7.if the data not available say so.
DATABASE:
{get_schema()}

QUESTION:
{question}
"""
    ## ask ai to generate query
    response=client.models.generate_content(
        model=model,
        contents=prompt,
    )

    ## return the generated sql
    if not response.text:
        raise ValueError("GEMINI return no sql")
    return response.text.strip().removeprefix("```sql").removesuffix("```").strip()



