from fastapi import FastAPI
from api.app.routers import default
from api.core.config import configs
import uvicorn




def include_router(app):
    app.include_router(default.router)

def start_application():
    app = FastAPI(title=configs.APP_TITLE,version=configs.APP_VERSION)
    include_router(app)
    return app

#docker
app = start_application()

#local
# if __name__ == "__main__":
#     app = start_application()
#     uvicorn.run(app,host=configs.APP_HOST,port=int(configs.APP_PORT)) 