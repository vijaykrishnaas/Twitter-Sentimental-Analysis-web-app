import tweepy
import os
from django.http import HttpResponse

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

from channels.layers import get_channel_layer

async def send_message(status):
    channel_layer = get_channel_layer()
    await channel_layer.group_send("status", {"type": "status.update", "text": status})

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


async def retrieve_tweets(keyword, tillDate):
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
            status = {"statusMsg": "Retrieved tweets successfully",
                      "step": "1", "total": "5"}
            await send_message(status)
            return raw_tweets
        except:
            print("Error: Can't able to Search")
    else:
        return HttpResponse("Server is Busy! Please kindly search after 15 minutes")


# API = auth()
