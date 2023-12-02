from fastapi import FastAPI 
from pydantic import BaseModel
from Service import getSummary as old_summary
from exp_modules.expService import get_summary_ranked_sigma as new_summary_ranked
from exp_modules.expService import get_summary_unranked_sigma as new_summary_unranked


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
    summarizedText = new_summary_unranked(m.text,0.5)
    return {"text": summarizedText}


@app.post("/v3/summarize")
def summarize(m:Message):
    summarizedText = new_summary_ranked(m.text,0.5)
    return {"text": summarizedText}