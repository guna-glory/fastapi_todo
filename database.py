from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()   # ✅ CALL THE FUNCTION

DATABASE_URL = os.getenv("DATABASE_URL")

print(DATABASE_URL)  # should now print real URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
