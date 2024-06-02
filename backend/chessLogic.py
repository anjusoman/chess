from collections import namedtuple

WHITE = 'w'
BLACK = 'b'

EMPTY = '.'

W_PAWN = 'P'
W_ROOK = 'R'
W_BISHOP = 'B'
W_QUEEN = 'Q'
W_KNIGHT = 'T'
W_KING = 'K'

B_PAWN = 'p'
B_ROOK = 'r'
B_BISHOP = 'b'
B_QUEEN = 'q'
B_KNIGHT = 't'
B_KING = 'k'

#Additional data structures used throughout the program for improved readability
Square = namedtuple('Square', ['row', 'col'])
Move = namedtuple('Move', ['fromSquare', 'toSquare'])
Piece = namedtuple('Piece', ['piece', 'square'])
Result = namedtuple('Result', ['score', 'moves'])

# return True if the input move (from-square and to-square) is legal, else False
# input is from-square and to-square
# this is the KEY function which contains the rules for each piece type
def IsMoveLegal(board, move):

  fromSquare = move.fromSquare
  toSquare = move.toSquare

  # if the fromSquare and toSquare are the same square or if the move is out of bounds
  if fromSquare.row == toSquare.row and fromSquare.col == toSquare.col:
      return False

  # use the input and the board to get the from-piece and to-piece
  fromPiece = board[fromSquare.row][fromSquare.col]
  toPiece = board[toSquare.row][toSquare.col]

  # Get the player based on from piece
  player = getPlayer(fromPiece)

  # Player cannot move a piece to a square occupied by their own piece
  if getPlayer(toPiece) == player:
    return False

  diffRow = (fromSquare.row - toSquare.row) 
  diffCol = (toSquare.col - fromSquare.col) 


  #if the from-piece is a "pawn"
  if fromPiece == W_PAWN or fromPiece == B_PAWN:

    #case -> pawn wants to move one step forward, toPiece must be empty
    if diffCol == 0 and diffRow == 1 and toPiece == EMPTY:
        return True

    #case -> white pawn can move two spaces forward ONLY if pawn on starting row
    elif diffCol == 0 and diffRow == 2 and fromSquare.row == 6 and IsClearPath(board, fromSquare, toSquare):
      return True

    #case - pawn attacks the enemy piece (diagonal)
    elif (abs(diffRow) == abs(diffCol) and diffRow == 1) and IsEnemyPiece(player, toPiece):
      return True


  # else if the from-piece is a "rook"
  elif fromPiece == W_ROOK or fromPiece == B_ROOK:

    #if to-square is in the same row or column and there is a clear path between fromSquare and toSquare
    if (diffRow == 0 or diffCol == 0) and IsClearPath(board, fromSquare, toSquare):
      return True


  # else if the from-piece is a "bishop"
  elif fromPiece == W_BISHOP or fromPiece == B_BISHOP:

    #if toSquare is diagonal with fromSquare and there is a clear path between fromSquare and toSquare
    if abs(diffRow) == abs(diffCol) and IsClearPath(board, fromSquare, toSquare):
      return True


  # else if the from-piece is a "queen"
  elif fromPiece == W_QUEEN or fromPiece == B_QUEEN:

    #if to-square is in the same row or column and there is a clear path between fromSquare and toSquare
    if (diffRow == 0 or diffCol == 0) and IsClearPath(board, fromSquare, toSquare):
      return True

    #if toSquare is diagonal with fromSquare and there is a clear path between fromSquare and toSquare
    if abs(diffRow) == abs(diffCol) and IsClearPath(board, fromSquare, toSquare):
      return True

  # else if the from-piece is a "knight"
  elif fromPiece == W_KNIGHT or fromPiece == B_KNIGHT:

    # return True for any of the following cases:
    if ( (diffRow == -2 and diffCol == 1) or
        (diffRow == -1 and diffCol == 2) or
        (diffRow == 1 and diffCol == 2) or
        (diffRow == 2 and diffCol == 1) or
        (diffRow == -2 and diffCol == -1) or
        (diffRow == -1 and diffCol == -2) or
        (diffRow == 1 and diffCol == -2) or
        (diffRow == 2 and diffCol == -1) ):

      return True

  # else if the from-piece is a "king"
  elif fromPiece == W_KING or fromPiece == B_KING:

    # return True for any of the following cases:
    if ((abs(diffCol) == 1 and abs(diffRow) == 0) or (abs(diffCol) == 0 and abs(diffRow) == 1) or (abs(diffCol) == 1 and abs(diffRow) == 1)):
        return True

  # return False - if none of the other True's are hit above
  return False


# gets a list of legal moves for a given piece
# input = current player and the given piece as the from-square
# output = list of to-square locations where the piece can move to
def GetListOfLegalMoves(board, fromSquare):

  # initialize the list of legal moves, i.e., to-square locations to []
  legalMoves = []

  # go through all squares on the board
  for row in range(0, 8):
    for col in range(0, 8):

      # for the selected square as to-square
      toSquare = Square(row, col)
      move = Move(fromSquare, toSquare)

      # call IsMoveLegal() with input move = from-square and to-square, if returned value is True
      if IsMoveLegal(board, move):

          # call DoesMovePutPlayerInCheck with input as move = from-square and to-square, if returned value is False
          if not DoesMovePutPlayerInCheck(board, move):

            # append this move as a legal move
            legalMoves.append(move)

  # return the list of legal moves (to-square locations)
  return legalMoves


