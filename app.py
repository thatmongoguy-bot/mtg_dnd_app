from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Folder to store deck files
DECK_FOLDER = "decks"
os.makedirs(DECK_FOLDER, exist_ok=True)

# Serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

# --- Deck Routes ---

@app.route('/api/deck/save', methods=['POST'])
def save_deck():
    data = request.json
    deck_name = data.get('name', 'default')
    deck_content = data.get('deck', {})
    
    filepath = os.path.join(DECK_FOLDER, f"{deck_name}.json")
    with open(filepath, 'w') as f:
        json.dump(deck_content, f, indent=2)
    
    return jsonify({'status': 'success', 'message': f'Deck "{deck_name}" saved'})

@app.route('/api/deck/load/<deck_name>', methods=['GET'])
def load_deck(deck_name):
    filepath = os.path.join(DECK_FOLDER, f"{deck_name}.json")
    if not os.path.exists(filepath):
        return jsonify({'error': 'Deck not found'}), 404
    
    with open(filepath, 'r') as f:
        deck = json.load(f)
    
    return jsonify({'status': 'success', 'deck': deck})

@app.route('/api/deck/list', methods=['GET'])
def list_decks():
    files = os.listdir(DECK_FOLDER)
    decks = [f.replace('.json', '') for f in files if f.endswith('.json')]
    return jsonify({'decks': decks})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
