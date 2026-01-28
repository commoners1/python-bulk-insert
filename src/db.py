from sqlalchemy import create_engine
from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

def get_engine():
    url = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    return create_engine(url, pool_pre_ping=True)
