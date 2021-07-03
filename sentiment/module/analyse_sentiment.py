import textblob
import os
import pandas as pd
from joblib import load

# Get the current working directory
cwd = os.getcwd()

# Loads the ML model
clf = load(cwd + "\\sentiment\\MLModel\\SVMModel.joblib")
print("ML Model Loaded!")


def predict(tweet):
    """
    The Prediction function which takes a tweet and makes prediction using the ML model.

    Parameters
    ----------
    tweet : str, required

    Returns
    ------
    Prediction
        a pandas Series which contains the predicted sentiment type and its respective polarity value
    """
    # makes prediction using the ML Classifier
    predicted = clf.predict([tweet])
    if predicted == -1:
        return pd.Series(["Negative", -1])
    elif predicted == 1:
        return pd.Series(["Positive", 1])
    else:
        return pd.Series(["Neutral", 0])


def polarize(tweet):
    """
    A Helper function which takes a tweet and finds subjectivity & polarity of it.

    Parameters
    ----------
    tweet : str, required

    Returns
    ------
    Subjectivity and Polarity
        a pandas Series which contains subjectivity and polarity of the tweet
    """
    blob = textblob.TextBlob(tweet)
    return pd.Series([blob.sentiment.subjectivity, blob.sentiment.polarity])


def analyse_sentiment(df):
    """
    A Helper function which takes a dataFrame containing processed data and performs sentimental analysis.

    Parameters
    ----------
    df : DataFrame, required

    Returns
    ------
    df
        a DataFrame with predicted results

    List 
        a list of python dictionaries for template view purpose
    """
    df[["subjectivity", "polarity"]] = df["processed_tweet"].apply(polarize)
    df[["sentiment", "Analysis"]] = df["processed_tweet"].apply(predict)
    print("Tweet Analysis Completed!")
    return (df, df.to_dict('records'))
