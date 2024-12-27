import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
database_url = os.getenv('DATABASE_URL')

if not database_url:
    raise ValueError("DATABASE_URL environment variable not set")
engine = create_engine(database_url, pool_pre_ping=True)

Base = declarative_base()

def create_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def create_tables():
    Base.metadata.create_all(engine)


class Job(Base):
    __tablename__ = 'jobs'
    title = Column(String, nullable=False)
    link = Column(String, primary_key=True)
    location = Column(String, nullable=False)
    company = Column(String, nullable=False)
    description = Column(Text)
    employment_type = Column(String)
    seniority_level = Column(String)
    job_function = Column(String)
    industries = Column(String)


if __name__ == "__main__":
    create_tables()