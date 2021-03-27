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


def main():
    name = users[0]['name']
    email = users[0]['email']
    to = users[0]['phone']
    send_text(
        submit_form(name, email),
        to=to)

'''
app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message("The Robots are coming! Head for the hills!")

    return str(resp)
'''

if __name__ == "__main__":
    app.run(debug=True)
    main()
