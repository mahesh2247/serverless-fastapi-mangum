# main.py

from fastapi import FastAPI
from mangum import Mangum
from routes import item_routes
from database import create_db_and_tables  # Importing the function

app = FastAPI()

# Create database tables if needed (call it only once)
create_db_and_tables()

# Include the item routes
app.include_router(item_routes.router, prefix="/items", tags=["Items"])

# Create a Mangum handler
handler = Mangum(app)