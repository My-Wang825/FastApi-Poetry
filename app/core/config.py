from dotenv import load_dotenv
from pathlib import Path
import os


dir_path = (Path(__file__)/".."/"..").resolve()
env_path = os.path.join(dir_path, '.env')
load_dotenv(dotenv_path=env_path)

# Load the .env file
class Config():

    APP_TITLE:str = os.getenv("APP_TITLE")
    APP_VERSION:str = os.getenv("APP_VERSION")
    APP_HOST:str = os.getenv("APP_HOST")
    APP_PORT:int = os.getenv("APP_PORT")
    NIFI_URL:str = os.getenv("NIFI_URL")
    NIFI_USERNAME:str = os.getenv("NIFI_USERNAME")
    NIFI_PASSWORD:str = os.getenv("NIFI_PASSWORD")
    DINGROBOT_ZHONGTAI:str = os.getenv("DINGROBOT_ZHONGTAI")
    OPENAI_API_KEY:str = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL:str = os.getenv("OPENAI_BASE_URL")

    DORIS_HOST:str = os.getenv("DORIS_HOST")
    DORIS_PORT:str = os.getenv("DORIS_PORT")
    DORIS_USER:str = os.getenv("DORIS_USER")
    DORIS_PASSWORD:str = os.getenv("DORIS_PASSWORD")
    DORIS_DATABASE:str = os.getenv("DORIS_DATABASE")
    DB_ECHO:bool = os.getenv("DB_ECHO")

configs = Config()