from ib_insync import IB, Stock
import pandas as pd
import numpy as np
from datetime import timedelta, date, datetime

from date_converter import get_friday_of_week, get_monday_of_week


def fetch_historical_stock_data(ticker, timeframe, time_period):
    ib = IB()
    ib.connect('127.0.0.1', 4002, clientId=1)

    stock = Stock(symbol=ticker, exchange='SMART', currency='USD')

    bars = ib.reqHistoricalData(
        stock,
        endDateTime='',
        durationStr=time_period,
        barSizeSetting=timeframe,
        whatToShow='TRADES',
        useRTH=True  
    )

    ib.disconnect()

    data = pd.DataFrame([[bar.date, bar.open, bar.close, bar.high, bar.low] for bar in bars], columns=['Date', 'Open', 'Close', 'High', 'Low'])

    data['Date'] = pd.to_datetime(data['Date'])
    data['Date'] = data['Date'].dt.tz_localize(None)

    data = data.set_index('Date')

    return data


def fetch_selected_week_stock_data(date, ticker, timeframe, time_period):
    friday = get_friday_of_week(date)
    next_friday = friday + timedelta(weeks=1)

    historical_data = fetch_historical_stock_data(ticker, timeframe, time_period)

    # Helper to get data with fallback to previous day
    def get_data(target_date):
        try:
            return historical_data.loc[str(target_date)]
        except KeyError:
            try:
                return historical_data.loc[str(target_date - timedelta(days=1))]
            except KeyError:
                return None

    if next_friday > date.today():
        # Current week only
        data = get_data(friday)
        if data is None:
            return "No data available", "No data currently available"
            
        selected_week_open = data['Open']
        selected_week_close = data['Close']
        current_week_change = round(((selected_week_close - selected_week_open) / selected_week_open) * 100, 2)
        next_week_change = np.nan
    else:
        # Current and next week
        current_data = get_data(friday)
        next_data = get_data(next_friday)
        
        if current_data is None or next_data is None:
            return "No data available", "No data available"
            
        selected_week_open = current_data['Open']
        selected_week_close = current_data['Close']
        selected_next_week_open = next_data['Open']
        selected_next_week_close = next_data['Close']

        current_week_change = round(((selected_week_close - selected_week_open) / selected_week_open) * 100, 2)
        next_week_change = round(((selected_next_week_close - selected_next_week_open) / selected_next_week_open) * 100, 2)

    return current_week_change, next_week_change

if __name__ == "__main__":

    start_date = datetime(2025, 4, 7)
    data = fetch_selected_week_stock_data(start_date, "SPY", "1 W", "2 M")
    

    print(data)