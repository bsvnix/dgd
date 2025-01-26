from flask import Flask, render_template, request, jsonify, g, abort
from flask_cors import CORS
import os
import psycopg2

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Database configuration from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'dgd')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')


def get_db():
    """Get a connection to the database."""
    if 'db' not in g:
        try:
            g.db = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
        except psycopg2.OperationalError as e:
            g.db = None
            app.logger.error(f"Database connection failed: {e}")
    return g.db


@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection when the app context ends."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    """Render the main page with scan results and decoy events."""
    db = get_db()
    scan_results = []
    decoy_events = []
    if db:
        try:
            cur = db.cursor()
            cur.execute('SELECT * FROM scan_results')
            scan_results = cur.fetchall()
            cur.execute('SELECT * FROM decoy_events')
            decoy_events = cur.fetchall()
            cur.close()
        except psycopg2.Error as e:
            app.logger.error(f"Database query failed: {e}")
    else:
        app.logger.warning("Database is not connected. Displaying empty data.")
    return render_template('index.html', scan_results=scan_results, decoy_events=decoy_events)


@app.route('/api/scan_results', methods=['POST'])
def api_scan_results():
    """API endpoint to receive scan results."""
    data = request.get_json()
    if not data or 'ip' not in data or 'open_ports' not in data:
        abort(400, description="Invalid data format")
    db = get_db()
    if db:
        try:
            cur = db.cursor()
            cur.execute(
                'INSERT INTO scan_results (ip, open_ports) VALUES (%s, %s)',
                (data['ip'], ', '.join(map(str, data['open_ports'])))
            )
            db.commit()
            cur.close()
            return jsonify({'message': 'Scan results received'}), 200
        except psycopg2.Error as e:
            app.logger.error(f"Database insert failed: {e}")
            abort(500, description="Failed to save scan results to the database")
    else:
        app.logger.warning("Database is not connected. Data cannot be saved.")
        abort(503, description="Database is not available")
    return jsonify({'message': 'Scan results received'}),
