import pandas as pd

from transformers import pipeline

sentiment_pipeline = pipeline(
    "sentiment-analysis", # Task
    model="distilbert-base-uncased-finetuned-sst-2-english" # Model
)

def score_data(review):
    sentiment = sentiment_pipeline(review[:512])[0]['label']
    
    if sentiment == 'NEGATIVE':
        return 1
    else:
        return 2
    
def determine_bias(data):
    negative_sentiment = data['score'].value_counts().iloc[0]
    positive_sentiment = data['score'].value_counts().iloc[1]

    print(negative_sentiment)
    print(positive_sentiment)
    
    if negative_sentiment > positive_sentiment:
        sentiment = "Bearish"
    else:
        sentiment = "Bullish"
        
    return sentiment, negative_sentiment, positive_sentiment

def fetch_sentiment(data):
    data['data'] = data['data'].astype(str)

    data['score'] = data['data'].apply(score_data)

    sentiment, negative_sentiment, positive_sentiment = determine_bias(data)

    return sentiment, negative_sentiment, positive_sentiment