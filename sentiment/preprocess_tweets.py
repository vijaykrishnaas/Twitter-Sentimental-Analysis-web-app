import re
import emoji
import pandas as pd
import nltk
from nltk.corpus import stopwords
# nltk.download('stopwords')


stop_words = set(stopwords.words("english"))

def normalize_tweets(tweet):
    """
    A Helper function which takes a tweet (unstructured data) and normalizes it to perform sentiment analysis.

    Parameters
    ----------
    tweet : str, required

    Returns
    ------
    tweet
        Cleaned tweet after normalization 
    """
    # Making the sentence case even
    tweet = tweet.lower()  
    # Removal of hastags/account
    tweet = re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", tweet) 
    # Removal of numbers
    tweet = re.sub(r"\d+", " ",tweet) 
    tweet = re.sub(r"rt+"," ",tweet)
    # Deal with emojis
    tweet = emoji.demojize(tweet) 
    # Removal of URL addresses
    tweet = re.sub(r"http\S+", " ",tweet)
    tweet = re.sub(r"https?:\/\/(www\.)?[-a-zA-Z0–9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)", " ",tweet)  
    # Removal of Punctuations
    tweet = re.sub("[\!\”\#\$\%\&\’\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]\^\_\`\{\|\}\~]", " ", tweet) 
    # Deal with Negative and shortWords
    tweet = re.sub(r"n\'t", " not", tweet)
    tweet = re.sub(r"\'re", " are", tweet)
    tweet = re.sub(r"\'s", " is", tweet)
    tweet = re.sub(r"\'d", " would", tweet)
    tweet = re.sub(r"\'ll", " will", tweet)
    tweet = re.sub(r"\'t", " not", tweet)
    tweet = re.sub(r"\'ve", " have", tweet)
    tweet = re.sub(r"\'m", " am", tweet)
    tweet = re.sub(r'\W*\b\w{1,2}\b', " ",tweet) 
    # Removal of Special characters
    tweet = re.sub("\W+"," ",tweet)
    # Removal of Whitespaces 
    tweet = tweet.strip()  
    return tweet

def convert_date(date):
  """
  A Helper function which takes the tweet created date and normalizes it to standard format.

  Parameters
  ----------
  date : str, required

  Returns
  ------
  date
      Formatted date after normalization 
  """
  return pd.Timestamp(date)


def get_hashtags(tweet):
  """
  A Helper function which takes a tweet and extracts Hashtags from it.

  Parameters
  ----------
  tweet : str, required

  Returns
  ------
  Hashtags List
      a list which contains the list of hashtags present in the tweet
  """
  return re.findall(r'\B#\w*[a-zA-Z]+\w*', tweet)
    

def preprocess_tweets(raw_tweets):
  """
  A Helper function which takes raw tweets and normalizes it to perform sentiment analysis.

  Parameters
  ----------
  tweepy.models.SearchResults object : json, required

  Returns
  ------
  df
      a dataFrame with processed data

  hashtags_count
      a pandas Series which contains hashtags with its respective count
  """
  # normalizing retrieve json object
  main_df = pd.json_normalize([i._json for i in raw_tweets])
  df = pd.DataFrame()
  hashtags = []
  df["id"] = main_df["id"]
  # normalizing tweet created date
  df["created_at"] = main_df["created_at"].apply(convert_date)
  df["raw_tweet"] = main_df["full_text"]
  # extracting hashtags from the tweets
  for tweet in df["raw_tweet"]:
    hashtags.extend(get_hashtags(tweet))
  hashtags_count = pd.Series(hashtags).value_counts()
  # normalizing retrieved tweets
  df["processed_tweet"] = df["raw_tweet"].apply(normalize_tweets)
  print("Preprocessing Tweets successful!")
  return df,hashtags_count