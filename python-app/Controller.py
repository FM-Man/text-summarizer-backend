from fastapi import FastAPI 
from pydantic import BaseModel
from Service import getSummary

app = FastAPI()

class Message(BaseModel):
    text : str

@app.get("/")
def index():
    return {"name":"fahim morshed"}

@app.post("/summarize")
def summarize(m:Message):
    summarizedText = getSummary(m.text)
    return {"text": summarizedText}