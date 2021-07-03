import tweepy
import os
from django.http import HttpResponse
os.environ["CONSUMER_KEY"] = 'DxZRh6R8M7cyeIw3pT6sNQfRJ'
os.environ["CONSUMER_SECRET"] = 'GbHpwceOO3OC4IAqORM1ZXgyCAMTHX75y9ivccN45HT7GOvQAJ'
os.environ["ACCESS_TOKEN"] = '974107707870298113-nyTU6YEmoZILnr0b4oYcNH61Z8wOcOT'
os.environ["ACCESS_TOKEN_SECRET"] = 'Is0BEuZtH3XXxRepCBJSDQibfgAO1gcrFQn9cU4PARWlu'

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")


def auth():
    """
    A Authentication function which makes authentication with Twitter API using twitter application key and token credentials.

    Parameters
    ----------
    None

    Returns
    ------
    API
        a tweepy.api.API object which holds the authenticated reference object
    """
    try:
        # Create the authentication object
        authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # Set the access token and access token secret
        authenticate.set_access_token(access_token, access_token_secret)
        # Creating the API object while passing in auth information
        api = tweepy.API(authenticate, wait_on_rate_limit=True)
        print("Authentication Successful!")
        return api
    except:
        print("Error: Authentication Failed")


def isUnderLimit(api):
    """
    A Validator function which checks for available remaining API rate_limits.

    Parameters
    ----------
    api : tweepy.api.API object, required

    Returns
    ------
    limit
        a boolean which holds the status of API rate_limits
    """
    limit = False
    # Using Twitter API makes a request for check remaining rate_limit
    api_limit = api.rate_limit_status()
    app_limit_status = api_limit['resources']['application']['/application/rate_limit_status']['remaining']
    search_limit_status = api_limit['resources']['search']['/search/tweets']['remaining']
    print("Application Limit Status: ", app_limit_status)
    print("Search Limit Status: ", search_limit_status)

    if(app_limit_status >= 60 and search_limit_status >= 60):
        limit = True

    return limit


def retrieve_tweets(keyword, tillDate):
    """
    A Helper function which retrieves recent tweets matching the user's keyword.

    Parameters
    ----------
    keyword : str, required

    Returns
    ------
    tweepy.models.SearchResults object
            a object which contains retrieved matched tweets
    """
    API = auth()
    # checks whether the Twitter API is available along with enough rate_limits
    if API and isUnderLimit(API):
        try:
            if tillDate == "":
                # using Twitter API makes a keyword search
                raw_tweets = API.search(
                    keyword+" -filter:retweets", count=100, lang='en', tweet_mode="extended")
            else:
                # using Twitter API makes a keyword search
                raw_tweets = API.search(
                    keyword+" -filter:retweets", count=100, lang='en', until=tillDate, tweet_mode="extended")
            print("Retrieved tweets successfully!")
            return raw_tweets
        except:
            print("Error: Can't able to Search")
    else:
        return HttpResponse("Server is Busy! Please kindly search after 15 minutes")


API = auth()
