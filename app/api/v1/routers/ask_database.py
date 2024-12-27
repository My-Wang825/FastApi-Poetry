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
        "path": "./chromadb_data",
        "embedding_function": sentence_transformer_ef,
    }
)

#TODO: 之后修改成统一db接口去连数据库，执行sql
vn.connect_to_mysql(host=configs.DORIS_HOST, dbname=configs.DORIS_DATABASE, user=configs.DORIS_USER, password=configs.DORIS_PASSWORD, port=configs.DORIS_PORT)



#TODO: 将四个阶段的类封装成一个类，然后将四个接口合并成一个接口去调用
class SQLQuery(BaseModel):
    question: str

class SQLResponse(BaseModel):
    query: str

class PlotlyNeed(BaseModel):
    question : str
    query: str
    df_json: str

class SummaryNeed(BaseModel):
    question: str
    df_json: str

class AskDatabase(BaseModel):
    question: str

@router.get("/")
def read_root():
    return {"Hello": "This is the Vanna API!"}

@router.post("/generate_sql/")
def generate_sql(request: SQLQuery):
    sql_query = vn.generate_sql(request.question)
    # 打印生成的 SQL 查询以进行调试
    return {"sql_query": sql_query}

@router.post("/run_sql/")
def run_sql(request: SQLResponse):
    try:
        sql_query_str = request.query
        sql_query = json.loads(sql_query_str)
        sql_query = sql_query['sql_query']
        sql_result = vn.run_sql(sql_query)
        # Convert scientific notation to normal numbers in the '订单数量' column
        if '订单数量' in sql_result.columns:
            sql_result['订单数量'] = sql_result['订单数量'].apply(lambda x: '{:.0f}'.format(x))
        print(sql_result)
        print(sql_result.info())
        df_json = sql_result.to_json(orient="records")
        df_markdwon = sql_result.to_markdown()
        return {"markdown_table": df_markdwon,"df_json":df_json}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/generate_plotly_figure/")
def generate_plotly_code(request: PlotlyNeed):
    try:
        sql_question = request.question
        sql_query = json.loads(request.query)
        print(sql_query)
        query = sql_query['sql_query']
        df_str = request.df_json
        print(df_str)
        df = pd.read_json(StringIO(df_str),orient='records')
        print(df)
        print(df.info())
        plotly_code = vn.generate_plotly_code(sql_question, query, df)
        print('generate code done')
        figure = vn.get_plotly_figure(plotly_code,df,dark_mode=False)
        print('generate figure done')
        figure_json = pio.to_json(figure)
        figure_json = f"```plotly_json{figure_json}```"
        return {"figure_json": figure_json}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/generate_summary/")
async def generate_summary(request: SummaryNeed):
    question = request.question
    df_str = request.df_json
    df = pd.read_json(StringIO(df_str),orient='records')
    summary = vn.generate_summary(question,df)
    return {"summary":summary}
    

#将上面的三个函数合并成一个函数，ask_database
@router.post("/ask_database/")
async def ask_database(request: AskDatabase):
    try:
        sql_question = request.question
        sql_query = vn.generate_sql(sql_question)
        sql_result = vn.run_sql(sql_query)
        # Convert scientific notation to normal numbers in the '订单数量' column
        if '订单数量' in sql_result.columns:
            sql_result['订单数量'] = sql_result['订单数量'].apply(lambda x: '{:.0f}'.format(x))
        print(sql_result)
        print(sql_result.info())
        df_markdwon = sql_result.to_markdown()
        plotly_code = vn.generate_plotly_code(sql_question, sql_query, sql_result)
        print('generate code done')
        figure = vn.get_plotly_figure(plotly_code,sql_result,dark_mode=False)
        print('generate figure done')
        summary = vn.generate_summary(sql_question,sql_result)
        figure_json = pio.to_json(figure)
        figure_json = f"```plotly_json{figure_json}```"
        print(figure_json)
        return {"markdown_table": df_markdwon, "figure_json": figure_json, "summary": summary, "sql_query": sql_query}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    