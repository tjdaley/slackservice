"""
cs_modals.py - Creates modal dialogs for the child support slash command.

Copyright (c) 2020 by Thomas J. Daley, J.D.
"""


class CsModals(object):
    @staticmethod
    def param_model(trigger_id: str) -> dict:
        """
        Return dict that specifies a modal dialog to retrieve
        input parameters to compute child support.

        Args:
            trigger_id (str): Received from interaction.

        Returns:
            (dict): Slack modal dialog specification
        """
        return {
            'trigger_id': trigger_id,
            'view': {
                'type': 'modal',
                'callback_id': 'cs_param_modal',
                'title': {
                    'type': 'plain_text',
                    'text': "Child Support Calculation"
                },
                'blocks': [
                    {
                        'type': 'input',
                        'label': "Income amount",
                        'element': 'plain_text_input',
                        'block_id': 'income_amount',
                        'hint': "Enter the obligor's income",
                        'optional': False
                    }
                ]
            }
        }

    def param_modalx(self, trigger_id, callback_id):
        return {
            'trigger_id': trigger_id,
            'dialog': {
                'callback_id': callback_id,
                'title': "Calculate Child Support",
                'submit_label': "Calculate",
                'notify_on_cancel': True,
                'state': "get_params",
                'elements': [
                    {
                        'type': 'text',
                        'label': "Income",
                        'name': 'cs_income_amount',
                    },
                    {
                        'type': 'text',
                        'label': "Frequency",
                        'name': 'cs_income_frequency'
                    },
                    {
                        'type': 'text',
                        'label': "Health insurance",
                        'name': 'cs_ins_amount'
                    },
                    {
                        'type': 'text',
                        'label': "Frequency",
                        'name': 'cs_ins_frequency'
                    },
                    {
                        'type': 'text',
                        'label': "Children in action",
                        'name': 'cs_children_in',
                    },
                    {
                        'type': 'text',
                        'label': "Children outside action",
                        'name': 'cs_children_out'
                    },
                    {
                        'type': 'text',
                        'label': "Union dues",
                        'name': 'cs_union_amount'
                    },
                    {
                        'type': 'text',
                        'label': "Frequency",
                        'name': 'cs_union_frequency'
                    }
                ]
            }
        }