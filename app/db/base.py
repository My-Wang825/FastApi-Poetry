from typing import Generator
from sqlmodel import SQLModel, Session, create_engine
from fastapi import Depends
from core.config import configs

# 创建数据库引擎
engine = create_engine(
    f"mysql+pymysql://{configs.DORIS_USER}:{configs.DORIS_PASSWORD}@{configs.DORIS_HOST}:{configs.DORIS_PORT}/{configs.DORIS_DATABASE}",
    pool_pre_ping=True,    # 连接池预检查
    pool_size=20,          # 连接池大小
    max_overflow=10        # 最大溢出连接数
)

# 获取数据库会话
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

get_db = get_session

# 初始化数据库
def init_db():
    SQLModel.metadata.create_all(engine)