from data_pre_processing import data_preprocessing
from twitter_tweet_Extraction import getTweets
from sentiment_analysis import sentiment_analysis
from getRealStock import getRealStock
import pandas as pd

def getSentiment(stock):
    data = getTweets(stock)
    cleaned_data = data_preprocessing(data, stock)
    cleaned_data['date'] = pd.to_datetime(cleaned_data['created_at']).dt.normalize()
    sentimented_data = sentiment_analysis(cleaned_data,stock)
    result_data = getRealStock(sentimented_data,stock)
    return result_data