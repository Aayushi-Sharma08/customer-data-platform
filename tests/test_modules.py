import pytest
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.modules import Base, Transaction

# Test database setup
@pytest.fixture(scope="module")
def test_engine():
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(test_engine)
    yield test_engine
    Base.metadata.drop_all(test_engine)

@pytest.fixture(scope="function")
def session(test_engine):
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()

def test_transaction_model(session):
    transaction = Transaction(
        customer_id=1,
        name="John Doe",
        transaction_amount=100.0,
        mob_no="1234567890",
        transaction_datetime=datetime.strptime("2023-01-01T12:00:00", "%Y-%m-%dT%H:%M:%S"),
        pincode="123456",
        state="TestState"
    )
    session.add(transaction)
    session.commit()
    retrieved = session.query(Transaction).filter_by(customer_id=1).first()
    assert retrieved.name == "John Doe"
    assert retrieved.transaction_amount == 100.0
