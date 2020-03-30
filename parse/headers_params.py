from flask import g
from models.error import InvalidUsage, PermissionError

"""--------------- Parse Request Headers and Parameters ------------------"""

def get_params(request, anon_allowed=True):
    print ('request:', request)
    params = {}
    parse_search_parameters(request, params)
    return params

"""--------------- Parse Request Headers ------------------"""

def interpret_header(headers, params):
    return params

#def parse_prefer_header(headers):
#    prefer = {}
#    if not headers.get("Prefer"):
#        return prefer
#    for part in headers.get("Prefer").strip().split(";"):
#        key, value = part.split("=")
#        prefer[key] = value.strip('"').strip("'")
#    if "return" in prefer and prefer["return"] == "representation":
#        prefer["view"] = prefer["include"].split("#")[1]
#    return prefer
#
# do we need a view???
#def determine_view_preference(headers):
#    default_view = "PreferMinimalContainer"
#    prefer = parse_prefer_header(headers)
#    return prefer["view"] if "view" in prefer else default_view

"""--------------- Parse Request Parameters ------------------"""

def parse_search_parameters(request, params):
    """do we want this in the filter"""
    params['filter'] = {}
    if request.args:
        reqob = request.args
    elif request.form:
        reqob = request.form
    print(reqob)
    if reqob.get("field_name"):
        params["filter"]["field_name"] = reqob.get("field_name")
    if reqob.get("search_term"):
        params["filter"]["search_term"] = reqob.get("search_term")
