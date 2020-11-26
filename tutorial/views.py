from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from tutorial.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from tutorial.graph_helper import get_user, get_calendar_events, post_findmeetingtime, post_freeorbusy, post_findmeetingtime_forC
import dateutil.parser
from tutorial.ggcalendar_helper import get_ggevents
from tutorial.order_helper import bubbleSort
from tutorial.mail_helper import create_and_sendEmail, create_and_sendEmailto_B, create_and_sendEmailto_C
from tutorial.event_helper import create_and_addEvent, getEvent_and_extension, create_and_addEvent_byinvitee, delete_event
from tutorial.strategy_helper import high_rank
# session
global_var = {
'eventinfo':[]
}
old_event = {}

# home page
def home(request):

    context = initialize_context(request)

    return render(request, 'tutorial/home.html', context)

# calendar page
def calendar(request):
    context = initialize_context(request)
    token = get_token(request)
    events = get_calendar_events(token)

    if events:
        events['value'].extend(get_ggevents())
        events['value'] = bubbleSort(events['value'])
        # Convert the ISO 8601 date times to a datetime object
        # This allows the Django template to format the value nicely
        for event in events['value']:
            event['start']['dateTime'] = dateutil.parser.parse(event['start']['dateTime'])
            event['end']['dateTime'] = dateutil.parser.parse(event['end']['dateTime'])

        context['events'] = events['value']
        # print("events: ", events['value'])
        # bubbleSort(events['value'])
    return render(request, 'tutorial/calendar.html', context)

# find meeting time page
def schedule_findmeetingtime(request):
    global global_var
    global old_event
    context = initialize_context(request)
    token = get_token(request)

    result = post_findmeetingtime(request, token)
    if result['emptySuggestionsReason']:
        # print('there is no suitable time slots.\n')
        # context['noSuggestionReasion'] = result['emptySuggestionsReason']
        context['suggestion'] = '0'
        request.session['eventinfo'] = global_var['eventinfo']

        old_event_info = high_rank(request, token)

        # if there is old event for replace
        if old_event_info:
            # old_event = old_event_info
            time = {
                'start': old_event_info['event_start'].split('T')[0]+' '+old_event_info['event_start'].split('T')[1],
                'end': old_event_info['event_end'].split('T')[0]+' '+old_event_info['event_end'].split('T')[1]
            }

            context['invitee_addr'] = request.POST['mail-addr']
            context['meeting-when'] = request.POST['when']
            context['meeting-howlong'] = request.POST['howlong']
            context['meeting-type'] = request.POST['type']
            context['meeting-movable'] = request.POST['movable']
            context['meeting-priority'] = request.POST['priority']

            context['old_event_time'] = time

            # send mail to ask delete old event
            old_reply = post_findmeetingtime_forC(old_event_info,token)
            if old_reply['emptySuggestionsReason']:
                # the old event can not be rescheduled (with no suitable slot)
                context['replaceable'] = "0"
                context['reason'] = "There is one previous event but it cannot be rescheduled."
                return render(request, 'tutorial/schedule.html', context)
            else:
                context['replaceable'] = "1"
                old_event = old_event_info
                old_suggestions = old_reply['meetingTimeSuggestions']

                context['old_suggestions_times'] = []
                for suggestion in old_suggestions:
                    time = {
                        'start': str(dateutil.parser.parse(suggestion['meetingTimeSlot']['start']['dateTime'])),
                        'end': str(dateutil.parser.parse(suggestion['meetingTimeSlot']['end']['dateTime']))
                    }
                    context['old_suggestions_times'].append(time)
                old_event['suggestions'] = context['old_suggestions_times']
                # print("global old_event: ", old_event)

        # if there is no old event for replace
        else:
            context['replaceable'] = "0"
            context['reason'] = 'canot find a previous event that can be replaced.'
            return render(request, 'tutorial/schedule.html', context)

    else:
        context['suggestion'] = '1'
        # print('there are some suitable time slots.\n')
        suggestions = result['meetingTimeSuggestions']
        num = len(suggestions)
        context['suggestions_num'] = num
        context['invitee_addr'] = request.POST['mail-addr']
        context['meeting-when'] = request.POST['when']
        context['meeting-howlong'] = request.POST['howlong']
        context['meeting-type'] = request.POST['type']
        context['meeting-movable'] = request.POST['movable']
        context['meeting-priority'] = request.POST['priority']
        context['suggestions_times'] = []
        for suggestion in suggestions:
            time = {
                'start': str(dateutil.parser.parse(suggestion['meetingTimeSlot']['start']['dateTime'])),
                'end': str(dateutil.parser.parse(suggestion['meetingTimeSlot']['end']['dateTime']))
            }
            context['suggestions_times'].append(time)

    # print("context: ", context)

    global_var['findmeetingtime'] = context
    request.session['findmeetingtime'] = context
    # print('gloval variable: ', global_var)
    return render(request, 'tutorial/schedule.html', context)

