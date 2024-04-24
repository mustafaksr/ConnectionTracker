from flask import Flask, jsonify
import psycopg2
from retry import retry
from prometheus_client import generate_latest
from prometheus_client import start_http_server, Counter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@postgres:5432/postgres'  # Update connection details

## prometheus metrics for backend
REQUEST_COUNT0 = Counter('backend_home_http_requests_total', 'Total number of HTTP requests for backend home')

REQUEST_COUNT1 = Counter('backend_hello_http_requests_total', 'Total number of HTTP requests for backend hello')

REQUEST_COUNT2 = Counter('backend_getconnections_http_requests_total', 'Total number of HTTP requests for backend getconnections')

REQUEST_COUNT3 = Counter('backend_lastconnection_http_requests_total', 'Total number of HTTP requests for backend lastconnection')


@retry(delay=2, backoff=2, max_delay=30)
def create_db_connection():
    return psycopg2.connect(
        host="postgres",  # Use the service name defined in docker-compose.yml
        user="postgres",
        password="123456",
        dbname="postgres"
    )
db_connection = create_db_connection()
db_cursor = db_connection.cursor()
@app.route('/')
def home():
    REQUEST_COUNT0.inc()
    return "api backend started successfully.\n\n you can visit | /api/hello  | /api/connections | /api/last_connection |"

@app.route('/api/hello')
def hello():
    REQUEST_COUNT1.inc()
    return jsonify(message="Hello from the backend!")

@app.route('/api/connections')
def get_connections():
    REQUEST_COUNT2.inc()
    select_query = "SELECT * FROM connections ORDER BY time DESC"
    db_cursor.execute(select_query)
    connection_records = db_cursor.fetchall()


    return jsonify(connections=connection_records)

@app.route('/api/last_connection')
def last_connections():
    REQUEST_COUNT3.inc()
    select_query = "SELECT * FROM connections ORDER BY time DESC LIMIT 1;"
    db_cursor.execute(select_query)
    connection_records = db_cursor.fetchall()


    return jsonify(connections=connection_records)

if __name__ == '__main__':
    start_http_server(8000)  # Start the Prometheus metrics server on port 8000

    app.run(host='0.0.0.0', port=7050)
