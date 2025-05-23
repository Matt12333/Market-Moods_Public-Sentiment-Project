import pandas as pd
import numpy as np
import re # To remove certain characters from a text
import string # To get lists of certain characters

# Natural Language Libraries
import nltk # Natural Language Tokenizer
from nltk.corpus import opinion_lexicon # Positive and Negative Words
from nltk.corpus import stopwords # Stopwords
from nltk.tokenize import word_tokenize # Word Tokenizer

# Stemmers & Lemmatizers
from nltk.stem.lancaster import LancasterStemmer # Stemmer

# Modelling libraries
from sklearn.feature_extraction.text import CountVectorizer # Transform text into numbers
from sklearn.linear_model import LogisticRegression # Classify into positive and negative


# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('opinion_lexicon')

positive_words = opinion_lexicon.positive()
negative_words = opinion_lexicon.negative()

l_stemmer = LancasterStemmer() # Stemmer
stpwrd = nltk.corpus.stopwords.words('english') # Stopwords
stpwrd.extend(string.punctuation) # Add punctuation to stopwords list

## As the reviews are stemmed, the charged words need to be stemmed as well
positive_words = [l_stemmer.stem(word) for word in positive_words]
negative_words = [l_stemmer.stem(word) for word in negative_words]

def regex_clean(txt, regex):
    return " ".join(re.sub(regex, " ", txt).split())

def prep_data(review):

    if not isinstance(review, str):
        if pd.isna(review):
            return []
        review = str(review)

    review = review.lower() # Lowers all letters
    review = regex_clean(review, r'\s\d+\s') # Removes the numbers with a space on either side
    review = regex_clean(review, r'\$?\d*\.\d+\s')
    
    review = word_tokenize(review) 

    review = [word for word in review if word not in stpwrd] # Remove stopwords from review
    review = [l_stemmer.stem(word) for word in review] # Lemmantise the review
    review = [word for word in review if word not in stpwrd] # Remove the stopwords again, if any formed through lemmantising
    review = [word for word in review if len(word) > 2] # Remove any words short than three characters
    
    return review

def score_review(review): # Takes a review as an input
    
    review = prep_data(review) # Cleans the review and prepares it to be scored

    # Create a count for both positivity and negativity
    positive_count = sum([1 for i in review if i in positive_words]) # How many positive words are in the review
    negative_count = sum([1 for i in review if i in negative_words])   # How many negative words in the review
    
    try:
        positive_score = round((positive_count) / len(review), 2) # Percentage of positive words in the review
        neutral_score =  round((len(review) - negative_count - positive_count) / len(review),2) # Percentage of neutral words in the review
        negative_score = round((negative_count) / len(review), 2) # Percentage of positive words in the review
        
    except ZeroDivisionError: # Catches if the cleaned review is empty - 'len(review) == 0'
        positive_score = 0
        neutral_score = 0
        negative_score = 0

    return positive_score, neutral_score, negative_score

def make_pred(score_tup):

    # Weight the predicitons, as the positive reviews are overwhelming the negative reviews
    positive_score = score_tup[0] * 1 # Penalise the positive reviews
    neutral_score = score_tup[1]
    negative_score = score_tup[2] * 1.4 # Enhance the negative reviews

    # If the positive score outscores the negative score, it's a positive review
    if positive_score > negative_score:
        return 2
    else:
        return 1
    
def fetch_sentiment(data):
    
    data['score'] = data['data'].apply(score_review)
    data['pred'] = data['score'].apply(make_pred)

    negative_sentiment = data.pred.value_counts().iloc[0]
    positive_sentiment = data.pred.value_counts().iloc[1]

    print(f"Negative Comments: {negative_sentiment}")
    print(f"Positive Comments: {positive_sentiment}")
    
    if negative_sentiment > positive_sentiment:
        sentiment = "Bearish"
    else:
        sentiment = "Bullish"
        
    return sentiment,negative_sentiment, positive_sentiment