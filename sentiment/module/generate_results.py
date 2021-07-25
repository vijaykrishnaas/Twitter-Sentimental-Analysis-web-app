from .utils import getLogFormat, send_message
import pandas as pd
import os
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import plotly
import plotly.graph_objects as go
import plotly.express as px
import asyncio

import logging
logger = logging.getLogger('sentiment')

# Get the current working directory
cwd = os.getcwd()


async def generate(df, hashtags_count):
    """
    A Helper function which takes the analysed data and hashtags count data to generate interactive visualizations.

    Parameters
    ----------
    df : DataFrame, required

    hashtags_count : Pandas Series, required

    Returns
    ------
    Visualizations
        a set of interactive charts generated based on the analysed data and hashtags count
    """
    # Main Function
    html_pie = generate_pie_chart(df)
    logger.info(getLogFormat(text="Sentiment Chart Generated!"))

    html_timebar = generate_timebar(df)
    logger.info(getLogFormat(text="TimeLine Chart Generated!"))

    html_hashtag_count = generate_hashtag_count_chart(hashtags_count)
    logger.info(getLogFormat(text="Hashtag count Chart Generated!"))

    html_subject = generate_subject_chart(df)
    logger.info(getLogFormat(text="Subjectivity-Polarity Chart Generated!"))

    status = {"statusMsg": "Chart Generation Completed",
              "step": "4", "total": "5"}
    await send_message(status)

    word_clouds = word_cloud(df)
    logger.info(getLogFormat(text="Word Cloud Generated!"))

    status = {"statusMsg": "Word Cloud Generation Completed",
              "step": "5", "total": "5"}
    await send_message(status)

    tweets = generate_tweets(df)
    logger.info(getLogFormat(text="Results Generated!"))

    await asyncio.sleep(0.4)

    return (html_pie, html_timebar, html_hashtag_count, html_subject, word_clouds, tweets)


def generate_pie_chart(df):
    """
    A Helper function which takes the analysed data and generates pie chart based on sentiment type.

    Parameters
    ----------
    df : DataFrame, required

    Returns
    ------
    Pie Chart
        HTML Tags which define the pie chart generated
    """
    # Plotting and visualizing the counts
    data = df['sentiment'].value_counts()
    fig = px.pie(data, values=data.values, names=data.index.tolist(), width=1100,
                 height=500, hole=.3, color_discrete_sequence=px.colors.sequential.Teal_r)
    fig.update_layout(title_text='Sentiment Analysis')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return plotly.offline.plot(fig, output_type='div')


def generate_timebar(df):
    """
    A Helper function which takes the analysed data and makes call to helper function for generating bar charts for various time frequencies.

    Parameters
    ----------
    df : DataFrame, required

    Returns
    ------
    timebar
        a Python Dictionary which contains HTML tags for Bar charts of various time frequencies
    """
    timebar = {}
    timebar["timeline_5min"] = generate_timebar_for_freq(df, "5min")
    timebar["timeline_10min"] = generate_timebar_for_freq(df, "10min")
    timebar["timeline_15min"] = generate_timebar_for_freq(df, "15min")
    return timebar


def generate_timebar_for_freq(df, freq):
    """
    A Helper function which takes the analysed data and a time frequency to generate a timeline Bar Chart for the given frequency.

    Parameters
    ----------
    df : DataFrame, required

    freq : str, required

    Returns
    ------
    Bar Chart
        HTML tags which define the bar chart are generated
    """
    df = df.groupby(pd.Grouper(key="created_at", freq=freq)).count()
    fig = px.bar(df, x=df.index, y="id", labels={
                 "id": "tweets_count"}, width=800, height=500)
    fig.update_layout(
        title="Tweet Created Count with Frequency of "+str(freq[:-3])+" minutes")
    fig.update_traces(marker_color='rgb(158,202,225)',
                      marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
    fig.update_xaxes(tickvals=df.index, ticktext=[d.strftime(
        '%d/%b/%Y %H:%M') for d in df.index.to_list()])
    return plotly.offline.plot(fig, output_type='div')


def generate_hashtag_count_chart(hashtags_count):
    """
    A Helper function which takes the hashtags count data and generates a Bar Chart on the hashtag counts.

    Parameters
    ----------
    hashtags_count : Pandas Series, required

    Returns
    ------
    Bar Chart
        HTML tags which define the bar chart are generated
    """
    fig = px.bar(hashtags_count, y=hashtags_count.index,
                 x=hashtags_count.values, width=1100, height=600)
    fig.update_xaxes(title_text='Count')
    fig.update_yaxes(title_text='HashTags')
    fig.update_layout(title="Count of Hashtags used")
    fig.update_traces(marker_color='rgb(158,202,225)',
                      marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
    return plotly.offline.plot(fig, output_type='div')


def generate_subject_chart(df):
    """
    A Helper function which takes the analysed data and generates a scatter plot with respect to Subjectivity and Polarity of the tweet.

    Parameters
    ----------
    df : DataFrame, required

    Returns
    ------
    Scatter Plot
        HTML tags which define the Scatter Plot are generated
    """
    fig = px.scatter(df, x="polarity", y="subjectivity", color="sentiment", hover_data=[
                     "raw_tweet"], size="subjectivity", width=1100, height=600)
    fig.update_layout(
        title_text='Subjectivity-Polarity Relationship Based on Sentiment')
    return plotly.offline.plot(fig, output_type='div')


def split_Analysis(df):
    """
    A Helper function which takes the analysed data and splits it based on Analysis value for further processing.

    Parameters
    ----------
    df : DataFrame, required

    Returns
    ------
    DataFrames
        a set of dataframes separated based on Analysis value
    """
    positive_df = df[df["Analysis"] == 1]
    negative_df = df[df["Analysis"] == -1]
    neutral_df = df[df["Analysis"] == 0]
    return positive_df, negative_df, neutral_df


def generate_tweets(df):
    """
    A Helper function which takes the analysed data and makes calls for splitting it based on Analysis value for displaying.

    Parameters
    ----------
    df : DataFrame, required

    Returns
    ------
    tweets
        a Python Dictionary which contains analysed data separated based on Analysis value
    """
    positive, negative, neutral = split_Analysis(df)
    tweets = {}
    tweets["positive"] = positive.to_dict('records')
    tweets["negative"] = negative.to_dict('records')
    tweets["neutral"] = neutral.to_dict('records')
    return tweets


def generate_word_cloud(df):
    """
    A Helper function which takes the analysed data and generates word clouds on it.

    Parameters
    ----------
    df : DataFrame, required

    Returns
    ------
    WordCloud
        a WordCloud based on given data in SVG Format 
    """
    allWords = ' '.join([tweet for tweet in df['processed_tweet']])
    twitter_mask = np.array(Image.open(
        cwd + "\\sentiment\\static\\sentiment\\img\\test1.png"))
    wordCloud = WordCloud(background_color='white', max_words=100, mask=twitter_mask, contour_width=2.0, contour_color="#1DA1F2").generate(
        allWords).to_svg(embed_font=True, optimize_embedded_font=False, embed_image=True)
    return wordCloud


def word_cloud(df):
    """
    A Helper function which takes the analysed data and makes calls to generates word clouds on it.

    Parameters
    ----------
    df : DataFrame, required

    Returns
    ------
    word_clouds
        a Python Dictionary which contains word clouds based on Sentiment type
    """
    positive, negative, neutral = split_Analysis(df)
    word_clouds = {}
    word_clouds["positive"] = generate_word_cloud(positive)
    word_clouds["negative"] = generate_word_cloud(negative)
    word_clouds["neutral"] = generate_word_cloud(neutral)
    return word_clouds
