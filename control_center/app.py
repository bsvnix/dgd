from flask import Flask, render_template, request, jsonify, g, abort
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Database file path
DATABASE = '/app/dgd.db'


def get_db():
    """Get a connection to the SQLite database."""
    if 'db' not in g:
        try:
            g.db = sqlite3.connect(DATABASE)
            g.db.row_factory = sqlite3.Row  # Return rows as dictionaries for easier access
        except sqlite3.Error as e:
            app.logger.error(f"Database connection failed: {e}")
            g.db = None
    return g.db


@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection when the app context ends."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """Initialize the database using schema.sql."""
    if not os.path.exists(DATABASE):
        app.logger.info("Initializing database...")
        try:
            with app.app_context():
                db = get_db()
                if db is None:
                    raise Exception("Database connection not available.")
                with app.open_resource('schema.sql', mode='r') as f:
                    db.executescript(f.read())
                db.commit()
                app.logger.info("Database initialized successfully.")
        except Exception as e:
            app.logger.error(f"Error initializing database: {e}")
    else:
        app.logger.info("Database already exists. Initialization skipped.")


@app.route('/')
def index():
    """Render the main page with scan results and decoy events."""
    try:
        db = get_db()
        if db is None:
            return "Database connection failed. Please check the logs.", 500

        # Fetch scan results and decoy events
        scan_results = db.execute('SELECT * FROM scan_results').fetchall()
        decoy_events = db.execute('SELECT * FROM decoy_events').fetchall()

        return render_template('index.html', scan_results=scan_results, decoy_events=decoy_events)
    except sqlite3.Error as e:
        app.logger.error(f"Database query failed: {e}")
        return "Internal Server Error", 500
    except Exception as e:
        app.logger.error(f"Unexpected error in index route: {e}")
        return "Internal Server Error", 500


@app.route('/api/scan_results', methods=['POST'])
def api_scan_results():
    """API endpoint to receive scan results."""
    data = request.get_json()
    if not data or 'ip' not in data or 'open_ports' not in data:
        abort(400, description="Invalid data format")

    try:
        db = get_db()
        if db is None:
            abort(503, description="Database connection failed")

        db.execute(
            'INSERT INTO scan_results (ip, open_ports) VALUES (?, ?)',
            (data['ip'], ', '.join(map(str, data['open_ports'])))
        )
        db.commit()
        return jsonify({'message': 'Scan results received'}), 200
    except sqlite3.Error as e:
        app.logger.error(f"Database insert failed: {e}")
        abort(500, description="Failed to save scan results")
    except Exception as e:
        app.logger.error(f"Unexpected error in api_scan_results: {e}")
        abort(500, description="Internal Server Error")


@app.route('/api/decoy_event', methods=['POST'])
def api_decoy_event():
    """API endpoint to receive decoy events."""
    data = request.get_json()
    if not data or 'decoy_name' not in data or 'port' not in data or 'attacker_ip' not in data:
        abort(400, description="Invalid data format")

    try:
        db = get_db()
        if db is None:
            abort(503, description="Database connection failed")

        db.execute(
            'INSERT INTO decoy_events (decoy_name, port, attacker_ip) VALUES (?, ?, ?)',
            (data['decoy_name'], data['port'], data['attacker_ip'])
        )
        db.commit()
        return jsonify({'message': 'Decoy event received'}), 200
    except sqlite3.Error as e:
        app.logger.error(f"Database insert failed: {e}")
        abort(500, description="Failed to save decoy event")
    except Exception as e:
        app.logger.error(f"Unexpected error in api_decoy_event: {e}")
        abort(500, description="Internal Server Error")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
