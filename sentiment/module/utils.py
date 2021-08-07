from channels.layers import get_channel_layer
import datetime as dt

# For Logging
import logging
logger = logging.getLogger('sentiment')


def getLogFormat(request='', text=''):
    try:
        date = '[ {} ]'.format(dt.datetime.now())
        if request:
            type = str(request.scope['type']).upper()
            version = str(request.scope['http_version'])
            method = str(request.scope['method'])
            path = str(request.scope['path'])
            host = str(request.headers._store["host"][1])
            val = ''
            if len(request.GET):
                val = request.GET.dict()
            if len(request.POST):
                val = request.POST.dict()
        if not text and request:
            msg = '{} {} {} {}  {} {} {}'.format(
                date, type, version, host, method, path, val)
        elif text and request:
            msg = '{} {} {} {}  {} {} {}'.format(
                date, type, version, host, method, path, text)
        else:
            msg = '{} {}'.format(date, text)
        return msg
    except:
        return "ERROR CREATING LOG ENTRY"


async def send_message(status):
    channel_layer = get_channel_layer()
    await channel_layer.group_send("status", {"type": "status.update", "text": status})
