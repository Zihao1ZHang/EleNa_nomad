from flask import Flask, request, jsonify
from flask_cors import CORS
from Route_Algorithm import *
app = Flask(__name__)
CORS(app)


@app.route('/get_route', methods=['POST'])
def get_route():
    content = request.get_json()
    # print(content)
    source = content['Source']
    dest = content['Destination']
    is_max = content['Is_max']
    percent = content['Percentage']
    # print(source)
    # print(dest)
    # <option>Shortest route</option>
    # <option>Max elevation</option>
    #     <option>Min elevation</option>
    method = "A"
    if is_max == "Shortest route":
        method = 'S'
    elif is_max == "Max elevation":
        is_max = True
    else:
        is_max = False
    route = find_route(source, dest, method=method,
                       percentage=float(percent)/100, is_max=is_max)
    response = jsonify({'Route': route})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/')
def hello_world():
    return "Hello world"


if __name__ == '__main__':
    print("start server at 127.0.0.1:8080")
    app.run(host="127.0.0.1", port=8080, debug=True)
