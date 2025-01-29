from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Database_URL = "mysql+mysqlconnector://root:1234@localhost:3306/collection"

engine = create_engine(Database_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)