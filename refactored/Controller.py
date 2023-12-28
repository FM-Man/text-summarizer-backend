from fastapi import FastAPI
from pydantic import BaseModel
from Service import get_summary as summary
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins, methods, and headers (you might want to restrict these in a production environment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your front-end URL(s) in production
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
