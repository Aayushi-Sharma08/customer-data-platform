from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ingest_data_endpoint():
    payload = {
        "customer_id": 1,
        "name": "Alice",
        "transaction_amount": 100.0,
        "mob_no": "1234567890",
        "transaction_datetime": "2023-01-01T12:00:00",
        "pincode": "123456",
        "state": "TestState"
    }
    response = client.post("/ingest-data", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Transaction data ingested successfully"}

def test_query_transaction_range_endpoint():
    payload = {
        "min_amount": 50.0,
        "max_amount": 150.0,
        "time_period": "2023-12-31T23:59:59"
    }
    response = client.post("/query-transaction-range", json=payload)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_top_customers_endpoint():
    payload = {"state": "TestState"}
    response = client.post("/top-customers", json=payload)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
