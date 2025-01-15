#--coding:utf-8--
import json
from typing import Union
import os
from fastapi import APIRouter, HTTPException
from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore
import pandas as pd
from vanna.chromadb import ChromaDB_VectorStore
from vanna.openai import OpenAI_Chat
from chromadb.utils import embedding_functions
from openai import OpenAI
from pydantic import BaseModel
from io import StringIO
import plotly.io as pio
from core.config import configs
from enum import Enum
from typing import Optional, Dict, Any

router = APIRouter()


class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, client=None, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self,client=client, config=config)

# Select the embedding model to use.
# List of model names can be found here https://www.sbert.net/docs/pretrained_models.html
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-large-zh-v1.5",
)
client = OpenAI(
    api_key=configs.OPENAI_API_KEY,
    base_url=configs.OPENAI_BASE_URL,
)
vn = MyVanna(
    client=client,
    config={
        "model": "qwen25:72b",
        "temperature": 0,
        "language": "chinese",
        "path": r"F:\MyFile\PythonProject\fastapi_demo\chromadb_data",
        "embedding_function": sentence_transformer_ef,
    }
)

#TODO: 之后修改成统一db接口去连数据库，执行sql
vn.connect_to_mysql(host=configs.DORIS_HOST, 
                    dbname=configs.DORIS_DATABASE, 
                    user=configs.DORIS_USER, 
                    password=configs.DORIS_PASSWORD, 
                    port=int(configs.DORIS_PORT))



@router.get("/")
def read_root():
    return {"Hello": "This is the Vanna API!"}
 
class DatabaseQuery(BaseModel):
    question: str | None = None
    query: str | None = None
    df_json: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "question": "显示销售数据",
                "query": "SELECT * FROM sales",
                "df_json": "{...}"
            }
        }

class QueryStep(str, Enum):
    GENERATE_SQL = "generate_sql"
    RUN_SQL = "run_sql"
    GENERATE_PLOT = "generate_plot"
    GENERATE_SUMMARY = "generate_summary"

@router.post("/query_database/")
async def query_database(
    request: DatabaseQuery,
    step: QueryStep
):
    try:
        result: Dict[str, Any] = {}
        
        if step == QueryStep.GENERATE_SQL:
            sql_query = vn.generate_sql(request.question)
            result["sql_query"] = sql_query
            
        elif step == QueryStep.RUN_SQL:
            sql_query = request.query
            sql_result = vn.run_sql(sql_query)
            
            
            result["markdown_table"] = sql_result.to_markdown()
            result["df_json"] = sql_result.to_json(orient="records")
            
        elif step == QueryStep.GENERATE_PLOT:
            sql_query = request.query
            df = pd.read_json(StringIO(request.df_json), orient='records')
            
            plotly_code = vn.generate_plotly_code(request.question, sql_query, df)
            figure = vn.get_plotly_figure(plotly_code, df, dark_mode=False)
            figure_json = pio.to_json(figure)
            result["figure_json"] = f"```plotly_json{figure_json}```"
            
        elif step == QueryStep.GENERATE_SUMMARY:
            df = pd.read_json(StringIO(request.df_json), orient='records')
            summary = vn.generate_summary(request.question, df)
            result["summary"] = summary
            
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

