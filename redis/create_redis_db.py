import redis
from flask import jsonify
import json

def connect_to_redis():
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    return redis_client


def set_user(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        redis_client = connect_to_redis()
        fullname = data['name'] + data['lastname'] + data['surname']
        redis_client.lpush('users', fullname)
        redis_client.hset(fullname, mapping={
                        'name': data['name'],
                        'lastname': data['lastname'],
                        'surname': data['surname'],
                        'email': data['email'],
                        'phone': data['phone_number'],
                        'password': data['password']})

        redis_client.close()
        return jsonify({'message': 'Data added successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_user(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        redis_client = connect_to_redis()

        list_length = redis_client.llen('users')
        values = []
        for i in range(list_length):
            value = redis_client.lindex('users', i)
            values.append(value.decode('utf-8'))

        for i in values:
            email = redis_client.hget(i, 'email')
            password = redis_client.hget(i, 'password')

            if email.decode('utf-8') == data['email'] and password.decode('utf-8') == data['password']:
                name = redis_client.hget(i, 'name')
                lastname = redis_client.hget(i, 'lastname')
                surname = redis_client.hget(i, 'surname')
                phone = redis_client.hget(i, 'phone')

                data_json = {
                        'name': name.decode('utf-8'),
                        'lastname': lastname.decode('utf-8'),
                        'surname': surname.decode('utf-8'),
                        'email': email.decode('utf-8'),
                        'phone': phone.decode('utf-8'),
                        'password': password.decode('utf-8')}
                redis_client.close()
                return jsonify({'message': 'Login successful', 'user': data_json}), 200

        redis_client.close()
        return jsonify({'error': 'Email or password incorrect'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def set_data_for_call(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        redis_client = connect_to_redis()

        redis_client.lpush('calls', data['phone_number'])
        redis_client.hset(data['phone_number'], mapping={
            'name': data['name'],
            'phone': data['phone_number'],
            'qestion': data['qestion'],})
        redis_client.close()
        return jsonify({'message': 'Data added successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def delete_request_of_call(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        redis_client = connect_to_redis()

        redis_client.lrem('calls', 1, data['phone_number'])
        redis_client.delete(data['phone_number'])

        redis_client.close()
        return jsonify({'message': 'Data deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_calls_list(data,metod):
    if metod == 'get':
        try:
            redis_client = connect_to_redis()
            list_length = redis_client.llen('calls')
            values = []

            for i in range(list_length):
                value = redis_client.lindex('calls', i)
                values.append(value.decode('utf-8'))

            merged_data = {}
            for i in values:
                hash_data = redis_client.hgetall(i)
                hash_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in hash_data.items()}
                merged_data[i] = hash_data

            redis_client.close()
            return jsonify({'list_of_calls': merged_data}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        if not data:
            return jsonify({'error': 'No data provided'}), 401
        try:
            redis_client = connect_to_redis()
            list_length = redis_client.llen('calls')
            values = []

            for i in range(list_length):
                value = redis_client.lindex('calls', i)
                values.append(value.decode('utf-8'))

            for i in values:
                hash_data = redis_client.hgetall(i)
                hash_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in hash_data.items()}

                if hash_data.get('phone') == data['phone_number']:
                    redis_client.close()
                    return jsonify({'message': hash_data}), 200

            redis_client.close()
            return jsonify({'message': 'No such phone_number'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
