import datetime
import time

def bubbleSort(events):
    context = {}
    n = len(events)
    print("number of all events: ", n)

    for i in range(n):
        for j in range(0, n - i - 1):
            if date_split2timestamp(str(events[j]['start']['dateTime'])) > date_split2timestamp(str(events[j+1]['start']['dateTime'])):
                # arr[j], arr[j + 1] = arr[j + 1], arr[j]
                events[j],events[j+1] = events[j+1],events[j]

    # print("after bubblesort: events: ", events)
    return events

def date_split2timestamp(string):
    # txt = "2020-07-24T09:00:00.0000000"
    # 2020-07-23T11:00:00+01:00
    # print('string: ', string)
    date = string.split("T")[0]
    timing = string.split("T")[1]

    year = date.split("-")[0]
    month = date.split("-")[1]
    day = date.split("-")[2]

    hour = timing.split(":")[0]
    minute = timing.split(":")[1]
    second = timing.split(":")[2]

    dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
    timestamp = time.mktime(dt.timetuple())


    return timestamp
if __name__ == '__main__':
    # date_split2timestamp("2020-07-24 09:00:00")

    events_values = [{'@odata.etag': 'W/"/0SMWdOpn0OA6nA1Y8eAKAAA99UIYA=="', 'id': 'AAMkADc2MjBlYjJhLTA1NGUtNDYyZC1hZWMyLWIyY2UwN2UyZWFjYgFRAAgI2C9kgirAAEYAAAAArMQ2PMEI2EmvUzkePJx0qgcA-0SMWdOpn0OA6nA1Y8eAKAAAAAABDQAA-0SMWdOpn0OA6nA1Y8eAKAAA_BJ60QAAEA==', 'subject': 'outlook event', 'start': {'dateTime': datetime.datetime(2020, 7, 24, 9, 0), 'timeZone': 'W. Europe Standard Time'}, 'end': {'dateTime': datetime.datetime(2020, 7, 24, 9, 30), 'timeZone': 'W. Europe Standard Time'}, 'organizer': {'emailAddress': {'name': 'FEI Wenchang', 'address': 'W.Fei@sms.ed.ac.uk'}}}, {'@odata.etag': 'W/"/0SMWdOpn0OA6nA1Y8eAKAAA99UIYA=="', 'id': 'AAMkADc2MjBlYjJhLTA1NGUtNDYyZC1hZWMyLWIyY2UwN2UyZWFjYgFRAAgI2DTkqw8AAEYAAAAArMQ2PMEI2EmvUzkePJx0qgcA-0SMWdOpn0OA6nA1Y8eAKAAAAAABDQAA-0SMWdOpn0OA6nA1Y8eAKAAA_BJ60QAAEA==', 'subject': 'outlook event', 'start': {'dateTime': datetime.datetime(2020, 7, 31, 9, 0), 'timeZone': 'W. Europe Standard Time'}, 'end': {'dateTime': datetime.datetime(2020, 7, 31, 9, 30), 'timeZone': 'W. Europe Standard Time'}, 'organizer': {'emailAddress': {'name': 'FEI Wenchang', 'address': 'W.Fei@sms.ed.ac.uk'}}}, {'@odata.etag': 'W/"/0SMWdOpn0OA6nA1Y8eAKAAA89fMDA=="', 'id': 'AAMkADc2MjBlYjJhLTA1NGUtNDYyZC1hZWMyLWIyY2UwN2UyZWFjYgFRAAgI2C3SLVdAAEYAAAAArMQ2PMEI2EmvUzkePJx0qgcA-0SMWdOpn0OA6nA1Y8eAKAAAAAABDQAA-0SMWdOpn0OA6nA1Y8eAKAAA6kEI_AAAEA==', 'subject': 'MSc Project Regular Meeting', 'start': {'dateTime': datetime.datetime(2020, 7, 22, 11, 0), 'timeZone': 'W. Europe Standard Time'}, 'end': {'dateTime': datetime.datetime(2020, 7, 22, 12, 0), 'timeZone': 'W. Europe Standard Time'}, 'organizer': {'emailAddress': {'name': 'MSc 2020: Calendar', 'address': 'MSc2020Calendar@uoe.onmicrosoft.com'}}}, {'@odata.etag': 'W/"/0SMWdOpn0OA6nA1Y8eAKAAA89fMDA=="', 'id': 'AAMkADc2MjBlYjJhLTA1NGUtNDYyZC1hZWMyLWIyY2UwN2UyZWFjYgFRAAgI2DNSVjuAAEYAAAAArMQ2PMEI2EmvUzkePJx0qgcA-0SMWdOpn0OA6nA1Y8eAKAAAAAABDQAA-0SMWdOpn0OA6nA1Y8eAKAAA6kEI_AAAEA==', 'subject': 'MSc Project Regular Meeting', 'start': {'dateTime': datetime.datetime(2020, 7, 29, 11, 0), 'timeZone': 'W. Europe Standard Time'}, 'end': {'dateTime': datetime.datetime(2020, 7, 29, 12, 0), 'timeZone': 'W. Europe Standard Time'}, 'organizer': {'emailAddress': {'name': 'MSc 2020: Calendar', 'address': 'MSc2020Calendar@uoe.onmicrosoft.com'}}}, {'@odata.etag': 'W/"/0SMWdOpn0OA6nA1Y8eAKAAA9ugsXQ=="', 'id': 'AAMkADc2MjBlYjJhLTA1NGUtNDYyZC1hZWMyLWIyY2UwN2UyZWFjYgFRAAgI2C3SLVdAAEYAAAAArMQ2PMEI2EmvUzkePJx0qgcA-0SMWdOpn0OA6nA1Y8eAKAAAAAABDQAA-0SMWdOpn0OA6nA1Y8eAKAAAdsxOfQAAEA==', 'subject': 'Scottish Politics ', 'start': {'dateTime': datetime.datetime(2020, 7, 22, 19, 30), 'timeZone': 'W. Europe Standard Time'}, 'end': {'dateTime': datetime.datetime(2020, 7, 22, 21, 30), 'timeZone': 'W. Europe Standard Time'}, 'organizer': {'emailAddress': {'name': 'FEI Wenchang', 'address': 'W.Fei@sms.ed.ac.uk'}}}, {'@odata.etag': 'W/"/0SMWdOpn0OA6nA1Y8eAKAAA9ugsXQ=="', 'id': 'AAMkADc2MjBlYjJhLTA1NGUtNDYyZC1hZWMyLWIyY2UwN2UyZWFjYgFRAAgI2DNSVjuAAEYAAAAArMQ2PMEI2EmvUzkePJx0qgcA-0SMWdOpn0OA6nA1Y8eAKAAAAAABDQAA-0SMWdOpn0OA6nA1Y8eAKAAAdsxOfQAAEA==', 'subject': 'Scottish Politics ', 'start': {'dateTime': datetime.datetime(2020, 7, 29, 19, 30), 'timeZone': 'W. Europe Standard Time'}, 'end': {'dateTime': datetime.datetime(2020, 7, 29, 21, 30), 'timeZone': 'W. Europe Standard Time'}, 'organizer': {'emailAddress': {'name': 'FEI Wenchang', 'address': 'W.Fei@sms.ed.ac.uk'}}}]
    bubbleSort(events_values)

