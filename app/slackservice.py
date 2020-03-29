"""
slackservice.py - Implements slash commands for slack service.

Copyright (c) 2020 by Thomas J. Daley, J.D.
"""
from flask import Flask, jsonify, request
import os
import dotenv

from modals.cs_modals import CsModals

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)
VERIFICATION_TOKEN = os.environ['VERIFICATION_TOKEN']

app = Flask(__name__)


@app.route('/slack/slash/cs', methods=['POST'])
def slack_slash_cs():
    if request.form['token'] == VERIFICATION_TOKEN:
        payload = {
            'text': "Hi, Tom. Would you like to play a game?"
        }

        for token in request.form:
            print(f"{token} = {request.form[token]}")

        trigger_id = request.form['trigger_id']
        callback_id = 'cs_calc'
        dialog = CsModals.param_modal(None, trigger_id, callback_id)

        return(jsonify(dialog))


if __name__ == '__main__':
    port = int(os.environ['LISTEN_PORT'])
    app.run(host='0.0.0.0', port=port)
