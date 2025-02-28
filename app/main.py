from fastapi import FastAPI
from app.api.routes import contracts, notifications

app = FastAPI()

# Include routers separately
app.include_router(contracts.router, prefix="/contracts")  
app.include_router(notifications.router, prefix="/notifications") 

@app.get("/")
def read_root():
    return {"message": "Content Misuse Monitoring API is running!"}
