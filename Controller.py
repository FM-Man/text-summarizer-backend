import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from ServiceOld import get_summary as summary
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    text: str


@app.get("/")
def index():
    return {"name": "fahim morshed from mangum"}


@app.post("/summarize")
def summarize(m: Message):
    _, summarized_text = summary(m.text)
    return {"text": m.text, "summary": summarized_text}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
