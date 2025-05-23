import praw
import pandas as pd
from datetime import datetime, timedelta
import random

from date_converter import *
import time

def connect_api():

    try: 
        reddit = praw.Reddit(
                client_id='...',
                client_secret='...',
                user_agent='...'
            )
    
    # Confirm API Connection  
    except:
        print("API unable to connect...")

    return reddit    

def select_subreddit(reddit):
    try:
        subreddit = reddit.subreddit("stocks")

    except:
        print("Subreddit not found...")

    return subreddit

def time_period(date):
    try:
        start_date = get_monday_of_week(date)
        end_date = get_friday_of_week(start_date)
            
        # Convert to Unix timestamps
        start_timestamp = start_date.timestamp()
        end_timestamp = end_date.timestamp()
    
    except:
        print("Unable to confirm Date Range...")

    return start_timestamp, end_timestamp

def fetch_data(ticker, start_timestamp, end_timestamp, subreddit):

    posts = []
    i = 1
    j = 1
    for submission in subreddit.search(ticker, sort="new", limit=1000):
        
        if start_timestamp <= submission.created_utc <= end_timestamp:
            print(f"Post {i}")
            submission.comments.replace_more(limit=2000)
            matched_comments = [
                 comment.body for comment in submission.comments.list()    
             ]
            i += 1
            
            posts.append({
                "title": submission.title,
                "body": submission.selftext,
                "comments": matched_comments
            })
    
    # Create DataFrame
    df = pd.DataFrame(posts)

    return df

def combine_data(data):
    
    try: 
        comment_data = data[['comments']].explode('comments', ignore_index=True)
        comment_data.columns = ['data']
    except:
        print("No comments")

    titles = pd.DataFrame(data['title'].unique(), columns=['data'])

    bodies = pd.DataFrame({'data': data['body']})

    all_data = pd.concat([titles, bodies, comment_data])

    print("Data successfully combined!")
    
    return all_data

def fetch_reddit_data(ticker, date):
    
    start_time = time.time()
    reddit = connect_api()
    subreddit = select_subreddit(reddit)
    
    start_timestamp, end_timestamp = time_period(date)
    data = fetch_data(ticker, start_timestamp, end_timestamp, subreddit)
    combined_data = combine_data(data)

    data_length = len(combined_data)
    
    print(f"{len(combined_data)} rows of data")
    print(f"Time taken: {time.time() - start_time }")

    return combined_data, data_length