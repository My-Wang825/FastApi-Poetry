from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.config import configs
from fastapi.exceptions import HTTPException
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
import os
import importlib
from task.schedule import scheduler
from contextlib import asynccontextmanager
from pathlib import Path
from db.base import init_db

# 定时任务
async def lifespan(app: FastAPI):
    init_db()
    scheduler.start()
    print("定时任务已启动")
    yield
    scheduler.shutdown()
    print("定时任务已关闭")



def init_app(app: FastAPI) -> FastAPI:


    # 支持跨域
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def register_router(app: FastAPI):
    # from api.v1.routers import test
    # 注册路由
    # app.include_router(test.router)
        api_path = Path(__file__).parent / "api"
        for file in api_path.rglob("*.py"):
            if file.name == "__init__.py":
                continue
            module_name = f"api.{file.relative_to(api_path).with_suffix('')}".replace(os.sep, ".")
            module = importlib.import_module(module_name)
            if hasattr(module, "router"):
                app.include_router(module.router)

    register_router(app)



    def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    # Error
    def err_handler(request: Request, exc: Exception) -> JSONResponse:

        if isinstance(exc, HTTPException):
            return http_exception_handler(request, exc)

        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )
    
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, err_handler)

    return app




app = FastAPI(title=configs.APP_TITLE, version=configs.APP_VERSION,lifespan=lifespan)
init_app(app)

if __name__ == "__main__":
    # prod
    uvicorn.run("server:app", host=configs.APP_HOST, port=int(configs.APP_PORT),reload=False)
    # dev
    # uvicorn.run(app, host=configs.APP_HOST, port=int(configs.APP_PORT),reload=True)
