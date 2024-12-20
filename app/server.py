from fastapi import FastAPI
from core.config import configs
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
import os
import importlib
from task.schedule import scheduler


# 定时任务
async def lifespan(app: FastAPI):
    scheduler.start()
    print("定时任务已启动")
    yield
    scheduler.shutdown()
    print("定时任务已关闭")

# 动态扫描并注册路由
def register_routers(app: FastAPI):
    for root, dirs, files in os.walk("api"):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                module_path = os.path.join(root, file).replace(os.sep, ".")[:-3]
                module = importlib.import_module(module_path)
                if hasattr(module, "router"):
                    app.include_router(module.router)

app = FastAPI(title=configs.APP_TITLE, version=configs.APP_VERSION,lifespan=lifespan)
# 注册路由
register_routers(app)

if __name__ == "__main__":
    # prod
    uvicorn.run("server:app", host=configs.APP_HOST, port=int(configs.APP_PORT),reload=False)
    # dev
    # uvicorn.run(app, host=configs.APP_HOST, port=int(configs.APP_PORT),reload=True)
