from fastapi import FastAPI
from api.v1.routers import default
from core.config import configs
import uvicorn
import os
import importlib

app = FastAPI(title=configs.APP_TITLE, version=configs.APP_VERSION)


def include_router(app):
    # 动态导入 api 目录下的所有路由模块
    api_dir = os.path.join(os.path.dirname(__file__), 'api', 'v1', 'routers')
    for filename in os.listdir(api_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f'api.v1.routers.{filename[:-3]}'
            module = importlib.import_module(module_name)
            app.include_router(module.router)

include_router(app)


if __name__ == "__main__":
    # prod
    uvicorn.run("main:app", host=configs.APP_HOST, port=int(configs.APP_PORT),reload=False)
    # dev
    # uvicorn.run(app, host=configs.APP_HOST, port=int(configs.APP_PORT),reload=True)
