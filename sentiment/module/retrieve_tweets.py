from .utils import getLogFormat, send_message
import logging
import tweepy
import os
from django.http import HttpResponse

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

logger = logging.getLogger('sentiment')


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
        logger.info(getLogFormat(text="Authentication Successful!"))
        return api
    except:
        logger.error(getLogFormat(text="Error: Authentication Failed"))


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
    logger.info(getLogFormat(
        text="Application Limit Status: " + str(app_limit_status)))
    logger.info(getLogFormat(
        text="Search Limit Status: " + str(search_limit_status)))

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

            logger.info(getLogFormat(text="Retrieved tweets successfully!"))
            status = {"statusMsg": "Retrieved tweets successfully",
                      "step": "1", "total": "5"}
            await send_message(status)
            return raw_tweets
        except:
            logger.error(getLogFormat(text="Error: Can't able to Search"))
    else:
        logger.error(getLogFormat(
            text="Server is Busy! Please kindly search after 15 minutes"))
        return HttpResponse("Server is Busy! Please kindly search after 15 minutes")


# API = auth()
