from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
import certifi

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Corrected MongoDB connection with proper certifi integration
connection_string = (
    "mongodb+srv://yagneshreddysomavarapu:rPI7gE3pjVXWpca6@"
    "test.4injoid.mongodb.net/"
    "?retryWrites=true&w=majority"
    "&tls=true"
    f"&tlsCAFile={certifi.where()}"  # Properly formatted certifi integration
)

mycli = MongoClient(connection_string)
mydb = mycli["test"]  # Make sure this matches your actual database name
mycol = mydb["test"]  # Make sure this matches your actual collection name

class EmailData(BaseModel):  # Changed to PascalCase for class names
    email: str
    password: str  # Warning: Storing plain passwords is unsafe

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Fly.io"}

@app.post("/email")
def email_det(data: EmailData):  # Changed to match class name
    try:
        result = mycol.insert_one({
            "email": data.email,
            "password": data.password  # In production, NEVER store plain passwords
        })
        return {"status": "success", "inserted_id": str(result.inserted_id)}
    except Exception as e:
        return {"status": "error", "message": str(e)}