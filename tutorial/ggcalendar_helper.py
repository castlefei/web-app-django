from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# from tutorial.order_helper import bubbleSort, date_split2timestamp
import time

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_ggevents():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=3, singleEvents=True,
                                        orderBy='startTime').execute()

    events = events_result.get('items', [])
    n = len(events)
    print("number of events in google calendar: ", n)

    if not events:
        print('No upcoming events found.')

    return events

def date_split2timestamp(string):

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
    get_ggevents()


