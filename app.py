from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, request
from neo4j import GraphDatabase
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "testingtesting"))

client = MongoClient("localhost:27017")
db = client['DrugID_NameMap']
collection = db['drug_map']

# https://www.biostars.org/p/271718/

def getNeighbors( node_name ):
    with driver.session() as session:
        result = session.run("MATCH (sourceNode {Name: $name})-[:INTERACTS_WITH]->(neighborNode) RETURN neighborNode", name=node_name)
        nodes = [record['neighborNode']['Name'] for record in result]
        return nodes

class NodeResource(Resource):
    def get(self):
        with driver.session() as session:
            result = session.run("MATCH (n) RETURN n")
            nodes = [record['n']['Name'] for record in result]
            return {'nodes': nodes}, 200

class Neighbors(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Name', required=True)
        args = parser.parse_args()
        node_name = args['Name']

        neighbors = getNeighbors(node_name)
        return {'neighbors': neighbors}, 201

class ValidMedication(Resource):
    def post(self):
        names = request.get_json()["Names"]
        neighbors = set()
        for n in names:
            query = { "synonym": n }
            result = collection.find_one(query)

            if not result:
                return {'error' : 'Invalid input. Please provide both name and age.'}, 400

            neighbors |=  set(getNeighbors(result["drug_id"]))

        intersection = [*(set(names) & neighbors)]
        return {'valid': not intersection, 'intersection' : intersection}, 201


api.add_resource(NodeResource, '/nodes')
api.add_resource(Neighbors, '/neighbors')
api.add_resource(ValidMedication, '/valid')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
