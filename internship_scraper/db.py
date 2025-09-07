import os
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.engine import Engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

load_dotenv()
database_url = os.getenv('DATABASE_URL')


if not database_url:
    raise ValueError("DATABASE_URL environment variable not set")
engine: Engine = create_engine(database_url, pool_pre_ping=True)


Base = declarative_base()

def create_session() -> Session:
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def create_tables() -> None:
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


def empty_jobs_table() -> None:
    """
    Delete all records from the jobs table.
    """
    session = create_session()
    session.query(Job).delete()
    session.commit()
    session.close()


def reset_jobs_table() -> None:
    """
    Reset the jobs table by deleting all records and then creating the table again.
    """
    empty_jobs_table()
    create_tables()


if __name__ == "__main__":
    empty_jobs_table()
    create_tables()