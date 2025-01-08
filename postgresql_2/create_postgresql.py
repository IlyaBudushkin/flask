import psycopg2
from config import host, user, db_name, password



try:
    connection = psycopg2.connect(
        dbname="postgres",
        user=user,
        password=password,
        host=host,
    )
    cursor = connection.cursor()
    connection.autocommit = True

    cursor.execute("CREATE DATABASE flask_postgre;")

    if connection:
        print("Connected close")
        cursor.close()
        connection.close()

    connection = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
    )
    cursor = connection.cursor()
    connection.autocommit = True


    cursor.execute(
        """CREATE TABLE IF NOT EXISTS roles (
                        role_id serial PRIMARY KEY,
                        user_role varchar(255) NOT NULL)""")

    cursor.execute("""INSERT INTO roles (user_role) VALUES (%s)""", ('user',))
    cursor.execute("""INSERT INTO roles (user_role) VALUES (%s)""", ('admin',))

    print("Table [roles] created successfully")



    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
                        user_id serial PRIMARY KEY,
                        name varchar(255) NOT NULL,
                        surname varchar(255) NOT NULL,
                        lastname varchar(255) NOT NULL,
                        role_id INT,
                        phone_number varchar(255) NOT NULL,
                        email varchar(255) NOT NULL,
                        password varchar(255) NOT NULL,
                        date_of_creating date NOT NULL,
                        FOREIGN KEY (role_id) REFERENCES roles(role_id))""")

    cursor.execute("""ALTER TABLE users DROP CONSTRAINT users_role_id_fkey""")

    print("Table [users] created successfully")

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS product_status (
                        prod_status_id serial PRIMARY KEY,
                        status varchar(255) NOT NULL)""")

    cursor.execute("""INSERT INTO product_status (status) VALUES (%s)""", ('status1',))
    cursor.execute("""INSERT INTO product_status (status) VALUES (%s)""", ('status2',))

    print("Table [product_status] created successfully")


    cursor.execute(
        """CREATE TABLE IF NOT EXISTS call_statuses (
                        call_status_id serial PRIMARY KEY,
                        status varchar(255) NOT NULL)""")

    cursor.execute("""INSERT INTO call_statuses (status) VALUES (%s)""", ('waiting',))
    cursor.execute("""INSERT INTO call_statuses (status) VALUES (%s)""", ('in work',))
    cursor.execute("""INSERT INTO call_statuses (status) VALUES (%s)""", ('finished',))

    print("Table [call_statuses] created successfully")


    cursor.execute(
        """CREATE TABLE IF NOT EXISTS requests_for_a_call (
                        id serial PRIMARY KEY,
                        user_id INT,
                        call_status_id INT,
                        name varchar(255),
                        phone_number varchar(255),
                        date_of_application_processing date NOT NULL,
                        application_date date NOT NULL,
                        qestion text NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(user_id),
                        FOREIGN KEY (call_status_id) REFERENCES call_statuses(call_status_id))""")

    cursor.execute("""ALTER TABLE requests_for_a_call DROP CONSTRAINT requests_for_a_call_call_status_id_fkey""")
    cursor.execute("""ALTER TABLE requests_for_a_call DROP CONSTRAINT requests_for_a_call_user_id_fkey""")

    print("Table [requests_for_a_call] created successfully")


    cursor.execute(
        """CREATE TABLE IF NOT EXISTS product_type (
                        product_type_id serial PRIMARY KEY,
                        type_name varchar(255) NOT NULL)""")

    cursor.execute("""INSERT INTO product_type (type_name) VALUES (%s)""", ('type1',))
    cursor.execute("""INSERT INTO product_type (type_name) VALUES (%s)""", ('type2',))

    print("Table [types_of_measurements] created successfully")

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS products (
                        products_id serial PRIMARY KEY,
                        product_type_id INT,
                        prod_status_id INT,
                        description text NOT NULL,
                        date_of_creating date NOT NULL,
                        name varchar(255) NOT NULL,
                        photo text NOT NULL,
                        FOREIGN KEY (product_type_id) REFERENCES product_type(product_type_id),
                        FOREIGN KEY (prod_status_id) REFERENCES product_status(prod_status_id));""")

    cursor.execute("""ALTER TABLE products DROP CONSTRAINT products_product_type_id_fkey""")
    cursor.execute("""ALTER TABLE products DROP CONSTRAINT products_prod_status_id_fkey""")

    print("Table [products] created successfully")

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS shopping_list (
                        id serial PRIMARY KEY,
                        products_id INT,
                        user_id INT,
                        FOREIGN KEY (user_id) REFERENCES users(user_id),
                        FOREIGN KEY (products_id) REFERENCES products(products_id));""")

    cursor.execute("""ALTER TABLE shopping_list DROP CONSTRAINT shopping_list_products_id_fkey""")
    cursor.execute("""ALTER TABLE shopping_list DROP CONSTRAINT shopping_list_user_id_fkey""")

    print("Table [shopping_list] created successfully")

    if connection:
        print("Connected close")
        cursor.close()
        connection.close()

except Exception as e:
    print('[INFO] Database creation failed because: ', e)

