from dotenv import load_dotenv
from pathlib import Path
import os


dir_path = (Path(__file__)/".."/"..").resolve()
env_path = os.path.join(dir_path, '.env')
load_dotenv(dotenv_path=env_path)


class Config:

    APP_TITLE:str = os.getenv("APP_TITLE")
    APP_VERSION:str = os.getenv("APP_VERSION")
    APP_HOST:str = os.getenv("APP_HOST")
    APP_PORT:int = os.getenv("APP_PORT")
    NIFI_URL:str = os.getenv("NIFI_URL")
    NIFI_USERNAME:str = os.getenv("NIFI_USERNAME")
    NIFI_PASSWORD:str = os.getenv("NIFI_PASSWORD")
    DINGROBOT_ZHONGTAI:str = os.getenv("DINGROBOT_ZHONGTAI")

configs = Config()