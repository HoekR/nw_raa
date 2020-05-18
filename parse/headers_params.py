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
    """do we want this in the filter and we make a default allowed """
    params['filter'] = {}
    if request.args:
        reqob = request.args
    elif request.form:
        reqob = request.form
    else:
        reqob = {}
    #print(reqob, list(reqob.keys()))
    for key in reqob.keys():
        params["filter"][key] = reqob.get(key)
    #print("!", params)
    #return params