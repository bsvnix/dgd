from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory data storage (replace with a database for persistence)
scan_results = []
decoy_events = []

@app.route('/')
def index():
    return render_template('index.html', scan_results=scan_results, decoy_events=decoy_events)

@app.route('/api/scan_results', methods=['POST'])
def scan_results():
    data = request.get_json()
    scan_results.append(data)
    return jsonify({'message': 'Scan results received'}), 200

@app.route('/api/decoy_event', methods=['POST'])
def decoy_event():
    data = request.get_json()
    decoy_events.append(data)
    return jsonify({'message': 'Decoy event received'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
