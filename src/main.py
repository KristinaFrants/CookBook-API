"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
from models import Cooking

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200


@app.route('/recipes', methods=['POST','GET'])
def get_recipes():
    # get request
    if request.method == 'GET':
        all_recipe = Cooking.query.all()
        all_recipe = list(map(lambda x : x.serialize(), all_recipe))
        
        return jsonify(all_recipe), 200

    if request.method == 'POST':
        body = request.get_json() 
        if body is None:
            raise APIException("Specify JSON body", status_code=400)
        if "description" not in body:
            raise APIException("Specify description", status_code=400)
        if "email" not in body:
            raise APIException("Specify Email", status_code=400)

        recipes1 = Cooking(author = body['author'], email = body['email'], name = body['name'], description = body['description'], servings = body['servings'], cooktime = body['cooktime'], image = body['image'], cooktips = body['cooktips'], ingridients = body['ingridients'])
        db.session.add(recipes1)
        db.session.commit()


    
        return "ok", 200

    return "invalid method", 404

@app.route('/recipes/<int:cooking_id>', methods=['PUT','GET', 'DELETE'])
def get_single_recipe(cooking_id):
    #put request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("Specify JSON body", status_code=400)
        
        recipe1 = Cooking.query.get(cooking_id)
        if "description" in body:
            recipe1.description = body["description"]
        db.session.commit()
        
        return jsonify(recipe1.serialize()), 200
    
    #get request
    if request.method == "GET":
        recipe1 = Cooking.query.get(cooking_id)
        if recipe1 is None:
            raise APIException("Recipe Not Found", status_code=404)
        return jsonify(recipe1.serialize()), 200

    #delete request
    if request.method == 'DELETE':
        recipe1 = Cooking.query.get(cooking_id)
        if recipe1 is None:
            raise APIException("Recipe Not Found", status_code=404)
        db.session.delete(recipe1)
        db.session.commit()
        return "recipe deleted", 200

    return "invalid method", 404
    

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)