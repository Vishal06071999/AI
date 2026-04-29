from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from config.config import Config


# 🔹 MySQL (phpMyAdmin) Connection URL
DATABASE_URL = Config.DATABASE_URL
# Agar password hai to:
# DATABASE_URL = "mysql+pymysql://root:yourpassword@localhost:3306/python"

# 🔹 Engine Create
engine = create_engine(DATABASE_URL, echo=True)

# 🔹 Session Create
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 🔹 Base Model
Base = declarative_base()


