from flask import Flask
from flask_restful import Api, Resource, reqparse
from neo4j import GraphDatabase

app = Flask(__name__)
api = Api(app)
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "testingtesting"))

print(driver)

# https://www.biostars.org/p/271718/

class NodeResource(Resource):
    def get(self):
        with driver.session() as session:
            result = session.run("MATCH (n) RETURN n")
            nodes = [record['n']['Name'] for record in result]
            return {'nodes': nodes}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Name', required=True)
        args = parser.parse_args()
        node_name = args['Name']

        with driver.session() as session:
            result = session.run("MATCH (sourceNode {Name: $name})-[:INTERACTS_WITH]->(neighborNode) RETURN neighborNode", name=node_name)
            nodes = [record['neighborNode']['Name'] for record in result]
            return {'neighbors': nodes}, 201

api.add_resource(NodeResource, '/nodes')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
