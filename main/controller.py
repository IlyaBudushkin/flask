from flask import jsonify
import json
import psycopg2

from config_db import *

def get_db_connection():
    conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
        )
    return conn



def get_measurement_type(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        type_id = data.get('type_id')

        query = "SELECT type_name FROM types_of_measurements WHERE type_id = %s"
        cursor.execute(query, (type_id,))
        type = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({'type': type[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



def set_measurement_type(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    type_name = data.get('type_name')

    query = "SELECT type_id FROM types_of_measurements WHERE type_name = %s"
    cursor.execute(query, (type_name,))
    type_id = cursor.fetchone()
    if not type_id:
        insert_query = "INSERT INTO types_of_measurements (type_name) VALUES (%s)"
        cursor.execute(insert_query, (type_name,))
        conn.commit()
        cursor.close()
        conn.close()
        try:
            return jsonify({'type_id': 'new type added'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Type already exists'}), 400



def set_user(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
                INSERT INTO users (name, surname , lastname, phone_number, 
                         email, password, date_of_creating) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

        cursor.execute(insert_query, (
            data['name'],
            data['surname'],
            data['lastname'],
            data['phone_number'],
            data['email'],
            data['password'],
            data['date_of_creating']))
        conn.commit()

        return jsonify({'message': 'Data added successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()



def get_user(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 401

    # Подключаемся к базе данных
    conn = get_db_connection()
    cursor = conn.cursor()

    # Выполняем запрос для проверки учетных данных
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({'message': 'Login successful', 'user': user}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401



def set_measurement(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        measurement_types = data.get('types_of_measurements')#fk
        user_name = data.get('user_name')#fk
        productStatus = data.get('product_status')#fk

        insert_query = """
            INSERT INTO list_of_measurements (type_id , user_id, prod_status_id, 
                     point_of_measurement, description, date_of_creating,name,report_1,report_2) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

        query = "SELECT type_id FROM types_of_measurements WHERE type_name = %s"
        cursor.execute(query, (measurement_types,))
        type_id = cursor.fetchone()
        if not type_id:
            return jsonify({'error': 'No types of measurements found'}), 401

        query = "SELECT user_id FROM users WHERE name = %s"
        cursor.execute(query, (user_name,))
        user_id = cursor.fetchone()
        if not user_id:
            return jsonify({'error': 'No user_name found'}), 401

        query = "SELECT prod_status_id FROM product_status WHERE status = %s"
        cursor.execute(query, (productStatus,))
        product_status_id = cursor.fetchone()
        if not product_status_id:
            return jsonify({'error': 'No product_status_id found'}), 401

        cursor.execute(insert_query, (
                                    type_id,
                                    user_id,
                                    product_status_id,
                                    data['point_of_measurement'],
                                    data['description'],
                                    data['date_of_creating'],
                                    data['name'],
                                    data['report_1'],
                                    data['report_2']))
        conn.commit()

        return jsonify({'message': 'Data added successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()



def get_measurement(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM list_of_measurements WHERE user_id = %s"
        cursor.execute(query, (data['user_id'],))
        measurements = cursor.fetchall()

        cursor.close()
        conn.close()

        if measurements:
            return jsonify({'measurements': measurements}), 200
        else:
            return jsonify({'error': 'User has no measurements'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500



def set_data_for_call(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = ("""
                 INSERT INTO requests_for_a_call(user_id,call_status_id, name, phone_number, date_of_application_processing, 
                            application_date, qestion) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)
                 """)

        cursor.execute(insert_query, (
            data['user_id'],
            1,
            data['name'],
            data['phone_number'],
            data['date_of_application_processing'],
            data['application_date'],
            data['qestion']))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Data added successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def call_status_updating(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT call_status_id FROM requests_for_a_call WHERE id = %s"
        cursor.execute(query, (data['id'],))
        call_status_id = cursor.fetchone()

        query = "SELECT MAX(call_status_id) FROM call_statuses"
        cursor.execute(query)
        max_id = cursor.fetchone()

        if call_status_id[0] < max_id[0]:
            new_status = call_status_id[0] + 1
            query = "UPDATE requests_for_a_call SET call_status_id = %s WHERE id = %s"
            cursor.execute(query, (new_status, data['id']))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'Data updated successfully'}), 200
        else:
            return jsonify({'error': 'No data provided'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500



def get_calls_list(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if data['person'] == 'all':
            query = "SELECT * FROM requests_for_a_call"
            cursor.execute(query)
            list_of_requests = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify({'list_of_requests': list_of_requests}), 200
        else:
            query = "SELECT * FROM requests_for_a_call WHERE id = %s"
            cursor.execute(query, (data['person'],))
            list_of_requests = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify({'list_of_requests': list_of_requests}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



def delete_request_of_call(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "DELETE FROM requests_for_a_call WHERE id = %s"
        cursor.execute(query, (data['id'],))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Data deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500