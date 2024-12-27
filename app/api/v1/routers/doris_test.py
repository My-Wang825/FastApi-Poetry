from fastapi import APIRouter, Depends
from sqlmodel import Session
from db.base import get_db
from sqlalchemy import text
from datetime import datetime,timedelta
import pandas as pd
from io import StringIO
router = APIRouter()

@router.get("/doris_test")
def test_db(db: Session = Depends(get_db)):
    result = db.exec(text("SELECT 1 ")).first()
    return {"message": "Database connection successful"}

@router.get("/version")
def get_version(db: Session = Depends(get_db)):
    result = db.exec(text("SELECT VERSION()")).first()
    return {"doris_version": result[0]}


#智铝数据监控接口
@router.get("/get_zl")
async def get_zl_supervise(db: Session = Depends(get_db)):
    #获取昨天的日报数据 时间格式 20210901
    error_message = []

    # 日报数据
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    day_result = db.exec(text(f"SELECT * FROM ods_ckxt_l1zpa_aeht_dayrpt where RIQ = {yesterday}")).all()
    #将result转为df
    df = pd.DataFrame(day_result)
    #除去["chulshk","huanjshk","jiagshk","taimxshk"]，列本身无数据
    df = df.drop(columns=["chulshk","huanjshk","jiagshk","taimxshk"])
    cols_with_missing = [col for col in df.columns if df[col].isnull().any()]
    if cols_with_missing:
        error_message.append(f"日报中以下列存在数据缺失：{cols_with_missing},请检查")
    print(error_message)

