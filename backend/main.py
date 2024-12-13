from fastapi import FastAPI
from api.app.routers import default
from api.core.config import configs
import uvicorn
import os
import importlib
import threading
import task.task_test

def start_task():
    task.task_test.main()

def include_router(app):
    # 动态导入 api 目录下的所有路由模块
    api_dir = os.path.join(os.path.dirname(__file__), 'api', 'app', 'routers')
    for filename in os.listdir(api_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f'api.app.routers.{filename[:-3]}'
            module = importlib.import_module(module_name)
            app.include_router(module.router)

def start_application():
    app = FastAPI(title=configs.APP_TITLE,version=configs.APP_VERSION)
    include_router(app)
    return app

#docker
app = start_application()

# local
# if __name__ == "__main__":
    # task_thread = threading.Thread(target=start_task)
    # task_thread.start()
    # print('task_thread started')
    # app = start_application()
    # uvicorn.run(app,host=configs.APP_HOST,port=int(configs.APP_PORT))
    # print('app started')