#main.py file
import uvicorn
from app.controller import app # Import the FastAPI app defined in controller.py


# main entry point for application
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000) # running on localhost at port 8000
