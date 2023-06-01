
from flask import Flask, redirect, send_from_directory
from flask_restful import Api
from flask_cors import CORS
from mongoengine import connect
from config import config
from flask_swagger_ui import get_swaggerui_blueprint

from modules.country import Countries
from modules.crops import Crops, Groups
from modules.accessions import AccessionsByIDCrop, AccessionsByIDGroup

app = Flask(__name__)
CORS(app)
api = Api(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Gap Analysis Web API"}
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route('/')
def home():
    return redirect("/swagger")

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)

api.add_resource(Countries, '/api/v1/countries')
api.add_resource(Crops, '/api/v1/crops')
api.add_resource(Groups, '/api/v1/groups')
api.add_resource(AccessionsByIDCrop, '/api/v1/accessionsbyidcrop')
api.add_resource(AccessionsByIDGroup, '/api/v1/accessionsbyidgroup')



if __name__ == '__main__':
    connect(host=config['CONNECTION_DB'])
    print("Connected DB")
    
    app.run(threaded=True, host=config['HOST'], port=config['PORT'], debug=config['DEBUG'])