# gets a list of all pieces for the current player that have legal moves
def GetPiecesWithLegalMoves(board, player):

  # initialize the list of pieces with legal moves to []
  piecesWithLegalMoves = []

  # go through all squares on the board
  for row in range(0, 8):
    for col in range(0, 8):
      piece = board[row][col]

      # for the selected square, if the square contains a piece that belongs to the current player's team
      if getPlayer(piece) == player:

        # call GetListOfLegalMoves() to get a list of all legal moves for the selected piece / square
        fromSquare = Square(row, col)
        legalMoves = GetListOfLegalMoves(board, fromSquare)

         # if the piece has any legal moves, append this piece to the list of pieces with legal moves
        if len(legalMoves) > 0:
          piece = Piece(piece, fromSquare)
          piecesWithLegalMoves.append(piece)

  # return the final list of pieces with legal moves
  return piecesWithLegalMoves


# returns True if the current player is in checkmate, else False
def IsCheckmate(board, player):

  # call GetPiecesWithLegalMoves to get all legal moves for the current player
  piecesWithLegalMoves = GetPiecesWithLegalMoves(board, player)

  # if there is no piece with any valid move return True, else return False
  if len(piecesWithLegalMoves) == 0:
    return True
  else:
    return False


# returns True if the given player is in Check state
def IsInCheck(board, player):
  # find given player's King's location = king-square
  kingSquare = None
  king = W_KING if player == WHITE else B_KING

  for row in range(0, 8):
    for col in range(0, 8):
      if board[row][col] == king:
        print(board)
        kingSquare = Square(row, col)
        break

  if kingSquare is None:
    print("Error Occured: Could not locate king")
    print(row, col, board[row][col], king)

  # go through all squares on the board
  for row in range(0, 8):
    for col in range(0, 8):

      # if there is a piece at that location and that piece is of the enemy team
      if IsEnemyPiece(player, board[row][col]):

        # call IsMoveLegal() for the enemy player from that square to the king-square, if the value returned is True, return True
        if IsMoveLegal(board, Move(Square(row, col), kingSquare)):
          return True

  # return False at the end
  return False



# helper function to figure out if a move is legal for straight-line moves (rooks, bishops, queens, pawns)
# returns True if the path is clear for a move (from-square and to-square), non-inclusive
def IsClearPath(board, fromSquare, toSquare):

    diffRow = toSquare.row - fromSquare.row # diffRow > 0 if toSquare is in the +vertical direction from fromSqaure
    diffCol = toSquare.col - fromSquare.col # diffCol > 0 if toSquare is in the +horizontal direction from fromSquare

    newFromSquare = None

    #if the from and to squares are only one square apart, return True
    if abs(diffRow) <= 1 and abs(diffCol) <= 1:
      return True

    else:

      #if to-square is in the +ve vertical direction from from-square, new-from-square = next square in the +ve vertical direction
      if diffRow > 0 and diffCol == 0:
        newFromSquare = Square(fromSquare.row + 1, fromSquare.col)

      # else if to-square is in the -ve vertical direction from from-square, new-from-square = next square in the -ve vertical direction
      elif diffRow < 0 and diffCol == 0:
        newFromSquare = Square(fromSquare.row - 1, fromSquare.col)

      #else if to-square is in the +ve horizontal direction from from-square, new-from-square = next square in the +ve horizontal direction
      elif diffRow == 0 and diffCol > 0:
        newFromSquare = Square(fromSquare.row, fromSquare.col + 1)

      #else if to-square is in the -ve horizontal direction from from-square, new-from-square = next square in the -ve horizontal direction
      elif diffRow == 0 and diffCol < 0:
        newFromSquare = Square(fromSquare.row, fromSquare.col - 1)

      # else if to-square is in the SE diagonal direction from from-square, new-from-square = next square in the SE diagonal direction
      elif diffRow > 0 and diffCol > 0:
        newFromSquare = Square(fromSquare.row + 1, fromSquare.col + 1)

      # else if to-square is in the SW diagonal direction from from-square, new-from-square = next square in the SW diagonal direction
      elif diffRow > 0 and diffCol < 0:
        newFromSquare = Square(fromSquare.row + 1, fromSquare.col - 1)

      # else if to-square is in the NE diagonal direction from from-square, new-from-square = next square in the NE diagonal direction
      elif diffRow < 0 and diffCol > 0:
        newFromSquare = Square(fromSquare.row - 1, fromSquare.col + 1)

      # else if to-square is in the NW diagonal direction from from-square, new-from-square = next square in the NW diagonal direction
      elif diffRow < 0 and diffCol < 0:
        newFromSquare = Square(fromSquare.row - 1, fromSquare.col - 1)

    # if new-from-square is not empty, return False
    if board[newFromSquare.row][newFromSquare.col] != EMPTY:
      return False

    #else return the result from the recursive call of IsClearPath() with the new-from-square and to-square
    else:
      return IsClearPath(board, newFromSquare, toSquare)


# makes a hypothetical move (from-square and to-square)
# returns True if it puts current player into check
def DoesMovePutPlayerInCheck(board, move):
  # given the move (from-square and to-square), get the player
  fromSquare = move.fromSquare
  fromPiece = board[fromSquare.row][fromSquare.col]
  player = getPlayer(fromPiece)

  # make the move temporarily by changing the 'board'
  boardCopy = [ row[:] for row in board ]
  MovePiece(boardCopy, move)

  # Call the IsInCheck() function to see if the 'player' is in check and return True if it puts current player into check, False otherwise
  return IsInCheck(boardCopy, player)


def IsEnemyPiece(player, piece):
  if getEnemyPlayer(player) == getPlayer(piece):
    return True
  else:
    return False

def getPlayer(piece):
  if piece.islower():
    return BLACK
  elif piece.isupper():
    return WHITE
  else:
    return EMPTY

def getEnemyPlayer(player):
  if player == WHITE:
    return BLACK
  else:
    return WHITE