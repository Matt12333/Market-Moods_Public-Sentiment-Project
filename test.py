from datetime import datetime, timedelta
import time
import pandas as pd

from reddit_data import fetch_reddit_data
from stock_data import fetch_selected_week_stock_data
#from sentiment_model import fetch_sentiment
from bert_sentiment_model import fetch_sentiment



def select_week_of_data(selected_date, ticker, company, timeframe='1 W', timeperiod='1 Y'):

    reddit_ticker = f" {company} "
    reddit_data, data_length = fetch_reddit_data(reddit_ticker, selected_date)

    sentiment, negative_sentiment, positive_sentiment = fetch_sentiment(reddit_data)
    
    current_week_change, next_week_change = fetch_selected_week_stock_data(selected_date, ticker, timeframe, timeperiod)
    
    

    return sentiment, negative_sentiment, positive_sentiment, current_week_change, next_week_change, data_length

def fetch_all_data(start_date, end_date):

    current_date = start_date
    data = pd.DataFrame()

    while current_date < end_date:

        print("Waiting 5 seconds between calls")
        time.sleep(5)
        print(current_date)

        sentiment, negative_sentiment, positive_sentiment, current_week_change, next_week_change, data_length = select_week_of_data(current_date, ticker, company, timeframe='1 W', timeperiod='1 Y')

        df = pd.DataFrame({
            'Week Start': [current_date],
            'Sentiment': [sentiment],
            "Current Week's Change (%)": [current_week_change],
            "Next Week's Change (%)": [next_week_change],
            "Number of comments": [data_length],
            "Negative comments": [negative_sentiment],
            "Positive comments": [positive_sentiment]
        })

        data = pd.concat([data, df], ignore_index=True)

        data.to_csv(f"{ticker}_reddit_data.csv", index=False)

        current_date += timedelta(weeks=1)

    return data




if __name__ == "__main__":
    
    ticker = 'WMT'
    company = 'walmart'

    start_date = datetime(2025, 2, 3)
    end_date = datetime(2025, 5, 12)

    data = fetch_all_data(start_date, end_date)
    print(data)
