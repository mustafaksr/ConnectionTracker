from flask import Flask, request, render_template
import psycopg2
from datetime import datetime
from retry import retry
from pymongo import MongoClient
from prometheus_client import start_http_server, Counter
from prometheus_client import generate_latest


app = Flask(__name__)

mongo_client = MongoClient("mongodb://root:password@mongodb:27017/")  # Use the service name defined in docker-compose.yml
mongo_db = mongo_client["mydatabase"]
mongo_collection = mongo_db["connections"]

## prometheus metrics http_requests_total
REQUEST_COUNT = Counter('webapp_http_requests_total', 'Total number of HTTP requests for webapp')

@retry(delay=2, backoff=2, max_delay=30)
def create_db_connection():
    return psycopg2.connect(
        host="postgres",  # Use the service name defined in docker-compose.yml
        user="postgres",
        password="123456",
        dbname="postgres"
    )

# Database configuration
db_connection = create_db_connection()
db_cursor = db_connection.cursor()

# # Database configuration
# db_connection = psycopg2.connect(
#     host="postgres",  # Use the service name defined in docker-compose.yml
#     user="postgres",
#     password="123456",
#     dbname="postgres"
# )
# db_cursor = db_connection.cursor()

# Create a table to store connection records if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS connections (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP,
    device TEXT
)
"""
db_cursor.execute(create_table_query)
db_connection.commit()

@app.route('/')
def hello_world2():
    REQUEST_COUNT.inc()
    # Record connection in the database
    current_time = datetime.now()
    user_agent = request.headers.get('User-Agent')


    ######## PostgreSQL ########
    insert_query = "INSERT INTO connections (time, device) VALUES (%s, %s)"
    db_cursor.execute(insert_query, (current_time, user_agent))
    db_connection.commit()

    # Fetch all connection records from the database
    select_query = "SELECT * FROM connections ORDER BY time DESC"
    db_cursor.execute(select_query)
    connection_records0 = db_cursor.fetchall()

    ####### MongoDB #########
    mongo_collection.insert_one({"time": current_time, "device": user_agent})

    # Fetch all connection records from MongoDB
    connection_records = list(mongo_collection.find().sort("time", -1))

    return render_template('index.html', connection_records=connection_records0)
@app.route('/metrics')
def metrics():
    return generate_latest()
if __name__ == '__main__':
    start_http_server(8000)  # Start the Prometheus metrics server on port 8000
    print("server listening: http://localhost:2000")
    app.run(host='0.0.0.0', port=2000)

