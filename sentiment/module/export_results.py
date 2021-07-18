import io
import csv
import pandas as pd
import json
from django.http import HttpResponse


def export_csv(data):
    df = str(data, 'utf-8').replace("\\n", "\n").replace("\'", "'")
    df = eval(df).strip('][').split('}, ')
    for i in range(len(df)):
        if(df[i][-1] != '}'):
            df[i] = df[i] + '}'
        df[i] = df[i].replace("Timestamp", "pd.Timestamp").replace(
            ", tz='tzutc()'", "")
        df[i] = eval(df[i])
    buffer = io.StringIO()
    csv_columns = list(df[0].keys())
    try:
        wr = csv.DictWriter(buffer, fieldnames=csv_columns)
        wr.writeheader()
        for row in df:
            wr.writerow(row)
    except:
        return "Error"
    fileContent = buffer.getvalue()
    buffer.close()
    response = HttpResponse(fileContent, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=tweets.csv'
    return response
