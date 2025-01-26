from flask import Flask, render_template, request, jsonify, g, abort
from flask_cors import CORS
import os
import psycopg2  # Assuming PostgreSQL as the external database

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
        g.db = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
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
    cur = db.cursor()
    cur.execute('SELECT * FROM scan_results')
    scan_results = cur.fetchall()
    cur.execute('SELECT * FROM decoy_events')
    decoy_events = cur.fetchall()
    cur.close()
    return render_template('index.html', scan_results=scan_results, decoy_events=decoy_events)


@app.route('/api/scan_results', methods=['POST'])
def api_scan_results():
    """API endpoint to receive scan results."""
    data = request.get_json()
    if not data or 'ip' not in data or 'open_ports' not in data:
        abort(400, description="Invalid data format")
    db = get_db()
    cur = db.cursor()
    cur.execute(
        'INSERT INTO scan_results (ip, open_ports) VALUES (%s, %s)',
        (data['ip'], ', '.join(map(str, data['open_ports'])))
    )
    db.commit()
    cur.close()
    return jsonify({'message': 'Scan results received'}), 200


@app.route('/api/decoy_event', methods=['POST'])
def api_decoy_event():
    """API endpoint to receive decoy events."""
    data = request.get_json()
    if not data or 'decoy_name' not in data or 'port' not in data or 'attacker_ip' not in data:
        abort(400, description="Invalid data format")
    db = get_db()
    cur = db.cursor()
    cur.execute(
        'INSERT INTO decoy_events (decoy_name, port, attacker_ip) VALUES (%s, %s, %s)',
        (data['decoy_name'], data['port'], data['attacker_ip'])
    )
    db.commit()
    cur.close()
    return jsonify({'message': 'Decoy event received'}), 200


if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0')
