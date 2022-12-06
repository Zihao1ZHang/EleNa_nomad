from flask import Flask, request, jsonify
from flask_cors import CORS
from Route_Algorithm import find_route
app = Flask(__name__)
CORS(app)


@app.route('/get_route', methods=['POST'])
def get_route():
    content = request.get_json()

    source = content['Source']
    dest = content['Destination']
    min_max = content['Min_max']
    percent = content['Percentage']
    print(source)
    print(dest)
    print(min_max)
    print(percent)
    route = find_route(source, dest, min_max, percent)

    response = jsonify({'Route': route})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/')
def hello_world():
    return "Hello world"


if __name__ == '__main__':
    print("start server at 127.0.0.1:8080")
    app.run(host="127.0.0.1", port=8080, debug=True)
