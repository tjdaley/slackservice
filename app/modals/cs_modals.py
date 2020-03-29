"""
cs_modals.py - Creates modal dialogs for the child support slash command.

Copyright (c) 2020 by Thomas J. Daley, J.D.
"""
import json


class CsModals(object):
    @staticmethod
    def param_modal(trigger_id: str) -> dict:
        """
        Return dict that specifies a modal dialog to retrieve
        input parameters to compute child support.

        Args:
            trigger_id (str): Received from interaction.

        Returns:
            (dict): Slack modal dialog specification
        """
        with open('./view/cs_params_view.json', 'r') as fp:
            view = json.load(fp)
        return {
            'trigger_id': trigger_id,
            'view': view
        }
