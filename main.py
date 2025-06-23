from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
import certifi

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hardcoded MongoDB connection (not recommended for production)
connection_string = (
    "mongodb+srv://yagneshreddysomavarapu:rPI7gE3pjVXWpca6@"
    "test.4injoid.mongodb.net/"
    "?retryWrites=true&w=majority"
    f"&tls=true&tlsCAFile={certifi.where()}"
)

try:
    client = MongoClient(connection_string)
    db = client["test"]
    collection = db["test"]
except Exception as e:
    print(f"Database connection error: {e}")

class EmailData(BaseModel):
    email: str
    password: str

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI on Render"}

@app.post("/email")
async def email_det(data: EmailData):
    try:
        if not data.email or not data.password:
            raise HTTPException(status_code=400, detail="Email and password are required")
            
        result = collection.insert_one({
            "email": data.email,
            "password": data.password  # Remember: Never store plain passwords in production
        })
        
        return {
            "status": "success",
            "message": "Data stored successfully",
            "inserted_id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))