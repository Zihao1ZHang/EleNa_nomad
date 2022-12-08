from flask import Flask, request, jsonify
from flask_cors import CORS
from Route_Algorithm import *
app = Flask(__name__)
CORS(app)


@app.route('/get_route', methods=['POST'])
def get_route():
    content = request.get_json()
    print(content)
    source = content['Source']
    dest = content['Destination']
    min_max = content['Min_max']
    percent = content['Percentage']
    print(source)
    print(dest)
    print(min_max)
    print(percent)
    route1, r1_length, elevation1 = find_route(
        source, dest, place="Amherst, Massachusetts, USA")
    route2, r2_length, elevation2 = Astar(
        source, dest, 1, r1_length*1.1, place="Amherst, Massachusetts, USA")
    response = jsonify({'Route': route2})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/')
def hello_world():
    return "Hello world"


if __name__ == '__main__':
    print("start server at 127.0.0.1:8080")
    app.run(host="127.0.0.1", port=8080, debug=True)
