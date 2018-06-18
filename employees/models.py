# -*- coding: utf-8 -*-
from tangent_core.model_facade import ModelFacade

"""
    RACE_GROUPS
    will almost never change - so treat as constants
"""
RACE_GROUPS = {
    'B': "Black",
    'C': 'Coloured',
    'I': 'Indian or Asian',
    'W': 'White',
    'N': 'None Dominant'
}


class Employee(ModelFacade):
    """
    Create our API model which will extend
    ModelFacade.

    Since we're using our custom API model we don't
    need to setup properties like we normally do in django.
    """
    pass
