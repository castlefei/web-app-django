from requests_oauthlib import OAuth2Session
from tutorial.event_helper import create_and_addEvent,getEvent_and_extension, create_and_addEvent_byinvitee
import time
import datetime
from tutorial.order_helper import date_split2timestamp

def high_rank(request, token):
    print("this is in high rank function")
    new_priority = request.POST['priority']
    now = datetime.datetime.utcnow()
    new_time_end = (now + datetime.timedelta(days=int(request.POST['when'])))
    new_timestamp = time.mktime(new_time_end.timetuple())

    for event_info in request.session['eventinfo']:
        event_id = event_info['event_id']
        extension_name = event_info['extension_name']
        result = getEvent_and_extension(event_id, extension_name, token)

        # need to judge whether result is successful or not,
        # since users may delete events in web outlook so it will return 500.
        if result.status_code == 200:
            result = result.json()
            old_time_end = result['event_end']
            old_timestamp = date_split2timestamp(old_time_end)
            if new_timestamp > old_timestamp:
                if result['meeting-movable']=='1':
                    old_priority = result['meeting-priority']
                    if new_priority > old_priority:
                        print("find an old event")
                        print("meeting with: ", result['invitee_addr'])
                        print("start time: ", result['event_start'])
                        # may return a list of suitable old events in future!!!
                        result['eventid'] = event_id
                        return result

    print("there is no old event that can be replaced.")
    return []


