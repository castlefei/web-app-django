from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_freebusy():
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
    print("Getting xiaolei's free busy time")
    calednarid = "xiaoleicheng2019@nlaw.northwestern.edu"
    body ={
            "calendarExpansionMax": 2,
            "groupExpansionMax": 2,
            "items": [
                {
                    "id": "xiaoleicheng2019@nlaw.northwestern.edu"
                }
            ],
            "timeMin": "2020-07-18T12:00:00Z",
            "timeMax": "2020-07-18T23:00:00Z",
            "timeZone": "W. Europe Standard Time"
            }

    events_result = service.freebusy().query(body=body).execute()

    events = events_result.get('calendars',[])
    print("events: ", events)
    events_cale = events.get(calednarid,[])
    print("events_cale: ", events_cale)
    events_busy = events_cale.get("busy",[])
    for event in events_busy:
        events_start = event.get("start")
        print("event start time: ", events_start)

if __name__ == '__main__':
    get_freebusy()
