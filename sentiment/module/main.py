import datetime as dt

# import Module Files
from .retrieve_tweets import retrieve_tweets
from .preprocess_tweets import preprocess_tweets
from .analyse_sentiment import analyse_sentiment
from .generate_results import generate
from .export_results import export_csv

# import forms
from ..forms import SearchEntriesForm

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


def constructFormData(request):
    data = dict()
    data["search_query"] = request.GET['query']
    if request.GET['date']:
        data["query_date"] = request.GET['date']
    else:
        data["query_date"] = dt.date.today().strftime('%Y-%m-%d')
    data["search_time"] = dt.datetime.now().strftime("%H:%M:%S")
    data["search_date"] = dt.date.today().strftime('%Y-%m-%d')
    data["user_host"] = request.headers._store["host"]
    data["user_agent"] = request.headers._store["user-agent"]

    return data


def saveSearchQuery(request):
    data = constructFormData(request)
    form = SearchEntriesForm(data)
    if form.is_valid():
        form.save()


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

    saveSearchQuery(request)

    return result


def export(body):
    return export_csv(body)
