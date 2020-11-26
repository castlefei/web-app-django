from requests_oauthlib import OAuth2Session
graph_url = 'https://graph.microsoft.com/v1.0'


def create_and_sendEmail(request, token):
    url = 'http://localhost:8000/invitee'
    # url = 'https://5a08a291958f.ngrok.io/invitee'

    graph_client = OAuth2Session(token=token)
    findtimes = request.session['findmeetingtime']

    print('request.session: ', findtimes)

    # time_choice = 2020-07-29 12:00:00 - 2020-07-29 15:00:00
    time_choice = request.POST['timeChoice']
    # print('time choice:', time_choice)


    headers = {"Content-type": "application/json"
               }

    body = {}
    body['message'] = {}
    body['message']['subject'] = "Meeting request - automated for test"
    body['message']['body'] = {}
    body['message']['body']['contentType'] = "HTML"
    body['message']['body']['content'] = "<p>Hi! How are you these days?</p>" \
                                         + "<p>Would you like to have a meeting with me from "+ time_choice +"?</p>"\
                                         + "<p><a href="+url+"?accept=1"+">I accept this meeting request</a></p>" \
                                         + "<p><a href="+url+"?accept=0"+">I reject this meeting request</a></p>" \
                                         + "<p>There are some other time slots that may be suitable for us. Please contact with me before making the choice.</p>"

    for time in findtimes['suggestions_times']:
        # time['start'] = 2020-08-03 10:00:00  => 2020-08-03T10:00:00
        time_start_t = time['start'].split(' ')[0]+'T'+time['start'].split(' ')[1]
        time_end_t = time['end'].split(' ')[0] + 'T' + time['end'].split(' ')[1]
        body['message']['body']['content'] = body['message']['body']['content']+"<p><a href="+url+"?accept=2&start_time="+time_start_t+"&end_time="+time_end_t+">"+ time['start']+" - "+ time['end']+"</a></p>"

    body['message']['body']['content'] = body['message']['body']['content']+"<p>This message is from "+ findtimes['user']['name']+"</p>"
    body['message']['toRecipients'] = []
    invitee = {
                "emailAddress": {
                        "address": findtimes['invitee_addr']
                    }
                }
    body['message']['toRecipients'].append(invitee)
    body['saveToSentItems'] = 'true'


    respond = graph_client.post('{0}/me/sendMail'.format(graph_url), headers=headers, json=body)
    # print('send mail respond: ', respond)

    return respond.status_code
    # return 202

# new event, there is only one time slot
def create_and_sendEmailto_B(request, token):
    print("this is in create_and_sendEmailto_B")
    # url = 'http://localhost:8000/inviteeB'
    url = 'https://5a08a291958f.ngrok.io/inviteeB'
    graph_client = OAuth2Session(token=token)
    findtimes = request.session['findmeetingtime']

    print('request.session: ', findtimes)

    # time_choice = 2020-07-29 12:00:00 - 2020-07-29 15:00:00
    time_choice = request.session['timeChoice']
    start_time = time_choice.split(' - ')[0].split(' ')[0]+'T'+time_choice.split(' - ')[0].split(' ')[1]
    end_time = time_choice.split(' - ')[1].split(' ')[0] + 'T' + time_choice.split(' - ')[1].split(' ')[1]

    headers = {"Content-type": "application/json"
               }

    body = {}
    body['message'] = {}
    body['message']['subject'] = "Meeting request - automated for test"
    body['message']['body'] = {}
    body['message']['body']['contentType'] = "HTML"
    body['message']['body']['content'] = "<p>Hi! How are you these days?</p>" \
                                         + "<p>Would you like to have a meeting with me from "+ time_choice +"?</p>"\
                                         + "<p><a href="+url+"?accept=1&start_time="+start_time+"&end_time="+end_time+">I accept this meeting request</a></p>" \
                                         + "<p><a href="+url+"?accept=0"+">I reject this meeting request</a></p>"

    body['message']['body']['content'] = body['message']['body']['content']+"<p>This message is from "+ findtimes['user']['name']+"</p>"
    body['message']['toRecipients'] = []

    invitee = {
                "emailAddress": {
                        "address": findtimes['invitee_addr']
                    }
                }
    body['message']['toRecipients'].append(invitee)
    body['saveToSentItems'] = 'true'

    respond = graph_client.post('{0}/me/sendMail'.format(graph_url), headers=headers, json=body)
    # print('send mail respond: ', respond)

    return respond.status_code


def create_and_sendEmailto_C(request, token):
    print("this is in create_and_sendEmailto_C")

    # url = 'http://localhost:8000/inviteeC'
    url = 'https://5a08a291958f.ngrok.io/inviteeC'
    graph_client = OAuth2Session(token=token)
    findtimes = request.session['findmeetingtime']
    old_event = request.session['old_event']

    print('request.session: ', findtimes)

    # time_choice = 2020-07-29 12:00:00 - 2020-07-29 15:00:00
    replaced_time_choice = request.session['timeChoice']

    time_choice = request.POST['timeChoice_old']
    # print('time choice:', time_choice)
    start_time = time_choice.split(' - ')[0].split(' ')[0] + 'T' + time_choice.split(' - ')[0].split(' ')[1]
    end_time = time_choice.split(' - ')[1].split(' ')[0] + 'T' + time_choice.split(' - ')[1].split(' ')[1]

    # request.session['old_event'] = old_event

    headers = {"Content-type": "application/json"
               }

    body = {}
    body['message'] = {}
    body['message']['subject'] = "Meeting request - automated for test"
    body['message']['body'] = {}
    body['message']['body']['contentType'] = "HTML"
    body['message']['body']['content'] = "<p>Hi! How are you these days?</p>" \
                                         + "<p>There are some conflicts in my calendar so would you like change the time of our meeting  from "+ replaced_time_choice+" to "+ time_choice +"?</p>"\
                                         + "<p><a href="+url+"?accept=1&start_time="+start_time+"&end_time="+end_time+">I accept this new time slot</a></p>" \
                                         + "<p><a href="+url+"?accept=0"+">I reject this change</a></p>" \
                                         + "<p>There are some other time slots that may be suitable for us. Please contact with me before making the choice.</p>"

    for time in old_event['suggestions']:
        # time['start'] = 2020-08-03 10:00:00  => 2020-08-03T10:00:00
        time_start_t = time['start'].split(' ')[0]+'T'+time['start'].split(' ')[1]
        time_end_t = time['end'].split(' ')[0] + 'T' + time['end'].split(' ')[1]
        body['message']['body']['content'] = body['message']['body']['content']+"<p><a href="+url+"?accept=1&start_time="+time_start_t+"&end_time="+time_end_t+">"+ time['start']+" - "+ time['end']+"</a></p>"

    body['message']['body']['content'] = body['message']['body']['content']+"<p>This message is from "+ findtimes['user']['name']+"</p>"
    body['message']['toRecipients'] = []
    invitee = {
                "emailAddress": {
                        "address": old_event['invitee_addr']
                    }
                }
    body['message']['toRecipients'].append(invitee)
    body['saveToSentItems'] = 'true'

    respond = graph_client.post('{0}/me/sendMail'.format(graph_url), headers=headers, json=body)
    # print('send mail respond: ', respond)

    return respond.status_code
