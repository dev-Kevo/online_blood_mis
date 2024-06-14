import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
organization_number = os.environ['TWILIO_TRIAL_NUMBER']



def sent_sms(to, body, from_=organization_number):
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                from_= from_, #'+15017122661',
                                body= body, #'Hi there',
                                to= to #'+15558675310'
                            )

    print(message.sid)