from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# # FOR SQLITE DB CONNECTION

# sqlite_file_name = "todosApp.db"
# SQLALCHEMY_DATABASE_URL = f"sqlite:///{sqlite_file_name}"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) 

# # FOR PostgreSQL DB CONNECTION               
# # SQLALCHEMY_DATABASE_URL = "postgresql://[username]://[password]@localhost/[database_name]"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres://postgres@localhost/PythonTodoApplication"


# # FOR MYSQL DB CONNECTION
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:chalie123@127.0.0.1:3306/PythonTodoApplication"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
