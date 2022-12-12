from flask import Flask, request, jsonify
from flask_cors import CORS
from Route_Algorithm import *
from model.Route import Route
app = Flask(__name__)
CORS(app)


@app.route('/get_route', methods=['POST'])
def get_route():
    # process the json file
    content = request.get_json()
    source = content['Source']
    dest = content['Destination']
    is_max = content['Is_max']
    percent = content['Percentage']

    method = ''
    if is_max == "Shortest route":
        method = 'S'
    elif is_max == "Max elevation":
        is_max = True
    else:
        is_max = False

    # run the routing algortihm
    route = find_route(source, dest, method=method,
                       percentage=float(percent)/100, is_max=is_max)

    # create json file and send response to client
    response = jsonify({'Route': route.path})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/')
def hello_world():
    return "Client address: localhost:3000"


if __name__ == '__main__':
    print("start server at 127.0.0.1:8080")
    app.run(host="127.0.0.1", port=8080, debug=True)