# page to handle response to invitations
def inviteeReply_handle(request):
    global global_var
    context = initialize_context(request)
    token = get_token(request)
    request.session['findmeetingtime'] = global_var['findmeetingtime']

    # create_and_addEvent(request, token)
    accept = request.GET['accept']
    # print('the accept of invitee is ', accept)
    if accept == '1':
        #i nvitee accept the request
        # print("the invitee has accepted the request")
        # print("all request session in invitee: ", request.session)
        # print("all request session[timechoice] in invitee: ", request.session['timeChoice'])
        # print("all request session[findmeetingtime] in invitee: ", request.session['findmeetingtime'])
        reply = create_and_addEvent(request, token)
        if reply.status_code == 200 or reply.status_code ==201 or reply.status_code == 202:
            print("the event has been created and added to Outlook. Request has been sent.")
            reply_json = reply.json()
            # print('reply json: ', reply_json)

            event = {
                'event_id': reply_json['id'],
                'extension_name': reply_json['extensions'][0]['extensionName']
            }
            global_var['eventinfo'].append(event)

            context['page_info'] = 'You have accepted the time slot of meeting. Meeting request mail has been sent to your email.'

        else:
            print("there may be some error happened. status code: ", reply.status_code)

    elif accept == '0':
        # invitee reject the request, do nothing
        # print("the invitee has rejected the request")
        context['page_info'] = 'You have rejected the time slot of meeting'

    elif accept == '2':
        # invitee selects another time slot
        # print("the invitee has selected another time slot")
        reply = create_and_addEvent_byinvitee(request, token)
        if reply.status_code == 200 or reply.status_code == 201 or reply.status_code == 202:
            # print("the event has been created and added to Outlook. Request has been sent.")
            reply_json = reply.json()
            event = {
                'event_id': reply_json['id'],
                'extension_name': reply_json['extensions'][0]['extensionName']
            }
            global_var['eventinfo'].append(event)

            context['page_info'] = 'You have chosen another time slot of meeting. Meeting request mail has been sent to your email.'
            # getEvent_and_extension(request, token)
    else:
        print("something wrong happened in accept.")

    return render(request, 'tutorial/invitee.html', context)

# page to handle multiple invitations
def inviteeB_handle(request):

    global global_var
    context = initialize_context(request)
    token = get_token(request)

    request.session['findmeetingtime'] = global_var['findmeetingtime']
    print('this is in inviteeB handle')
    # create_and_addEvent(request, token)
    accept = request.GET['accept']
    # print('the accept of invitee is ', accept)
    if accept == '1':
        #invitee accept the request
        print("the invitee has accepted the request")

        reply = create_and_addEvent_byinvitee(request, token)
        if reply.status_code == 200 or reply.status_code ==201 or reply.status_code == 202:
            print("the event has been created and added to Outlook. Request has been sent.")
            reply_json = reply.json()

            event = {
                'event_id': reply_json['id'],
                'extension_name': reply_json['extensions'][0]['extensionName']
            }
            global_var['eventinfo'].append(event)
            context['page_info'] = 'You have accepted the time slot of meeting. Meeting request mail has been sent to your email.'
        else:
            print("there may be some error happened. status code: ", reply.status_code)

    elif accept == '0':
        # invitee B reject the request, do nothing
        print("the invitee has rejected the request")

        context['page_info'] = 'You have rejected the time slot of meeting'

    else:
        print("something wrong happened in accept.")

    return render(request, 'tutorial/invitee.html', context)

# pages to handle multiple invitations
def inviteeC_handle(request):

    global global_var
    global old_event
    context = initialize_context(request)
    token = get_token(request)

    request.session['findmeetingtime'] = old_event
    print('this is in inviteeC handle')
    # create_and_addEvent(request, token)
    accept = request.GET['accept']
    # print('the accept of invitee is ', accept)
    if accept == '1':
        #invitee accept the request
        print("the invitee has accepted the request")
        print('old event id: ', old_event['eventid'])
        # delete the old event need event id old_event['eventid']
        delete_status = delete_event(old_event['eventid'], token)

        if delete_status == 204:
            # delete successfully and create event
            reply = create_and_addEvent_byinvitee(request, token)
            if reply.status_code == 200 or reply.status_code ==201 or reply.status_code == 202:
                print("the event has been created and added to Outlook. Request has been sent.")
                reply_json = reply.json()

                event = {
                    'event_id': reply_json['id'],
                    'extension_name': reply_json['extensions'][0]['extensionName']
                }

                global_var['eventinfo'].append(event)

                # getEvent_and_extension(request, token)
                context['page_info'] = 'You have accepted the time slot of meeting. Meeting request mail has been sent to your email.'
            else:
                print("there may be some error happened when creating event. status code: ", reply.status_code)
        else:
            print('deleting old event failed')

    elif accept == '0':
        # invitee reject the request, delete B if B exist
        print("the invitee has rejected the request")

        context['page_info'] = 'You have rejected the time slot of meeting'

    else:
        print("something wrong happened in accept.")

    return render(request, 'tutorial/invitee.html', context)

