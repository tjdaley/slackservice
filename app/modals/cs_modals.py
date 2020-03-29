"""
cs_modals.py - Creates modal dialogs for the child support slash command.

Copyright (c) 2020 by Thomas J. Daley, J.D.
"""

class CsModals(object):
    def param_modal(self, trigger_id, callback_id):
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