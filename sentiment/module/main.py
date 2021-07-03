import datetime as dt

# import Module Files
from .retrieve_tweets import retrieve_tweets
from .preprocess_tweets import preprocess_tweets
from .analyse_sentiment import analyse_sentiment
from .generate_results import generate
from .export_results import export_csv

date_list = []


def getDateList():
    clearDateList()
    today = dt.date.today()
    date_list.append("")
    date_list.append(today.strftime("%Y-%m-%d"))
    for i in range(1, 7):
        date = today - dt.timedelta(days=i)
        date_list.append(date.strftime("%Y-%m-%d"))
    return date_list


def clearDateList():
    date_list.clear()


def processSearchQuery(request):
    clearDateList()

    result = dict()
    result["keyword"] = request.GET['query']
    result["date"] = request.GET['date']

    if result["keyword"]:
        raw_tweets = retrieve_tweets(result["keyword"], result["date"])
        processed_data = preprocess_tweets(raw_tweets)
        analysed_data = analyse_sentiment(processed_data[0])
        charts = generate(analysed_data[0], processed_data[1])

    if charts:
        result["senti_chart"] = charts[0]
        result["timeline_chart"] = charts[1]
        result["hashtag_chart"] = charts[2]
        result["subject_chart"] = charts[3]
        result["word_tags"] = charts[4]
        result["tweets"] = charts[5]

    return result


def export(body):
    return export_csv(body)