# page to mail to invitee
def mail(request):

    global global_var
    context = initialize_context(request)
    token = get_token(request)

    time_choice = request.POST['timeChoice']
    request.session['timeChoice'] = time_choice
    print('time choice:', time_choice)
    global_var['findmeetingtime']['timeChoice'] = time_choice
    status_code = create_and_sendEmail(request, token)
    context['status_code'] = status_code

    return render(request, 'tutorial/mail.html', context)


def mailtoBC(request):
    print('this is in mailtoBC function')
    # new event to B
    global global_var
    global old_event
    context = initialize_context(request)
    token = get_token(request)

    time_choice = global_var['findmeetingtime']['old_event_time']['start']+' - ' + global_var['findmeetingtime']['old_event_time']['end']

    request.session['timeChoice'] = time_choice
    print('time choice:', time_choice)
    global_var['findmeetingtime']['timeChoice'] = time_choice

    status_code = create_and_sendEmailto_B(request, token)
    context['status_code_B'] = status_code

    # old event to C
    request.session['old_event'] = old_event
    status_code = create_and_sendEmailto_C(request, token)
    context['status_code_C'] = status_code

    return render(request, 'tutorial/mail.html', context)

# page to get other's free or busy status
def schedule_getfreeorbusy(request):
    context = initialize_context(request)
    token = get_token(request)

    events = post_freeorbusy(token)
    context['errors'] = [
        {'message': 'Events', 'debug': format(events)}
    ]

    get_ggevents()
    return render(request, 'tutorial/schedule.html', context)

# page to get events from google calendar
def get_googleevents(request):
    context = initialize_context(request)
    get_ggevents()
    return render(request, 'tutorial/schedule.html', context)

# page to schedule meetings
def schedule(request):
    try:
    # context = initialize_context(request)
        pref_wh = request.POST['when']
        pref_hl = request.POST['howlong']
        pref_im = request.POST['important']
    except:
        return render(request, 'tutorial/preference.html', {
            'error_message': "You didn't select a choice.",
        })
    else:
        request.session['pref_when'] = pref_wh
        request.session['pref_howlong'] = pref_hl
        request.session['pref_important'] = pref_im

        return render(request, 'tutorial/schedule.html', {
            'pref_when': pref_wh,
            'pref_howlong': pref_hl,
            'pref_important': pref_im,
        })

# page for users to set preference.
def preference(request):
    # context = initialize_context(request)

    return render(request, 'tutorial/preference.html')


def initialize_context(request):
  context = {}

  # Check for any errors in the session
  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  # Check for user in the session
  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context


# The signin action generates the Azure AD signin URL,
# saves the state value generated by the OAuth client,
# then redirects the browser to the Azure AD signin page.
def sign_in(request):
  # Get the sign-in URL
  sign_in_url, state = get_sign_in_url()
  # Save the expected state so we can validate in the callback
  request.session['auth_state'] = state
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(sign_in_url)


def callback_p(request):
  # Get the state saved in session
  expected_state = request.session.pop('auth_state', '')
  # Make the token request
  token = get_token_from_code(request.get_full_path(), expected_state)
  # Temporary! Save the response in an error so it's displayed
  request.session['flash_error'] = { 'message': 'Token retrieved', 'debug': format(token) }
  return HttpResponseRedirect(reverse('home'))


def callback(request):
  # Get the state saved in session
  expected_state = request.session.pop('auth_state', '')
  # Make the token request
  token = get_token_from_code(request.get_full_path(), expected_state)

  # Get the user's profile
  user = get_user(token)

  # Save token and user
  store_token(request, token)
  store_user(request, user)

  return HttpResponseRedirect(reverse('home'))
  # return HttpResponseRedirect("http://7f6f44efd0e7.ngrok.io")

def sign_out(request):
  # Clear out the user and token
  remove_user_and_token(request)

  return HttpResponseRedirect(reverse('home'))
