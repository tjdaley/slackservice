"""
slackservice.py - Implements slash commands for slack service.

Copyright (c) 2020 by Thomas J. Daley, J.D.
"""
from flask import Flask, jsonify, request
from functools import wraps
import hashlib
import hmac
import json
import locale
import requests as req
import os
import time
import dotenv

from modals.cs_modals import CsModals
from util.gather_input import InputGatherer

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)
VERIFICATION_TOKEN = os.environ['VERIFICATION_TOKEN']
SIGNING_SECRET = str(os.environ['SLACK_SIGNING_SECRET'])
CLIENT_ID = os.environ['CLIENT_ID']
SLACK_URL = os.environ['SLACK_API_ENDPOINT']
CHANNELS = {}
RESPONSE_URLS = {}

locale.setlocale(locale.LC_ALL, '')

app = Flask(__name__)


def dump_dict(d):
    print("*"*80)
    print(json.dumps(d, indent=4))
    print("*"*80)


def dump_form():
    for token in request.form:
        print(f"{token} = {request.form[token]}")


def slack_headers():
    return {
        'Content-type': 'application/json; charset=utf-8',
        'Authorization': f'Bearer {CLIENT_ID}'
    }


def valid_submission() -> bool:
    """
    Validates using signing-secret per documentation available at
    http://api.slack.com/authenticatiopn/verifying-requests-from-slack
    """
    request_body = request.get_data(as_text=True)
    timestamp = request.headers['X-Slack-Request-Timestamp']

    # If it's more than 5 minute old, might be a replay attack.
    if abs(time.time() - float(timestamp)) > 60*5:
        return False

    sig_basestring = 'v0:' + timestamp + ':' + request_body
    my_signature = 'v0=' + hmac.new(
        bytes(SIGNING_SECRET, 'latin-1'),
        msg=bytes(sig_basestring, 'latin-1'),
        digestmod=hashlib.sha256
    ).hexdigest()
    slack_signature = request.headers['X-Slack-Signature']
    if hmac.compare_digest(my_signature, slack_signature):
        return True
    return False


# Verifies that the message has not been tampered with.
def is_verified_message(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if valid_submission():
            return f(*args, **kwargs)
        print('Unverified message received')
        return('', 204)
    return wrap


def post_message(message: dict):
    headers = slack_headers()
    url = f'{SLACK_URL}/chat.postMessage'
    result = req.post(url, data=json.dumps(message), headers=headers)
    print('*'*40, '\n\n', result.text, '\n\n', '*'*40)


def open_view(dialog: dict):
    headers = slack_headers()
    url = f'{SLACK_URL}/views.open'
    result = req.post(url, data=json.dumps(dialog), headers=headers)
    print('*'*40, '\n\n', result.text, '\n\n', '*'*40)


def push_view(dialog: dict):
    headers = slack_headers()
    url = f'{SLACK_URL}/views.push'
    result = req.post(url, data=json.dumps(dialog), headers=headers)
    print('*'*40, '\n\n', result.text, '\n\n', '*'*40)


@app.route('/slack/slash/cs', methods=['POST'])
@is_verified_message
def slack_slash_cs():
    if 'ssl_check' in request.form and request.form['ssl_check'] == '1':
        return('', 204)
    # dump_form()

    user_id = request.form['user_id']
    channel_id = request.form['channel_id']
    response_url = request.form['response_url']
    CHANNELS[user_id] = channel_id
    RESPONSE_URLS[user_id] = response_url

    trigger_id = request.form['trigger_id']
    modal = CsModals.param_modal(trigger_id)
    open_view(modal)
    return('', 204)


@app.route('/slack/interactive', methods=['POST'])
@is_verified_message
def slack_interactive():
    payload = json.loads(request.form['payload'])

    user_id = payload['user']['id']
    channel_id = CHANNELS.get(user_id, None)
    user_input = InputGatherer.gather(payload)
    # dump_dict(user_input)
    CsModals.calculate_child_support(user_input)
    # dump_dict(user_input)
    money_amount = locale.currency(user_input['child_support_monthly'], grouping=True)

    title_len = 25
    data_len = 10
    mg_t = "Monthly Gross:".ljust(title_len)
    ss_t = "Less: Social Security".ljust(title_len)
    mc_t = "      Medicare".ljust(title_len)
    mi_t = "      Medical Ins.".ljust(title_len)
    di_t = "      Dental Ins.".ljust(title_len)
    ft_t = "      Federal Income Tax".ljust(title_len)
    ud_t = "      Union Dues".ljust(title_len)
    nr_t = "Net Resources".ljust(title_len)
    mg_d = locale.currency(user_input['gross_income_monthly'], grouping=True).rjust(data_len)
    ss_d = locale.currency(-user_input['social_sec_monthly'], grouping=True).rjust(data_len)
    mc_d = locale.currency(-user_input['medicare_monthly'], grouping=True).rjust(data_len)
    mi_d = locale.currency(-user_input['medical_monthly'], grouping=True).rjust(data_len)
    di_d = locale.currency(-user_input['dental_monthly'], grouping=True).rjust(data_len)
    ft_d = locale.currency(-user_input['income_tax_monthly'], grouping=True).rjust(data_len)
    ud_d = locale.currency(-user_input['union_dues_monthly'], grouping=True).rjust(data_len)
    nr_d = locale.currency(user_input['net_resources_monthly'], grouping=True).rjust(data_len)
    message = f"Guideline child support: {money_amount}/month.\n" + \
              f"```{mg_t} {mg_d}\n" + \
              f"{ss_t} {ss_d}\n" + \
              f"{mc_t} {mc_d}\n" + \
              f"{mi_t} {mi_d}\n" + \
              f"{di_t} {di_d}\n" + \
              f"{ft_t} {ft_d}\n" + \
              f"{ud_t} {ud_d}\n" + \
              "" + '-'*(title_len+data_len+1) + "\n" + \
              f"{nr_t} {nr_d}\n```"
    message = {
        'text': message,
        'response_type': 'ephmeral',
        'channel': channel_id
    }
    post_message(message)
    return('', 204)


if __name__ == '__main__':
    port = int(os.environ['LISTEN_PORT'])
    app.run(host='0.0.0.0', port=port)
