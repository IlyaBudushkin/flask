from flask import jsonify
import json
import psycopg2

from config import *

def get_db_connection():
    conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
        )
    return conn



def get_product_type(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        type_id = data.get('type_id')

        query = "SELECT type_name FROM product_type WHERE product_type_id = %s"
        cursor.execute(query, (type_id,))
        type = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({'type': type[0]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



def set_product_type(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    type_name = data.get('type_name')

    query = "SELECT product_type_id FROM product_type WHERE type_name = %s"
    cursor.execute(query, (type_name,))
    product_type_id = cursor.fetchone()
    if not product_type_id:
        insert_query = "INSERT INTO product_type (type_name) VALUES (%s)"
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



def set_product(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
                INSERT INTO products (product_type_id, prod_status_id , description, date_of_creating, 
                         name, photo) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
        type_name = data.get('type_name')
        query = "SELECT product_type_id FROM product_type WHERE type_name = %s"
        cursor.execute(query, (type_name,))
        product_type_id = cursor.fetchone()
        if not product_type_id:
            return jsonify({'error': 'No product type'}), 401

        prod_status = data.get('product_status')
        query = "SELECT prod_status_id FROM product_status WHERE status = %s"
        cursor.execute(query, (prod_status,))
        product_status_id = cursor.fetchone()
        if not product_status_id:
            return jsonify({'error': 'No product type'}), 401

        cursor.execute(insert_query, (
            product_type_id,
            product_status_id,
            data['description'],
            data['date_of_creating'],
            data['name'],
            data['photo']))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Data added successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



def set_shopping_list(data):
    if not data:
        return jsonify({'error': 'No data provided'}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        product_name = data.get('product_name')#fk
        user_name = data.get('user_name')#fk

        insert_query = """
            INSERT INTO shopping_list (user_id, products_id)
            VALUES (%s, %s)
            """

        query = "SELECT products_id FROM products WHERE name = %s"
        cursor.execute(query, (product_name,))
        type_id = cursor.fetchone()
        if not type_id:
            return jsonify({'error': 'No types of measurements found'}), 401

        query = "SELECT user_id FROM users WHERE name = %s"
        cursor.execute(query, (user_name,))
        user_id = cursor.fetchone()
        if not user_id:
            return jsonify({'error': 'No user_name found'}), 401


        cursor.execute(insert_query, (
                                    user_id,
                                    type_id))
        conn.commit()

        return jsonify({'message': 'Data added successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()



# def get_measurement(data):
#     if not data:
#         return jsonify({'error': 'No data provided'}), 401
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#
#         query = "SELECT * FROM list_of_measurements WHERE user_id = %s"
#         cursor.execute(query, (data['user_id'],))
#         measurements = cursor.fetchall()
#
#         cursor.close()
#         conn.close()
#
#         if measurements:
#             return jsonify({'measurements': measurements}), 200
#         else:
#             return jsonify({'error': 'User has no measurements'}), 401
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500



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



def get_calls_list(data,metod):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if metod == 'get':
            query = ("SELECT requests_for_a_call.id, "
                     "requests_for_a_call.user_id, "
                     "requests_for_a_call.name, "
                     "requests_for_a_call.phone_number, "
                     "requests_for_a_call.date_of_application_processing, "
                     "requests_for_a_call.application_date, "
                     "requests_for_a_call.qestion, "
                     "call_statuses.status AS call_status "
                     "FROM requests_for_a_call "
                     "JOIN call_statuses ON requests_for_a_call.call_status_id = call_statuses.call_status_id")
            cursor.execute(query)
            list_of_requests = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify({'list_of_requests': list_of_requests}), 200
        else:
            if not data:
                return jsonify({'error': 'No data provided'}), 401
            query = """SELECT 
                           requests_for_a_call.id, 
                           requests_for_a_call.user_id, 
                           requests_for_a_call.name, 
                           requests_for_a_call.phone_number, 
                           requests_for_a_call.date_of_application_processing, 
                           requests_for_a_call.application_date, 
                           requests_for_a_call.qestion, 
                           call_statuses.status AS call_status 
                       FROM 
                           requests_for_a_call 
                       JOIN 
                           call_statuses ON requests_for_a_call.call_status_id = call_statuses.call_status_id 
                       WHERE 
                           requests_for_a_call.id = %s"""

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