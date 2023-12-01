from fastapi import FastAPI 
from pydantic import BaseModel
from Service import getSummary as old_summary
from exp_modules.expService import getSummary as new_summary

app = FastAPI()

class Message(BaseModel):
    text : str

@app.get("/")
def index():
    return {"name":"fahim morshed"}

@app.post("/v1/summarize")
def summarize(m:Message):
    summarizedText = old_summary(m.text)
    return {"text": summarizedText}


@app.post("/v2/summarize")
def summarize(m:Message):
    summarizedText = new_summary(m.text)
    return {"text": summarizedText}