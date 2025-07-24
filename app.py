from flask import Flask, jsonify, render_template
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import random
from os import environ

app = Flask(__name__)

# Configuration for MySQL database
DB_CONFIG = {
    'host': environ['DB_HOST'],
    'user': environ['DB_USER'],           
    'password': environ['DB_USER_PASSWORD'],
    'database': environ['APP_DATABASE']
}

# Establish a connection to the database
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Route index

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Route 1: Create Table in the Database
@app.route('/create-db', methods=['GET'])
def create_db():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                id INT PRIMARY KEY AUTO_INCREMENT,
                data1 VARCHAR(100),
                data2 VARCHAR(100)
            )
        ''')
        connection.commit()
        cursor.close()
        return jsonify({"message": "Table 'data' created successfully"})
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# Route 2: Insert Dummy Data into the Table
@app.route('/insert-dummy', methods=['GET', 'POST'])
def insert_dummy():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        random_number = str(random.randint(1, 100))

        cursor = connection.cursor()
        cursor.execute("INSERT INTO data (data1, data2) VALUES (%s, %s)", (current_time, random_number))
        connection.commit()
        cursor.close()
        return jsonify({"message": "Dummy data inserted successfully"})
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

# Route 3: Retrieve and Display All Data from the Table
@app.route('/get-data', methods=['GET'])
def get_data():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM data")
        rows = cursor.fetchall()
        cursor.close()
        return jsonify(rows)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
