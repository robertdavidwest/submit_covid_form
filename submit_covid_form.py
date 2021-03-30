import os
import json
import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from private_config import TWILIO_CONFIG, USERS


NAME_ID = 'AeCw0MXquUhr'
EMAIL_ID = 'uRQDBI5qGoQH'
GET_URL = 'https://bachfeedbackv2.typeform.com/to/cDTteMfM'
POST_URL = 'https://bachfeedbackv2.typeform.com/forms/cDTteMfM/complete-submission'

BAD_COMMAND_RESPONSE = 'I did not understand your request. Please try again'
BAD_USER_RESPONSE = 'I do not recognise this user. Please try again'

COVID_FORM_SUCCESS_MSG = "Successfully completed covid form submission"
COVID_FORM_FAIL_MSG = "Form submission was not successful"


def get_compliment():
    url = 'https://complimentr.com/api'
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()['compliment']
    else:
        return ''


def get_repo_dir():
    """Get the dir. It will be different in dev vs prod server runs"""
    this_dir = os.getcwd()
    home_dir = os.getenv("HOME")
    if this_dir == home_dir:
        dir_ = os.path.join(this_dir, 'submit_covid_form')
    else:
        dir_ = this_dir
    return dir_


def get_post_data(name, email):
    _dir = get_repo_dir()
    path = os.path.join(_dir, 'data_template.json')
    data_template = json.load(open(path, 'r'))
    for item in data_template['answers']:
        if item['field']['id'] == NAME_ID:
            item['text'] = name
        elif item['field']['id'] == EMAIL_ID:
            item['email'] = email
    return data_template


def submit_form(name, email, test):
    if test:
        return 'TEST::' + COVID_FORM_SUCCESS_MSG

    data = get_post_data(name, email)
    headers = {
            'content-Type': 'application/json'}
    r = requests.post(POST_URL, json=data, headers=headers)
    if (r.status_code == 200 ) & (r.json().get('type')=='completed'):
        return COVID_FORM_SUCCESS_MSG
    else:
        return COVID_FORM_FAIL_MSG
    


def send_text(msg, to):
    client = Client(TWILIO_CONFIG['account_sid'],
                    TWILIO_CONFIG['auth_token'])
    message = client.messages.create(
        to=to,
        from_=TWILIO_CONFIG['phone'],
        body=msg)


def run_bac_job(u, test):
    msg = submit_form(u['name'], u['email'], test)

    if u['username'] == 'sarah':
        msg += '\n'
        msg += get_compliment()
    send_text(msg, u['phone'])


def get_user_config(username):
    users = [x for x in USERS if x['username']==username]
    if len(users) != 1:
        return
    return users[0]


app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""

    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    body = body.lower()
    words = body.split(' ')
    job = words[0]
    if len(words) > 1:
        username = words[1]
    else:
        username = None
    
    if len(words) > 2:
        if words[2]=='test':
            test = True
        else:
            test = False
    else:
        test = False

    # Start our TwiML response
    resp = MessagingResponse()
    
    user_config = get_user_config(username)

    # submit form for permitted users
    if job != 'bac':
        resp.message(BAD_COMMAND_RESPONSE)
    elif not user_config:
        resp.message(BAD_USER_RESPONSE)
    else:
        run_bac_job(user_config, test)

    return str(resp)


@app.route('/')
def hello_world():
    return 'Doesn’t matter if it’s out of tune coz your cool'


if __name__ == "__main__":
    app.run(debug=True)
