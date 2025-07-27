from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlite_file_name = "todosApp.db"
sqlite_database_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_database_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
