from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'dgd.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Initialize the database (if it doesn't exist)
try:
    init_db()
except sqlite3.OperationalError:
    pass  # Database already exists

@app.route('/')
def index():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM scan_results')
    scan_results = cur.fetchall()
    cur.execute('SELECT * FROM decoy_events')
    decoy_events = cur.fetchall()
    return render_template('index.html', scan_results=scan_results, decoy_events=decoy_events)

@app.route('/api/scan_results', methods=['POST'])
def scan_results():
    data = request.get_json()
    db = get_db()
    db.execute('INSERT INTO scan_results (ip, open_ports) VALUES (?, ?)', (data['ip'], ', '.join(data['open_ports'])))
    db.commit()
    return jsonify({'message': 'Scan results received'}), 200

@app.route('/api/decoy_event', methods=['POST'])
def decoy_event():
    data = request.get_json()
    db = get_db()
    db.execute('INSERT INTO decoy_events (decoy_name, port, attacker_ip) VALUES (?, ?, ?)', (data['decoy_name'], data['port'], data['attacker_ip']))
    db.commit()
    return jsonify({'message': 'Decoy event received'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
