import json
import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from private_config import twilio_config, users


NAME_ID = 'AeCw0MXquUhr'
EMAIL_ID = 'uRQDBI5qGoQH'
GET_URL = 'https://bachfeedbackv2.typeform.com/to/cDTteMfM'
POST_URL = 'https://bachfeedbackv2.typeform.com/forms/cDTteMfM/complete-submission'

BAD_COMMAND_RESPONSE = 'I did not understand your request. Please try again'
BAD_USER_RESPONSE = 'I do not recognise this user. Please try again'


def get_complement():
    url = 'https://complimentr.com/api'
    r = requests.get(url)
    if r.status_code == 200:
        return i.json()['compliment']
    else:
        return ''


def get_post_data(name, email):
    data_template = json.load(open('data_template.json', 'r'))
    for item in data_template['answers']:
        if item['field']['id'] == NAME_ID:
            item['text'] = name
        elif item['field']['id'] == EMAIL_ID:
            item['email'] = email
    return data_template


def submit_form(name, email):
	data = get_post_data(name, email)
	headers = {
		'content-Type': 'application/json'}
	r = requests.post(POST_URL, json=data, headers=headers)
	if (r.status_code == 200 ) & (r.json().get('type')=='completed'):
		return "Successfully completed covid form submission"
	else:
		return "Form submission was not successful"


def send_text(msg, to):
    client = Client(twilio_config['account_sid'],
                    twilio_config['auth_token'])
    message = client.messages.create(
        to=to,
        from_=twilio_config['phone'],
        body=msg)


def run_bac_job(username):
    users = [x for x in users if x['username']==username]
    if len(users) != 1:
        return
    u = users[0]
    msg = submit_form(u['name'], u['email']),

    if u['username'] == 'sarah':
        msg += '\n'
        msg += get_compliment()
    send_text(msg, u['phone'])


app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""

    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    words = bodys.split(' ')
    job = words[0]
    if len(words) > 1:
        username = words[1]
    else:
        username = None

    # Start our TwiML response
    resp = MessagingResponse()

    # submit form for permitted users
    if job != 'bac':
        resp.message(BAD_COMMAND_RESPONSE)
    elif username !='robert':
        resp.message(BAD_USER_RESPONSE)
    else:
        run_bac_job(username)


    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
