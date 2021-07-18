import datetime as dt

# import Module Files
from .retrieve_tweets import retrieve_tweets
from .preprocess_tweets import preprocess_tweets
from .analyse_sentiment import analyse_sentiment
from .generate_results import generate
from .export_results import export_csv

# import forms
from ..forms import SearchEntriesForm

# import channels
from channels.layers import get_channel_layer
import asyncio

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
    data["search_query"] = request.POST['query']
    if request.POST['date']:
        data["query_date"] = request.POST['date']
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


async def send_message(status):
    channel_layer = get_channel_layer()
    await channel_layer.group_send("status", {"type": "status.update", "text": status})


async def processSearchQuery(request):
    clearDateList()

    result = dict()
    result["keyword"] = request.POST['query']
    result["date"] = request.POST['date']

    status = {"statusMsg": "Processing Search Query",
              "step": "0", "total": "5"}
    await send_message(status)

    if result["keyword"]:
        raw_tweets = await asyncio.gather(retrieve_tweets(result["keyword"], result["date"]))
        processed_data = await asyncio.gather(preprocess_tweets(raw_tweets[0]))
        analysed_data = await asyncio.gather(analyse_sentiment(processed_data[0][0]))
        charts = await asyncio.gather(generate(analysed_data[0][0], processed_data[0][1]))

    if charts:
        result["senti_chart"] = charts[0][0]
        result["timeline_chart"] = charts[0][1]
        result["hashtag_chart"] = charts[0][2]
        result["subject_chart"] = charts[0][3]
        result["word_tags"] = charts[0][4]
        result["tweets"] = charts[0][5]

    return result


def export(body):
    return export_csv(body)
