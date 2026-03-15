from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


MYSQL_USER = "root"
MYSQL_PASSWORD = "12345678"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "fastapi_db"

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"


#connection
engine = create_engine(DATABASE_URL)

#session
SessionLocal = sessionmaker(autocommit=False , autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


##BASE
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()





print(Base)
print(engine)
print(SessionLocal)
print(DATABASE_URL)