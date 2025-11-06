from fastapi import FastAPI
from pydantic import BaseModel
from textblob import TextBlob

app = FastAPI()

class Review(BaseModel):
    review: str

@app.post("/analyze")
def analyze_sentiment(data: Review):
    blob = TextBlob(data.review)
    score = blob.sentiment.polarity
    if score > 0.1:
        sentiment = "Positive"
    elif score < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return {"sentiment": sentiment, "score": score}
