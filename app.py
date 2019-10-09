!/usr/bin/python3
#Service that receives SMS from twilio and turns the body text into an optical
# illusion button with pyedgeon, then uploading that image to imgur, using the
# public imgur link as an image source, and then sending that image via MMS to
# the client

import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from src.validate_sms import validate_sms
from src.weather import weather
from pathlib import Path
import logging

# create staic and logs folders if they don't exist
for f in ['img', 'logs']:
    if not os.path.exists(f):
        os.makedirs(f)

logging.basicConfig(filename='logs/app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.debug = True

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming with a simple text message."""
    # create MessagingResponse object and cast request to dict
    resp = MessagingResponse()
    rq = request.form.to_dict()
    logging.info(str(rq))
    # validate input and prepare txt, msg_id
    val = validate_sms(rq)
    try:
        assert val['validated'] == True
    except AssertionError as e:
        # handle case where there is an invalid input
        msg = resp.message(val['error'])
        return str(resp)
    # input is validated, proceed with directive determination
    directive = 0

    msg_id = rq['MessageSid']

    msg = resp.message("Thanks for using pyedgeon-service!")
    msg.media(img_link)

    logging.info('text:{text}'
                 .format(text=text,
                         fr=rq['From'],
                         to=rq['To'],
                         s=msg_id,
                         )
                 )
    return str(resp)

if __name__ == "__main__":
    app.run(port=5069)


