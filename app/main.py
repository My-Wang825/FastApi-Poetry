from fastapi import FastAPI
from api.v1.routers import test
from core.config import configs
import uvicorn

app = FastAPI(title=configs.APP_TITLE, version=configs.APP_VERSION)


app.include_router(test.router)


if __name__ == "__main__":
    # prod
    uvicorn.run("main:app", host=configs.APP_HOST, port=int(configs.APP_PORT),reload=True)
    # dev
    # uvicorn.run(app, host=configs.APP_HOST, port=int(configs.APP_PORT),reload=True)
