# utils/sms.py
import os
def send_sms(mobile, text):
    # DEV: print to console
    print(f"SMS to {mobile}: {text}")
    # PRODUCTION: implement Twilio or Fast2SMS here.
    # Example (Twilio):
    # from twilio.rest import Client
    # account_sid = os.getenv('TWILIO_SID')
    # auth_token  = os.getenv('TWILIO_TOKEN')
    # client = Client(account_sid, auth_token)
    # client.messages.create(body=text, from_='+1XXX', to=mobile)
