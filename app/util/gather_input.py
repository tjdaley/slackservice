"""
gather_input.py - Gather input from a Slack payload.

Copyright (c) 2020 by Thomas J. Daley, J.D.
"""
import json

class InputGatherer(object):
    """
    Gather user input from a Slack payload.
    """
    @staticmethod
    def gather(payload: dict) -> dict:
        """
        Create a dict of the user's input from the json string
        we received from slack when the user hit the [SUBMIT] button.

        Args:
            payload (dict): dict from Stack payload

        Returns:
            (dict): User's input.
        """
        result = {}

        # values will be a dict
        values = payload['view']['state']['values']
        for key, field in values.items():
            for field_name, value in field.items():
                v = PARSERS.get(value['type'])(value)
                result[field_name] = v
        
        return result

def get_static_select_value(input: dict) -> str:
    """
    Get the value selected from a drop-down.
    """
    if 'selected_option' in input:
        if 'value' in input['selected_option']:
            return input['selected_option']['value']
    return None


def get_plain_text_value(input: dict) -> str:
    """
    Get the value of a text input field.
    """
    return input.get('value', None)

PARSERS = {
    'static_select': get_static_select_value,
    'plain_text_input': get_plain_text_value
}
