from fastapi import FastAPI
from pydantic import BaseModel
from Service import get_summary as summary
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


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
    return {"name": "fahim morshed"}


@app.post("/summarize")
def summarize(m: Message):
    _, summarized_text = summary(m.text)
    return {"text": m.text, "summary": summarized_text}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
