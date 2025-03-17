import pytest
from datetime import datetime
from app.service import ingest_transaction_data, query_transaction_range_service
from app.modules import TransactionData, SessionLocal

@pytest.fixture(scope="function")
def db_session():
    db = SessionLocal()
    yield db
    db.close()

def test_ingest_transaction_data(db_session):
    data = TransactionData(
        customer_id=1,
        name="Alice",
        transaction_amount=150.0,
        mob_no="9876543210",
        transaction_datetime=datetime.now(),
        pincode="654321",
        state="TestState"
    )
    response = ingest_transaction_data(data)
    assert response == {"message": "Transaction data ingested successfully"}

def test_query_transaction_range_service(db_session):
    min_amount = 100.0
    max_amount = 200.0
    time_period = "2023-12-31T23:59:59"
    results = query_transaction_range_service(min_amount, max_amount, time_period)
    assert isinstance(results, list)
