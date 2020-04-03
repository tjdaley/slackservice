"""
cs_modals.py - Creates modal dialogs for the child support slash command.

Copyright (c) 2020 by Thomas J. Daley, J.D.
"""
import json
import math
import re


class CsModals(object):
    @staticmethod
    def param_modal(trigger_id: str) -> dict:
        return CsModals.load_view('cs_params_view', trigger_id)

    @staticmethod
    def good_response_modal(trigger_id: str) -> dict:
        return CsModals.load_view('cs_good_response', trigger_id)

    @staticmethod
    def load_view(modal_name: str, trigger_id: str) -> dict:
        """
        Return dict that specifies a modal dialog to retrieve
        input parameters to compute child support.

        Args:
            modal_name (str): Portion of the file's name
            trigger_id (str): Received from interaction.

        Returns:
            (dict): Slack modal dialog specification
        """
        with open(f'./modals/views/{modal_name}.json', 'r') as fp:
            view = json.load(fp)
        return {
            'trigger_id': trigger_id,
            'view': view
        }

    @staticmethod
    def calculate_child_support(user_data: dict) -> dict:
        """
        Compute Texas Guideline Child Support.
        """
        net_resources_cap = 9200.0 * 12.0
        clean_data(user_data)
        user_data['gross_income_annual'] = user_data['income_amount'] * user_data['income_frequency']
        user_data['medical_annual'] = user_data['medical_amount'] * user_data['insurance_frequency']
        user_data['dental_annual'] = user_data['dental_amount'] * user_data['insurance_frequency']
        user_data['union_dues_annual'] = user_data['union_dues_amount'] * user_data['union_dues_frequency']
        user_data['social_sec_annual'] = social_security(user_data)
        user_data['medicare_annual'] = medicare(user_data)
        user_data['income_tax_annual'] = federal_income_tax(user_data)
        user_data['net_resources_annual'] = annual_net_resources(user_data)
        user_data['support_factor'] = support_factor(user_data)
        user_data['child_support_annual'] = min(user_data['net_resources_annual'], net_resources_cap) * user_data['support_factor']
        scale_numbers(user_data)
        print(json.dumps(user_data, indent=4))


def round_up(number, decimals: int = 2) -> float:
    factor = int('1' + ('0' * decimals))
    return math.ceil(number * factor) / factor


def scale_numbers(user_data: dict):
    fields = [
        'gross_income_annual', 'medical_annual', 'dental_annual', 'union_dues_annual',
        'social_sec_annual', 'medicare_annual', 'income_tax_annual', 'net_resources_annual',
        'child_support_annual'
    ]

    for field in fields:
        user_data[field] = round_up(user_data[field])
        month_key = field.replace('_annual', '_monthly')
        user_data[month_key] = round_up(user_data[field] / 12.0)


def support_factor(user_data: dict):
    factors = [
        [],
        [.2, .175, .16, .1475, .1360, .1333, .1314, .13],
        [.25, .225, .2063, .19, .1833, .1786, .175, .1722],
        [.3, .2738, .2520, .24, .2314, .225, .22, .216],
        [.35, .322, .3033, .29, .28, .2722, .266, .2609],
        [.4, .3733, .3543, .34, .3289, .32, .3127, .3067],
        [.4, .3771, .36, .3467, .336, .3273, .32, .3138],
        [.4, .38, .3644, .352, .3418, .3333, .3262, .32]
    ]
    children_in = min(user_data['children_inside'], len(factors)-1)
    children_out = min(len(factors[children_in])-1, user_data['children_outside'])
    return factors[children_in][children_out]


def annual_net_resources(user_data: dict):
    return user_data['gross_income_annual'] - \
           user_data['medical_annual'] - \
           user_data['dental_annual'] - \
           user_data['union_dues_annual'] - \
           user_data['social_sec_annual'] - \
           user_data['medicare_annual'] - \
           user_data['income_tax_annual']


