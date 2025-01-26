from flask import Flask, render_template, request, jsonify, abort, g
import sqlite3
import os

app = Flask(__name__)

# Database setup
DATABASE = 'dgd.db'

def get_db():
    """Get a connection to the database."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Enables dict-like access for rows
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection when the app context ends."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the database using schema.sql."""
    if not os.path.exists(DATABASE):
        print("Initializing database...")
        with app.app_context():
            db = get_db()
            try:
                with app.open_resource('schema.sql', mode='r') as f:
                    db.cursor().executescript(f.read())
                db.commit()
                print("Database initialized successfully.")
            except Exception as e:
                print(f"Error initializing database: {e}")
                raise
    else:
        print("Database already exists.")

# Routes
@app.route('/')
def index():
    """Render the main page with scan results and decoy events."""
    db = get_db()
    scan_results = db.execute('SELECT * FROM scan_results').fetchall()
    decoy_events = db.execute('SELECT * FROM decoy_events').fetchall()
    return render_template('index.html', scan_results=scan_results, decoy_events=decoy_events)

@app.route('/api/scan_results', methods=['POST'])
def api_scan_results():
    """API endpoint to receive scan results."""
    data = request.get_json()
    if not data or 'ip' not in data or 'open_ports' not in data:
        abort(400, description="Invalid data format")
    db = get_db()
    db.execute(
        'INSERT INTO scan_results (ip, open_ports) VALUES (?, ?)',
        (data['ip'], ', '.join(map(str, data['open_ports'])))
    )
    db.commit()
    return jsonify({'message': 'Scan results received'}), 200

@app.route('/api/decoy_event', methods=['POST'])
def api_decoy_event():
    """API endpoint to receive decoy events."""
    data = request.get_json()
    if not data or 'decoy_name' not in data or 'port' not in data or 'attacker_ip' not in data:
        abort(400, description="Invalid data format")
    db = get_db()
    db.execute(
        'INSERT INTO decoy_events (decoy_name, port, attacker_ip) VALUES (?, ?, ?)',
        (data['decoy_name'], data['port'], data['attacker_ip'])
    )
    db.commit()
    return jsonify({'message': 'Decoy event received'}), 200

# Initialize the database when the app starts
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
