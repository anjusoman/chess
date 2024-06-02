from flask import Flask, request, jsonify
from flask_cors import CORS

from chessLogic import IsMoveLegal, Square, Move, IsInCheck, IsCheckmate

app = Flask(__name__)
CORS(app)

@app.route('/api/isMoveLegal', methods=['POST'])
def check_is_move_legal():
    data = request.json
    board = data['board']
    move = Move( Square(data['fromRow'], data['fromCol']), Square(data['toRow'], data['toCol']))
    
    print('Received data:', board, move)

    result = IsMoveLegal(board, move)
    response_data = {'message': 'Data received successfully', 'result': result}
    return jsonify(response_data)

@app.route('/api/isInCheck', methods=['POST'])
def check_is_in_check():
    data = request.json
    board = data['board']
    player = data['player']
    
    print('Received data:', data)

    result = IsInCheck(board, player)
    response_data = {'message': 'Data received successfully', 'result': result}
    return jsonify(response_data)

@app.route('/api/isCheckmate', methods=['POST'])
def check_is_checkmate():
    data = request.json
    board = data['board']
    player = data['player']
    
    result = IsCheckmate(board, player)
    response_data = {'message': 'Data received successfully', 'result': result}
    return jsonify(response_data)

    
if __name__ == '__main__':
    app.run(debug=True)