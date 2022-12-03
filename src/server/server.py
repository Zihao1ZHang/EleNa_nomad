from flask import Flask, request, jsonify
from flask_cors import CORS
from Route_Algorithm import find_route
app = Flask(__name__)
CORS(app)


@app.route('/get_route', methods=['POST'])
def get_route():
    content = request.get_json()

    source = content['source']
    dest = content['destination']
    min_max = content['Min_max']
    percent = content['Percentage']
    print(source)
    print(dest)
    print(min_max)
    print(percent)
    route, dist, elevation = find_route(source, dest, min_max, percent)

    response = jsonify({'Route': route, "Distance": dist,
                       "Elevation Gain": elevation})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/')
def hello_world():
    return "Hello world"


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)
