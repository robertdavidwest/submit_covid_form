# submit_covid_form

Send simple text message command to submit covid form for gym so I don't have to fill it out every time I go.


### private_config.py setup to run main.py

```
TWILIO_CONFIG = {
    'account_sid': '',
    'auth_token': '',
    'phone': '+1XXXXXXXXXX'
    }

USERS = [
    {'name': '',
     'email': '',
     'phone': '+1XXXXXXXXXX},

    {'name': '',
     'email': '',
     'phone': '+1XXXXXXXXXX},
     ...
     ]
```

### How to use service :

Once you have the app running on a server. You simply text the following to submit the form:

```
bac <user>
```

where `<user>` is the `username` of the person you want to submit the form for. 

There is also a test mode. By typing:

```
bac <user> test
```
You can fully interact with the app but the form will not be submitted. 

### Like compliments?

There is also a random compliment generator that you can choose to close the msg with and choose which users receive the compliments
