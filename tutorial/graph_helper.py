from requests_oauthlib import OAuth2Session
import datetime
graph_url = 'https://graph.microsoft.com/v1.0'

def get_user(token):
  graph_client = OAuth2Session(token=token)
  # Send GET to /me
  user = graph_client.get('{0}/me'.format(graph_url))
  # Return the JSON result
  return user.json()

def get_calendar_events(token):
  graph_client = OAuth2Session(token=token)
  headers = {
             'Prefer': 'outlook.timezone = "W. Europe Standard Time"'
             }
  # Configure query parameters to
  # modify the results
  query_params = {
     '$select': 'subject,organizer,start,end',
      'startdatetime': '2020-07-20T07:39:40.604Z',
      'enddatetime': '2020-08-3T07:39:40.604Z'
  }

  # Send GET to /me/events
  events = graph_client.get('{0}/me/calendar/calendarview'.format(graph_url), headers = headers,params=query_params)
  # Return the JSON result
  return events.json()


def post_findmeetingtime(request, token):
    graph_client = OAuth2Session(token=token)
    headers = {"Content-type": "application/json",
            'Prefer': 'outlook.timezone = "W. Europe Standard Time"'
    }
    now = datetime.datetime.utcnow().isoformat()

    body = {}
    body['attendees']=[]
    attend = {
        "type": "required",
        "emailAddress": {

            "address": request.POST['mail-addr']
        }
    }

    body['attendees'].append(attend)
    body['timeConstraint'] = {}
    body['timeConstraint']['activityDomain'] = request.POST['type']
    body['timeConstraint']['timeslots'] = []
    time = {
            "start": {
              "dateTime": now,
              "timeZone": "W. Europe Standard Time"
            },
            "end": {
              "dateTime": (datetime.datetime.utcnow()+datetime.timedelta(days=int(request.POST['when']))).isoformat(),
              "timeZone": "W. Europe Standard Time"
            }
          }

    body['timeConstraint']['timeslots'].append(time)
    body['meetingDuration'] = request.POST['howlong']
    body['returnSuggestionReasons'] = True
    body['minimumAttendeePercentage'] = 100

    body_example = {
      "attendees": [
        {
          "type": "required",
          "emailAddress": {
            # "name": "Xiaolei Cheng",
            "address": "s1854521@ed.ac.uk"
          }
        }
      ],
      "timeConstraint": {
        "activityDomain":"work",
        "timeslots": [
          {
            "start": {
              "dateTime": "2020-07-16T09:00:00",
              "timeZone": "W. Europe Standard Time"
            },
            "end": {
              "dateTime": "2020-07-20T17:00:00",
              "timeZone": "W. Europe Standard Time"
            }
          }
        ]
      },
      "meetingDuration": "PT2H",
      "returnSuggestionReasons": True,
      "minimumAttendeePercentage": 100
    }
    events = graph_client.post('{0}/me/findMeetingTimes'.format(graph_url), headers=headers, json=body)
    # Return the JSON result
    return events.json()



def post_findmeetingtime_forC(context, token):
    graph_client = OAuth2Session(token=token)
    headers = {"Content-type": "application/json",
            'Prefer': 'outlook.timezone = "W. Europe Standard Time"'
    }
    now = datetime.datetime.utcnow().isoformat()
    body = {}
    body['attendees']=[]
    attend = {
        "type": "required",
        "emailAddress": {
            # "name": "Xiaolei Cheng",
            "address": context['invitee_addr']
        }
    }

    body['attendees'].append(attend)
    body['timeConstraint'] = {}
    body['timeConstraint']['activityDomain'] = context['meeting-type']
    body['timeConstraint']['timeslots'] = []
    time = {
            "start": {
              "dateTime": now,
              "timeZone": "W. Europe Standard Time"
            },
            "end": {
              "dateTime": (datetime.datetime.utcnow()+datetime.timedelta(days=int(context['meeting-when']))).isoformat(),
              "timeZone": "W. Europe Standard Time"
            }
          }

    body['timeConstraint']['timeslots'].append(time)
    body['meetingDuration'] = context['meeting-howlong']
    body['returnSuggestionReasons'] = True
    body['minimumAttendeePercentage'] = 100
    # print('request body: ', body)

    events = graph_client.post('{0}/me/findMeetingTimes'.format(graph_url), headers=headers, json=body)
    # Return the JSON result
    return events.json()

def post_freeorbusy(token):
  graph_client = OAuth2Session(token=token)
  headers = {"Content-type": "application/json",
              'Prefer': 'outlook.timezone = "W. Europe Standard Time"'
  }
  body= {
        "Schedules": ["s1854521@ed.ac.uk"],
        "StartTime": {
            "dateTime": "2020-07-14T09:00:00",
            "timeZone": "W. Europe Standard Time"
            # "timeZone": "Pacific Standard Time"
        },
        "EndTime": {
            "dateTime": "2020-07-14T18:00:00",
            "timeZone": "W. Europe Standard Time"
        },
        "availabilityViewInterval": "60"
    }
  events = graph_client.post('{0}/me/calendar/getschedule'.format(graph_url), headers=headers, json=body)
  # Return the JSON result
  return events.json()

