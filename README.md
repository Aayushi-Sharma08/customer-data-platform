# Overview
This project involves creating a FastAPI service with three main functions: ingesting transaction data, querying customers based on transaction amount ranges, and retrieving the top transacting customers by region. It uses a relational database for efficient data management and modular code for clear structure. Key features include duplicate handling, error management, and unit tests for robust functionality
# Project Objectives
The main objectives of this project are to create a set of APIs using FastAPI that perform the following tasks:

**1. Data Ingestion:** An API that accepts transaction data and inserts it into the database, while handling duplicate records appropriately.

**2. Transaction Range Query:**  An API that returns customers whose total transaction amounts fall within a specified range.

**3. Top Transacting Customers by specific:** An API that retrieves the top 5 transacting customers per pincode in a given state.
 # Project Prerequisites
**1. Paython:**  I used python 3.10.12 version.

**2. Database:** I used MySQL 8.0.39 database.

**3. Development Environment:** Setting up in PyCharm.

**4. Postman:** Use Postman to test APIs quickly and easily. 

**5. Git version:** I used git 2.34.1 version.

# Project setup Command
* **Access the Project Folder:**
```cd <path of the folder> ```Changes the current directory to the project folder.

* **Create a Virtual Environment:**

```python3 -m venv venv```
Creates a virtual environment named venv.

* **Activate the Virtual Environment:**

```source venv/bin/activate```
Activates the virtual environment.

* **Generate requirements.txt:**
```pip freeze > requirements.txt```
Creates a requirements.txt file with the currently installed packages.

* **Install Required Packages from requirements.txt**
```pip install -r requirements.txt```
Installs packages listed in the requirements.txt file.

* **Install Uvicorn** 
```sudo apt install uvicorn```
Installs the Uvicorn server globally using the package manager.

* **Install FastAPI**
```pip install fastapi```
Installs FastAPI framework in the active virtual environment.

* **Run the FastAPI Application with Uvicorn**
```uvicorn main:app --reload```
Starts the FastAPI application with auto-reload on changes.

* **Create __init__.py File:**
```touch app/__init__.py```
Creates an empty __init__.py file to mark the directory as a package.

* **Run a Python Module**
```python -m app.main```
Executes the main module within the app package.
  
# Project Code Overview
1. **main.py file :**
* Purpose: This file starts the app. It runs the FastAPI app on localhost:8000, so you can access it in your browser.

2. **modules.py file:**
* Purpose: Sets up the database and defines the data structure.
* Details:
   * Connects to a MySQL database using SQLAlchemy.
   * Defines a Transaction class to represent each transaction (like customer_id, amount, etc.).
    * Has Pydantic models (TransactionData for inputs, QueryResponse for outputs) to check data format.
3. **service.py file:** 

* Purpose: Contains all the main logic for handling transactions.
* Details:
   * ingest_transaction_data: Adds new transactions to the database (skips duplicates).
   * query_transaction_range_service: Gets transactions filtered by amount and date.
   * top_customers_service: Finds the top 5 customers per pincode within a specific state.
   * get_db: Manages database sessions.
4. **controller.py file :** 

* Purpose: Links everything to FastAPI, defining the routes (endpoints).
* Details:
   * /ingest-data: Endpoint to add new transactions.
   * /query-transaction-range: Filters transactions by amount and date.
   * /top-customers: Finds the top customers per pincode in a state.




# API Specifications
1. **Ingest Transaction Data:**
* Endpoint: /api/ingest-data
* Method: POST
* Objective: To accept and insert transaction data into the database.
* Sample Request:
   ``` 
      { 
        "customer_id": 101,
        "name": "amit",
        "transaction_amount": 1500.75,
        "mob_no": "9876543210",
        "transaction_datetime": "2024-09-24T15:30:00",
        "pincode": "110001",
        "state": "gujrat"
      }
  ```

 Response: Status indicating success or handling of duplicate record.

2. **Query Customer Transactions by Amount Range:**
* Endpoint: /api/query-transaction-range
* Method: POST
* Objective: Returns customers whose total transaction amounts are within a specified range.
* Sample Request:
     ```
         {
           "min_amount": 50000,
           "max_amount": 200000,
           "time_period": "2038-01-01T00:00:00"
         }
    ```
* Sample Response:
    ```
      [
          {
            "customer_id": 102,
            "name": "Jane Smith",
            "total_transaction_amount": 180000
          }
         {
            "customer_id": 104,
            "name": "Robert Johnson",
            "total_transaction_amount": 120000
         }
      ]

3. **Top Transacting Customers by Pincode in a State:** 
* Endpoint: /api/top-customers
* Method: POST
* Objective: Returns the top 5 transacting customers for each pincode in a specified state.
* Sample Request:
    ```
       {
          "state": "Punjab"
        }
  ```
* Sample Response:
```commandline{
  "pincode_141001": [
    {
      "customer_id": 201,
      "name": "Atharva Sharma",
      "total_transaction_amount": 75000
    }
    {
      "customer_id": 202,
      "name": "Simran Patel",
      "total_transaction_amount": 60000
    }
  ]
  "pincode_160001": [
    {
      "customer_id": 301,
      "name": "Lakshman Mehta",
      "total_transaction_amount": 90000
    }
    {
      "customer_id": 302,
      "name": "Ram Sharma",
      "total_transaction_amount": 85000
    }
  ]
}

```

# Unit Testing
* **Install pytest:**
```pip install pytest```
* **Install httpx:** ```pip install httpx```

* **Run Unit Tests:**
```pytest tests/```

* **test_main.py file :**  Confirms that the app runs and handles undefined endpoints correctly.

* **test_modules.py file :** Tests database models to ensure they initialize and store data as expected.
* **test_services.py file :** Checks core functions for data ingestion and transaction queries.
* **test_controller.py file :** Validates API endpoints for data ingestion, transaction range queries, and top customers.


# Assumptions
* **Duplicates:** Duplicate transactions are identified based on customer_id and transaction_datetime.
* **Time Zones:** The transaction times are assumed to be in UTC.
* **Data Retention:** Transaction data is retained indefinitely unless otherwise stated.














      
 # CDP-cutomer-data-platfrom-
