from core.config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

## Create the engine

engine = create_engine(config.database_url, echo=True)

#creating session
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Function to get the database in routes
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
        
