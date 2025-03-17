# controller.py file
from fastapi import FastAPI, HTTPException, Depends
from typing import List, Dict
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.modules import QueryResponse, TransactionData
from app.service import ingest_transaction_data, query_transaction_range_service, top_customers_service, get_db

# create the FastAPI app instance
app = FastAPI()

#Model for request data
class QueryTransactionRangeRequest(BaseModel):
    min_amount: float
    max_amount: float
    time_period: str

# Ingest new transaction data
@app.post("/ingest-data")
def ingest_data(data: TransactionData):
    return ingest_transaction_data(data)

# Query transactions within a specified range
@app.post("/query-transaction-range", response_model=List[QueryResponse])
def query_transaction_range(request: QueryTransactionRangeRequest):
    return query_transaction_range_service(request.min_amount, request.max_amount, request.time_period)

# Define a model for top customers request
class TopCustomersRequest(BaseModel):
    state: str

# get Top 5 Transacting Customers per Pincode in a Given State
@app.post("/top-customers", response_model=Dict[str, List[QueryResponse]])
def top_customers(request: TopCustomersRequest, db: Session = Depends(get_db)):
    return top_customers_service(request.state, db)
