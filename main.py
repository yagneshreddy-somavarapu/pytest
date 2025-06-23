from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pymongo
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mycli = pymongo.MongoClient("mongodb+srv://yagneshreddysomavarapu:rPI7gE3pjVXWpca6@test.4injoid.mongodb.net/")
mydb = mycli["test"]
mycol = mydb["test"]

class email_data(BaseModel):
   email: str
   password : str

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Fly.io"}
@app.post("/email")
def email_det(data:email_data):
    data = {
        "email":data.email,
        "password":data.password
      }
    mycol.insert_one(data)
    return "sucessfuly submited"