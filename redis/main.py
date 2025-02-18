from flask import Flask, request
from create_redis_db import *


app = Flask(__name__)
app.config['SECRET_KEY'] = '<KEY>'


@app.route('/register', methods=['GET', 'POST'])
def register():
    data = request.json
    return set_user(data)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return get_user(data)



@app.route('/set_call', methods=['POST'])
def set_call():
    data = request.get_json()
    return set_data_for_call(data)


@app.route('/delete_call', methods=['DELETE'])
def delete_call():
    data = request.get_json()
    return delete_request_of_call(data)


@app.route('/get_call', methods=['GET', 'POST'])
def get_call():
    if request.method == 'GET':
        return get_calls_list(data=None,metod='get')
    else:
        data = request.get_json()
        return get_calls_list(data, 'post')


@app.errorhandler(404)
def page_not_found(e):
    return json.loads(json.dumps({"error": "404 Not Found"}))


if __name__ == '__main__':
    app.run(debug=True)