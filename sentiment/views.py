from django.shortcuts import render
from django.http import HttpResponse
import json
import datetime as dt 
from . import retrieve_tweets, preprocess_tweets,analyse_sentiment,generate_results,export_results

date_list = []

def index(request):
    date_list.clear()
    today = dt.date.today()
    date_list.append("")
    date_list.append(today.strftime("%Y-%m-%d"))
    for i in range(1,7):
        date = today - dt.timedelta(days=i)
        date_list.append(date.strftime("%Y-%m-%d"))
    print(date_list)
    context = {
        'dates': date_list
    }
    return render(request, 'sentiment/index.html', context)

def searchQuery(request):
    keyword = request.GET['query']
    date = request.GET['date']
    
    if keyword:

        raw_tweets = retrieve_tweets.retrieve_tweets(keyword, date)
        processed_tweets_df, hashtags_count = preprocess_tweets.preprocess_tweets(raw_tweets)
        analyzed_data_df,analyzed_data = analyse_sentiment.analyse_sentiment(processed_tweets_df)
        senti_chart, timeline_chart, hashtag_chart, subject_chart, word_tags, tweets = generate_results.generate(analyzed_data_df,hashtags_count)

        query = {
            'keyword': keyword,
            'date': date,
            'senti_chart': senti_chart,
            'timeline_chart': timeline_chart,
            'hashtag_chart': hashtag_chart,
            'subject_chart': subject_chart,
            'word_tags' : word_tags,
            'tweets':tweets
        }
        
    
    date_list.clear()
    return render(request,'sentiment/results.html',query)

def export(request):
    if request.method == 'POST':
        # print(request.body)
        data = request.body
        return export_results.export_csv(data)
