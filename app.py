from flask import Flask
from flask_restful import Api, Resource, reqparse
from neo4j import GraphDatabase

app = Flask(__name__)
api = Api(app)
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "testingtesting"))

print(driver)

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
        parser = reqparse.RequestParser()
        parser.add_argument('Names', required=True)
        args = parser.parse_args()
        names = args['Names']

        neighbors = { getNeighbors(n) for n in names }

        intersection = set(names) & neighbors

        return {'valid': not intersection, 'intersection' : intersection}, 201



api.add_resource(NodeResource, '/nodes')
api.add_resource(Neighbors, '/neighbors')
api.add_resource(Neighbors, '/valid')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
