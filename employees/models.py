# -*- coding: utf-8 -*-
from tangent_core.model_facade import ModelFacade

"""
	Create our API model which will extend
	ModelFacade.

    Since we're using our custom API model we don't
    need to setup properties like we normally do in django.
"""
class Employee(ModelFacade):
	pass