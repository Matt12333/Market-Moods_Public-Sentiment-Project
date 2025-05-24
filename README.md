<h1>Market Moods - A Public Sentiment Study</h1>    

<h3>Objective:</h3>
To determine if there is a correlation between public sentiment and the percentage change in a given market price.  
<br><br/>

[Presentation Script Link](https://docs.google.com/document/d/1wd2En0-qHanKVZDsTsk6BsxfsPdtx6z-PQqg6RfZOzA/edit?usp=sharing) - *The presentation script link, if you would like the narration of the presentation*

---
<h2>Project Overview</h2>

This is my Digital Futures Capstone Project. Having an interest in the financial markets, I had always heard that how you should never follow the crowd when trading/investing. This prompted myself to use Natural Language Processing to discover if this was accurate or not.   
The final outputs of the code files are the:
- Sentiment of the week
- % Change in Price for the Selected Week
- % Change in Price for the Following Week

The '% Change in Price for the Following Week' is included to see if there is a lag between the public sentiment and the change in market price.

<h3>Data Sources</h3>
I required two types of data for this project: Public Sentiment Data and Stock Market Data.  
  
- Public Sentiment Data: [Reddit API](https://www.reddit.com/dev/api/)   
- Stock Market Data: [Interactive Brokers API](https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/#api-introduction)

<h3>Script Purposes</h3>

- main.py: Contains two functions, to select a certain week of data and return the: Sentiment of that week, % Change in Price of Selected Week, % Change in Price of the Following Week or to loop through each week from a given start week and return the data to a csv file
- bert_sentiment_model.py: Determines the sentiment of each post and returns the overall sentiment of the market, based on if there are more bullish or bearish posts
- reddit_data.py: Fetches the reddit data of the specified market, within the specified time period
- stock_data.py: Fetches the stock data of the specific market, within the specified time period
- date_converter.py: Any date can be inputted into the main function, but to fetch the data from Monday to Friday of a given week, there are two functions the date is run through to return these dates and pass them to the   
Stock or Reddit APIs to return the data from that week
---

