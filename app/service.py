# service.py file
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime
from app.modules import Transaction, SessionLocal, TransactionData, QueryResponse
import logging

logging.basicConfig(level=logging.INFO) # Set up logging for debugging in tracking
logger = logging.getLogger(__name__)

#This function handel new transaction to the database
def ingest_transaction_data(data: TransactionData):
    session = SessionLocal()  # Start a new session
    try:
        # Check for duplicates based on customer_id and datetime
        duplicate = session.query(Transaction).filter(
            Transaction.customer_id == data.customer_id,
            Transaction.transaction_datetime == data.transaction_datetime
        ).first()
        if duplicate:
            return {"message": "Duplicate transaction found, not inserting."} # skip if it is duplicate entry

#Create new Transaction record and add it to the session
        transaction = Transaction(**data.dict())
        session.add(transaction)
        session.commit() #Save changes to the database
        return {"message": "Transaction data ingested successfully"}
    finally:
        session.close() #close the session to free resources

# This function fetch transactions based on amount and date
def query_transaction_range_service(min_amount: float, max_amount: float, time_period: str):
    session = SessionLocal()
    try:
        time_period_dt = datetime.fromisoformat(time_period)  # converting the time_period from string to datetime
        results = (
            session.query(Transaction.customer_id, Transaction.name,
                          func.sum(Transaction.transaction_amount).label("total_transaction_amount"))
            .filter(
                Transaction.transaction_amount.between(min_amount, max_amount),
                Transaction.transaction_datetime <= time_period_dt
            )
            .group_by(Transaction.customer_id, Transaction.name)
            .all()
        )
        #Raise error if no transaction found
        if not results:
            raise HTTPException(status_code=404, detail="No transactions found within the given range")

        # return the results as a list
        return [QueryResponse(customer_id=row[0], name=row[1], total_transaction_amount=row[2]) for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

#This function returns the top customers for a particular state
def top_customers_service(state: str, db: Session):
    try:
        # query for getting top customers by transaction amount per pincode
        results = (
            db.query(
                Transaction.pincode,
                Transaction.customer_id,
                func.max(Transaction.name).label("name"),  # Aggregate function for name
                func.sum(Transaction.transaction_amount).label("total_transaction_amount")
            )
            .filter(Transaction.state == state)
            .group_by(Transaction.pincode, Transaction.customer_id)
            .order_by(Transaction.pincode, func.sum(Transaction.transaction_amount).desc())
            .all()
        )
        #Raise an error if no transaction found
        if not results:
            raise HTTPException(status_code=404, detail="No transactions found for the given state.")
        #Orgnizing the results by pincode
        response = {}
        current_pincode = None
        top_customers = []

        for row in results:
            pincode = f"pincode_{row[0]}"
            if pincode != current_pincode:
                if current_pincode is not None:
                    response[current_pincode] = top_customers[:5] # Keep only top 5
                current_pincode = pincode
                top_customers = []
            top_customers.append(QueryResponse(customer_id=row[1], name=row[2], total_transaction_amount=row[3]))

        if current_pincode is not None:
            response[current_pincode] = top_customers[:5]

        return response
    except Exception as e:
        logger.error(f"Error occurred while fetching top customers: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

#dependency to get a database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db # allowing FastAPI to manage the session
    finally:
        db.close() # Ensure the session is closed after use