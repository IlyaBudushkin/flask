from flask import Flask, request
from controller import *


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


@app.route('/delete_calldelete_call', methods=['DELETE'])
def delete_call():
    data = request.get_json()
    return delete_request_of_call(data)


@app.route('/call_status_update', methods=['POST'])
def call_status_update():
    data = request.get_json()
    return call_status_updating(data)


@app.route('/get_call', methods=['GET','POST'])
def get_call():
    if request.method == 'GET':
        return get_calls_list(data=None,metod='get')
    else:
        data = request.get_json()
        return get_calls_list(data,'post')


@app.route('/get_type', methods=['POST'])
def get_type():
    data = request.json
    return get_product_type(data)


@app.route('/set_type', methods=['POST'])
def set_type():
    data = request.json
    return set_product_type(data)


@app.route('/set_shopping_list', methods=['POST'])
def set_shopping():
    data = request.get_json()
    return set_shopping_list(data)


# @app.route('/get_mej', methods=['POST'])
# def get_mej():
#     data = request.get_json()
#     return get_measurement(data)


@app.errorhandler(404)
def page_not_found(e):
    return json.loads(json.dumps({"error": "404 Not Found"}))


if __name__ == '__main__':
    app.run(debug=True)