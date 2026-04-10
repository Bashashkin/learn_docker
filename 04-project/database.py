from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL")

# ждём пока поднимется postgres
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        conn = engine.connect()
        conn.close()
        break
    except Exception:
        print("DB not ready, retrying...")
        time.sleep(3)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
