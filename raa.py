from flask import Flask, Blueprint, request, abort, make_response, jsonify, g
from flask_restplus import Api, Resource
from flask_cors import CORS

from models.response_models import *
from models.error import InvalidUsage
from parse.headers_params import *
#from models.name import NaamError
#from models.name_collection import NameCollection

from settings import server_config

app = Flask(__name__, static_url_path='', static_folder='public')
app.config['SECRET_KEY'] = "some combination of key words"
cors = CORS(app)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc="/docs")

----------

from flask import Flask, Blueprint, request, abort, make_response, jsonify, g
from flask_restplus import Api, Resource
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from config import get_config
from models import *
from query import *
from models.response_models import *
from models.error import InvalidUsage
from parse.headers_params import *


from settings import server_config

app = Flask(__name__, static_url_path='', static_folder='public')
#app.config['SECRET_KEY'] = "some combination of key words"
app.config['SQLALCHEMY_DATABASE_URI'] = get_config(host="local")['SQLALCHEMY_DATABASE_URI']
cors = CORS(app)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc="/docs")

Base = automap_base()
Base.prepare(db.engine, reflect=True)


@app.route('/regent/<int:regent_id>')


@app.route('/')
def index():
    #new_product = Product(name='New Product', price=50, monthly_goal=1000)
    #db.session.add(new_product)
    #db.session.commit()

    results = db.session.query(regent).all()
    lst_results = [Persoon(r).fullname() for r in results]
    return(jsonify(lst_results))




#search simple field
@api.doc(params={'search_field': 'field name',
                 'search_term': 'search string'}, required=False)
@api.route("/search/simple", endpoint='simple_search')
class PersonNameSimpleSearchAPI(Resource):
    @api.response(200, 'Success', name_response)
    @api.response(404, 'No input?')

    def _handle_request(self, params):
        fieldname = params['filter']['field_name']
        searchterm = params['filter']['search_term']
        body = name_store.simple(field=fieldname, condition=searchterm)
        names = name_store.query(index='namenindex',
                                doc_type='naam',
                                body=body
                )
        response_data = names['hits']
        return jsonify(response_data)

    def post(self):
        params = get_params(request)
        result = self._handle_request(params)
        return result


    def get(self):
        params = get_params(request)
        result = self._handle_request(params)
        return result


    #order_count = db.session.query(Order).join(Product).filter(Product.id == 2).count()
    #print(order_count)

    return ''