def federal_income_tax(user_data):
    personal_exemption = 0.0  # Until 2025
    standard_deduction = 12400.0
    gross = user_data['gross_income_annual'] - personal_exemption - standard_deduction

    if user_data['self_employed']:
        gross -= user_data['social_sec_annual'] / 2
        gross -= user_data['medicare_annual'] / 2

    if gross >= 518400.0:
        return 156235.0 + .37 * max(gross-518400.0, 0.0)

    if gross >= 207351.0:
        return 47367.5 + .35 * max(gross-207350.0, 0.0)

    if gross >= 163301.0:
        return 33217.5 + .32 * max(gross-163300.0, 0.0)

    if gross >= 85526.0:
        return 14605.5 + .24 * max(gross-85525.0, 0.0)

    if gross >= 40126.0:
        return 4617.5 + .22 * max(gross-40125.0, 0.0)

    if gross >= 9876.0:
        return 987.5 + .12 * max(gross-9875.0, 0.0)

    return .1 * gross


def social_security(user_data):
    social_sec_rate_emp = .062
    social_sec_rate_self = .124
    max_social_sec_wages = 137700.0
    self_employment_factor = .9235

    if user_data['self_employed']:
        taxable_income = min(user_data['gross_income_annual'] * self_employment_factor, max_social_sec_wages)
        return taxable_income * social_sec_rate_self
    taxable_income = min(user_data['gross_income_annual'], max_social_sec_wages)
    return taxable_income * social_sec_rate_emp


def medicare(user_data):
    medicare_rate_emp = .0145
    medicare_rate_self = .029
    self_employment_factor = .9235

    if user_data['self_employed']:
        taxable_income = user_data['gross_income_annual'] * self_employment_factor
        return taxable_income * medicare_rate_self
    return user_data['gross_income_annual'] * medicare_rate_emp


def clean_data(user_data: dict):
    supply_defaults(user_data)
    edit_data(user_data)
    convert_types(user_data)


def edit_data(user_data: dict):
    user_data['income_amount'] = user_data['income_amount'] \
                                 .replace('$', '') \
                                 .replace(',', '') \
                                 .strip()
    user_data['medical_amount'] = user_data['medical_amount'] \
                                 .replace('$', '') \
                                 .replace(',', '') \
                                 .strip()
    user_data['dental_amount'] = user_data['dental_amount'] \
                                 .replace('$', '') \
                                 .replace(',', '') \
                                 .strip()
    user_data['union_dues_amount'] = user_data['union_dues_amount'] \
                                 .replace('$', '') \
                                 .replace(',', '') \
                                 .strip()
    user_data['children_inside'] = user_data['children_inside'].strip()
    user_data['children_outside'] = user_data['children_outside'].strip()


def convert_types(user_data):
    types = {
        'income_frequency': int,
        'insurance_frequency': int,
        'self_employed': bool,
        'union_dues_frequency': int,
        'income_amount': float,
        'medical_amount': float,
        'dental_amount': float,
        'children_inside': int,
        'children_outside': int,
        'union_dues_amount': float
    }

    for key, value in user_data.items():
        if types.get(key) == int:
            user_data[key] = int(value)
            continue
        if types.get(key) == bool:
            user_data[key] = value.upper() == 'YES'
            continue
        if types.get(key) == float:
            user_data[key] = float(value)
            continue


def supply_defaults(user_data):
    defaults = {
        'income_frequency': "12",
        'insurance_frequency': "12",
        'self_employed': "NO",
        'union_dues_frequency': "12",
        'income_amount': "1300",
        'medical_amount': "0",
        'dental_amount': "0",
        'children_inside': "1",
        'children_outside': "0",
        'union_dues_amount': "0"
    }
    # Supply defaults for extant keys with missing values
    for key, value in user_data.items():
        if not value or value == '':
            user_data[key] = defaults.get(key, None)

    # Supply defaults for missing keys
    for key, value in defaults.items():
        if key not in user_data:
            user_data[key] = value
