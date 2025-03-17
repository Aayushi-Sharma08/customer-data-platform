# modules.py file
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from pydantic import BaseModel
from datetime import datetime
from typing import List

# Set up the Database connection
DATABASE_URL = "mysql+pymysql://root:root@localhost/banking"  # connection string for MySQL
engine = create_engine(DATABASE_URL)   # creating Engine for the database
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
 # session management
Base = declarative_base()  # base class for database models

# This class represents "Transactions" table in the database
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    name = Column(String(100))
    transaction_amount = Column(Float)
    mob_no = Column(String(15))
    transaction_datetime = Column(DateTime)
    pincode = Column(String(10))
    state = Column(String(50))

# Create tables in database if it's not duplicate
Base.metadata.create_all(bind=engine)

#schema for incoming transaction data
class TransactionData(BaseModel):
    customer_id: int
    name: str
    transaction_amount: float
    mob_no: str
    transaction_datetime: datetime
    pincode: str
    state: str

#this is response model which is use to return data from queries
class QueryResponse(BaseModel):
    customer_id: int
    name: str
    total_transaction_amount: float

