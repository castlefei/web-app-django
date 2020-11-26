from requests_oauthlib import OAuth2Session
graph_url = 'https://graph.microsoft.com/v1.0'


def create_and_addEvent(request, token):
    graph_client = OAuth2Session(token=token)

    body = {}
    body['subject'] = 'a meeting with '+ request.session['findmeetingtime']['invitee_addr']
    body['body'] = {
             "contentType": "HTML",
             "content": "some content in meeting test"}

    start_time = request.session['findmeetingtime']['timeChoice'].split(' - ')[0].split(' ')[0]+'T'+request.session['findmeetingtime']['timeChoice'].split(' - ')[0].split(' ')[1]
    end_time = request.session['findmeetingtime']['timeChoice'].split(' - ')[1].split(' ')[0]+'T'+request.session['findmeetingtime']['timeChoice'].split(' - ')[1].split(' ')[1]

    body['start'] = {
        "dateTime": start_time,
        "timeZone": "W. Europe Standard Time"
    }
    body['end'] = {
        "dateTime": end_time,
        "timeZone": "W. Europe Standard Time"
    }
    body['location'] = {
        "displayName": "8 Roxburgh Plae"
    }
    body['attendees'] = []
    attendee = {
        "emailAddress": {
            "address": request.session['findmeetingtime']['invitee_addr'],
            "name": request.session['findmeetingtime']['invitee_addr']
        },
        "type": "required"
    }
    body['attendees'].append(attendee)
    body['extensions'] = [{
        "@odata.type": "microsoft.graph.openTypeExtension",
        "extensionName": "webapp.test.testextension",
        "event_start": start_time,
        "event_end": end_time,
        "invitee_addr": request.session['findmeetingtime']['invitee_addr'],
        "meeting-when": request.session['findmeetingtime']['meeting-when'],
        "meeting-howlong": request.session['findmeetingtime']['meeting-howlong'],
        "meeting-type": request.session['findmeetingtime']['meeting-type'],
        "meeting-movable": request.session['findmeetingtime']['meeting-movable'],
        "meeting-priority": request.session['findmeetingtime']['meeting-priority'],
    }]

    creat_events_reply = graph_client.post('{0}/me/calendar/events'.format(graph_url), json=body)
    # print("create event reply: ", creat_events_reply.json())
    return creat_events_reply


# create an event that invitee choose the time and add it to calendar
def create_and_addEvent_byinvitee(request, token):
    graph_client = OAuth2Session(token=token)

    body = {}
    body['subject'] = 'a meeting with ' + request.session['findmeetingtime']['invitee_addr']
    body['body'] = {
        "contentType": "HTML",
        "content": "some content in meeting test"}

    start_time = request.GET['start_time']
    end_time = request.GET['end_time']

    body['start'] = {
        "dateTime": start_time,
        "timeZone": "W. Europe Standard Time"
    }
    body['end'] = {
        "dateTime": end_time,
        "timeZone": "W. Europe Standard Time"
    }
    body['location'] = {
        "displayName": "8 Roxburgh Plae"
    }
    body['attendees'] = []
    attendee = {
        "emailAddress": {
            "address": request.session['findmeetingtime']['invitee_addr'],
            "name": request.session['findmeetingtime']['invitee_addr']
        },
        "type": "required"
    }
    body['attendees'].append(attendee)
    body['extensions'] = [{
        "@odata.type": "microsoft.graph.openTypeExtension",
        "extensionName": "webapp.test.testextension",
        "event_start": start_time,
        "event_end": end_time,
        "invitee_addr": request.session['findmeetingtime']['invitee_addr'],
        "meeting-when": request.session['findmeetingtime']['meeting-when'],
        "meeting-howlong": request.session['findmeetingtime']['meeting-howlong'],
        "meeting-type": request.session['findmeetingtime']['meeting-type'],
        "meeting-movable": request.session['findmeetingtime']['meeting-movable'],
        "meeting-priority": request.session['findmeetingtime']['meeting-priority'],
    }]

    creat_events_reply = graph_client.post('{0}/me/calendar/events'.format(graph_url), json=body)
    # print("create event reply: ", creat_events_reply.json())
    return creat_events_reply


def getEvent_and_extension(event_id, extension_name, token):
    graph_client = OAuth2Session(token=token)

    reply = graph_client.get(('{0}/me/calendar/events/'+event_id+'/extensions/'+extension_name).format(graph_url))

    print('get event and extension')
    print('status code: ', reply.status_code)
    print('reply content: ', reply.json())

    return reply

def delete_event(event_id, token):
    graph_client = OAuth2Session(token=token)

    delete_events_reply = graph_client.delete(('{0}/me/calendar/events/'+event_id).format(graph_url))
    print("delete event status: ", delete_events_reply.status_code)
    return delete_events_reply.status_code

