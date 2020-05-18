from flask import Flask, Blueprint, request, abort, make_response, jsonify, g
from flask_restx import Api, Resource
from flask_cors import CORS
from .query.query import *
from .models.models import *
from .models.response_models import *
from .models.error import InvalidUsage
from .parse.headers_params import *
from .config import default_preferences

preferences = default_preferences # customize with cookies/session

from .get_db import db, app
cors = CORS(app)
blueprint = Blueprint('api', __name__, url_prefix="/api")
api = Api(app)


"""--------------- Error handling -----------------------"""
@api.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    return error.to_dict(), error.status_code

# @api.errorhandler(NaamError)
# def handle_Name_error(error):
#     return error.to_dict(), error.status_code


"""--------------- endpoints ------------------"""

#api endpoint
@api.route("/", endpoint='api_base')
class BasicAPI(Resource):
    @api.doc('basic api access point for raa')
    @api.response(200, 'Success') #, person_response)
    @api.response(404, 'Nameindex Error')
    def get(self):
        """This is the repertory of officeholders server"""
        return {"message": "raa server v0.1 online"}


#get name by id
@api.doc(params={'regent_id': 'A Name ID'}, required=False)
@api.route("/regent/<int:regent_id>", endpoint='regent_base')
class RegentByIdAPI(Resource):
    @api.doc('raa regent by id')
    @api.response(200, 'Success', person_response)
    @api.response(404, 'Name does not exist')
    def get(self, regent_id):
        results = get_regent_by_id(db.session, regent_id)
        response_data = Persoon(results).repr() # get requests only return a single results
        return jsonify(response_data)

    def put(self):
        """not implemented"""
        pass

#search simple field
@api.doc(params={'search_term': 'search string',
                 'fuzzy': 'toggle fuzzy search (like)'},
         required=False)
@api.route("/regent/simple_search", endpoint="regent_simple_search")
class RegentNameSimpleSearchAPI(Resource):
     @api.response(200, 'Success', person_response)
     @api.response(404, 'No input?')

     def _handle_request(self, params):
         searchterm = params['filter']['search_term']
         #fuzzy = params['filter']['fuzzy']
         results = query_regent_name(db.session, qs=searchterm)
         response_data = [Persoon(r).repr() for r in results]
         return jsonify(response_data)

     def post(self):
         params = get_params(request)
         result = self._handle_request(params)
         return result


     def get(self):
         params = get_params(request)
         result = self._handle_request(params)
         return result

#get aanstelling by id
@api.doc(params={'aanstelling_id': 'An aanstelling ID'}, required=False)
@api.route("/aanstelling/<int:aanstelling_id>", endpoint='aanstelling_base')
class RegentByIdAPI(Resource):
    @api.doc('raa aanstelling by id')
    @api.response(200, 'Success', aanstelling_response)
    @api.response(404, 'Name does not exist')
    def get(self, aanstelling_id):
        results = get_aanstelling_by_id(db.session, aanstelling_id)
        response_data = [Aanstelling(r).repr() for r in results]
        return jsonify(response_data)

    def put(self):
        """not implemented"""
        pass

#search Aanstelling
@api.doc(params={'start_year_search_value': 'search string',
                 'start_year': 'field name',
                 'end_year_search_value': 'search string',
                 'end_year': 'field name'
                 },
         required=False)
@api.route("/aanstelling/period", endpoint="aanstelling_simple_search")

class AanstellingSimpleSearchAPI(Resource):
      @api.response(200, 'Success', aanstelling_response)
      @api.response(404, 'No input?')

      def _handle_request(self, params):
          print(params)
          startyear = params['filter'].get('start_year') or 1576
          startyear = int(startyear)
          endyear = params['filter'].get('end_year') or 1862
          endyear = int(endyear)
          results = q_aanstelling_onyrs(db.session, bj=startyear, ej=endyear)
          page = params['filter'].get('page') or 1
          if page: # factor this out into separate handler?
              pages = results.paginate(per_page=preferences['perpage'])
              results = pages.items
          response_data = [Aanstelling(r).repr() for r in results]
          return jsonify(response_data)

      def post(self):
          params = get_params(request)
          result = self._handle_request(params)
          return result


      def get(self):
          params =  get_params(request)
          result = self._handle_request(params)
          return result

#get college
@api.doc(params={'college_id': 'college ID'}, required=False)
@api.route("/college/<int:college_id>", endpoint='college_base')
class CollegeByIdAPI(Resource):
    @api.doc('raa college by id')
    @api.response(200, 'Success', college_response)
    @api.response(404, 'Name does not exist')
    def get(self, college_id):
        results = get_college_by_id(db.session, college_id)
        response_data = College(results).repr()
        return jsonify(response_data)

    def put(self):
        """not implemented"""
        pass


#get collegenamen

@api.doc(params={'period': 'period_id'},
          required=False)
@api.route("/colleges", endpoint="all_colleges_names")
class CollegeNames(Resource):
     @api.doc('raa all college names')
     @api.response(200, 'Success', college_response)
     @api.response(404, 'no college names')
     def _handle_request(self, params):
         period = params['filter'].get('period') or -1
         period = int(period)
         results = get_college_names(db.session, period=period)
         results = results.order_by("naam")
         response_data = [r.naam for r in results]
         return jsonify(response_data)

     def post(self):
         params = get_params(request)
         result = self._handle_request(params)
         return result

     def get(self):
         params = get_params(request)
         result = self._handle_request(params)
         return result


# get function names

@api.doc(params={'period': 'period_id'},
          required=False)
@api.route("/functions", endpoint="all_function_names")
class FunctionNames(Resource):
     @api.doc('raa all function names')
     @api.response(200, 'Success', function_response)
     @api.response(404, 'no college names')
     def _handle_request(self, params):
         period = params['filter'].get('period') or -1
         period = int(period)
         results = get_function_names(db.session, period=period)
         results = results.order_by("naam")
         response_data = [r.naam for r in results]  # no wrappers here
         return jsonify(response_data)

     def post(self):
         params = get_params(request)
         result = self._handle_request(params)
         return result

     def get(self):
         params = get_params(request)
         result = self._handle_request(params)
         return result


# get period names

@api.doc(params=dict(),
          required=False)
@api.route("/periods", endpoint="all_period_names")
class FunctionNames(Resource):
     @api.doc('raa all period names')
     @api.response(200, 'Success', period_response)
     @api.response(404, 'no period names')
     def _handle_request(self, params):
         results = get_period_names(db.session)
         results = results.order_by("naam")
         response_data = [r.naam for r in results.all()]  # no wrappers here
         return jsonify(response_data)

     def post(self):
         params = get_params(request)
         result = self._handle_request(params)
         return result

     def get(self):
         params = get_params(request)
         result = self._handle_request(params)
         return result