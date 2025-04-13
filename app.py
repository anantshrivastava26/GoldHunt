
from flask import Flask, render_template, request, jsonify
from game_logic import Game
import time

app = Flask(__name__)
game = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global game
    data = request.get_json()
    size = int(data['size'])
    game = Game(size)
    return jsonify({"status": "started", "grid": game.get_visible_grid(), "player": game.player_pos})

@app.route('/move', methods=['POST'])
def move():
    direction = request.get_json()['direction']
    game.move_player(direction)
    return jsonify({"grid": game.get_visible_grid(), "player": game.player_pos, "status": game.status})

@app.route('/ai')
def run_ai():
    steps = game.run_ai_trace()
    return jsonify({"steps": steps})


if __name__ == '__main__':
    app.run(debug=True)
