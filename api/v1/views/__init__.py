#!/usr/bin/python3
"""
creating the blueprint package
"""
from flask import Blueprint


app_views = Blueprint("app_view", __name__, url_prefix="/api/v1")


from api.v1.views.index import *
#from api.v1.view.states import *
#from api.v1.view.cities import *
#from api.v1.view.amenities import *
#from api.v1.view.index import *
#from api.v1.view.index import *
#from api.v1.view.index import *
#from api.v1.view.index import *
