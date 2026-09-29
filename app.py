from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from engine.rulebook import Rulebook
from engine.game import Game
import json
import os

app = Flask(__name__)
CORS(app)

# Folder to store deck files
DECK_FOLDER = "decks"
os.makedirs(DECK_FOLDER, exist_ok=True)

# Load the rulebook
rules = Rulebook("data/mtg_rules2026.txt")
game = None

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

@app.route('/api/rules/search', methods=['POST'])
def search_rules():
    data = request.json
    keyword = data.get('keyword', '')
    results = rules.search(keyword)
    return jsonify({
        'keyword': keyword,
        'count': len(results),
        'results': [{'line': line, 'text': text} for line, text in results[:10]]})

@app.route('/api/start', methods=['POST'])
def start_game():
    global game
    data = request.json
    format_type = data.get('format', 'Standard')
    players = data.get('players', [])
    
    game = Game(format_type)
    for name in players:
        game.add_player(name)
    
    return jsonify({'status': 'success', 'message': f'{format_type} game started with {len(players)} players'})

@app.route('/api/status', methods=['GET'])
def get_status():
    if not game:
        return jsonify({'error': 'No game in progress'}), 400
    
    players_data = []
    for p in game.players:
        players_data.append({
            'name': p.name,
            'life': p.life.value,
            'poison': p.poison.value,
            'commander_damage': dict(p.commander_damage)
        })
    
    return jsonify({
        'format': game.format_type,
        'current_turn': game.current_turn_index,
        'players': players_data
    })

@app.route('/api/life', methods=['POST'])
def change_life():
    if not game:
        return jsonify({'error': 'No game in progress'}), 400
    
    data = request.json
    player_index = data.get('player_index')
    amount = data.get('amount', 1)
    
    if player_index is None or player_index >= len(game.players):
        return jsonify({'error': 'Invalid player'}), 400
    
    player = game.players[player_index]
    if amount < 0:
        for _ in range(abs(amount)):
            player.life.decrement()
    else:
        for _ in range(amount):
            player.life.increment()
    
    return jsonify({'status': 'success', 'new_life': player.life.value})

@app.route('/api/poison', methods=['POST'])
def add_poison():
    if not game:
        return jsonify({'error': 'No game in progress'}), 400
    
    data = request.json
    player_index = data.get('player_index')
    amount = data.get('amount', 1)
    
    if player_index is None or player_index >= len(game.players):
        return jsonify({'error': 'Invalid player'}), 400
    
    if amount > 0:
        for _ in range(amount):
            game.players[player_index].poison.increment()
    else:
        for _ in range(abs(amount)):
            game.players[player_index].poison.decrement()
    
    return jsonify({'status': 'success', 'new_poison': game.players[player_index].poison.value})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
