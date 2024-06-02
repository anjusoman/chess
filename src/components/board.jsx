import React, {useEffect, useState} from 'react';
import BoardSquare from './boardSquare';
import axios from 'axios';
import '../styles/board.css'

export const WHITE_PIECES = {
    PAWN: 'P',
    ROOK: 'R',
    BISHOP: 'B',
    QUEEN: 'Q',
    KNIGHT: 'T',
    KING: 'K',
};

export const BLACK_PIECES = {
    PAWN: 'p',
    ROOK: 'r',
    BISHOP: 'b',
    QUEEN: 'q',
    KNIGHT: 't',
    KING: 'k',
};

export const EMPTY = '.';

export const BLACK = "Black"
export const WHITE = "White"

function Board({currentPlayer, setCurrentPlayer, setIsInCheck, setIsCheckmate, setError, errorInitialState, setResetTimer, setBlackPiecesTaken, setWhitePiecesTaken, whitePiecesTaken, blackPiecesTaken}){
    const [board, setBoard] = useState([]);
    const fromSquareInitialState = {row:-1, col:-1}
    const [fromSquare, setFromSquare] = useState(fromSquareInitialState);
   
    useEffect( () => {
        setBoard(ChessBoardSetup())
    }, [])

    useEffect( () => {
        if (board.length == 8){ //ensure board has been set up already
            checkIsInCheck(currentPlayer);
            checkIsCheckmate(currentPlayer);
        }
        
    }, [currentPlayer])

   
    // initialize and return a chess board - create a 2D 8x8 array that has the value for each cell
    function ChessBoardSetup() {
        const board = Array.from({ length: 8 }, () => Array(8).fill(EMPTY));
        
        const whiteRow1 = [
            WHITE_PIECES.ROOK,
            WHITE_PIECES.KNIGHT,
            WHITE_PIECES.BISHOP,
            WHITE_PIECES.QUEEN,
            WHITE_PIECES.KING,
            WHITE_PIECES.BISHOP,
            WHITE_PIECES.KNIGHT,
            WHITE_PIECES.ROOK,
        ];
        const whiteRow2 = Array(8).fill(WHITE_PIECES.PAWN);
        const blackRow1 = [
            BLACK_PIECES.ROOK,
            BLACK_PIECES.KNIGHT,
            BLACK_PIECES.BISHOP,
            BLACK_PIECES.QUEEN,
            BLACK_PIECES.KING,
            BLACK_PIECES.BISHOP,
            BLACK_PIECES.KNIGHT,
            BLACK_PIECES.ROOK,
        ];
        const blackRow2 = Array(8).fill(BLACK_PIECES.PAWN);

        board[0] = whiteRow1;
        board[1] = whiteRow2;
        board[6] = blackRow2;
        board[7] = blackRow1;
    
        return board;
    }

    function flipBoard(){
        const boardCopy = board.map(row => [...row]);

        const newBoard = [];

        boardCopy.forEach(item => {
            newBoard.unshift(item)
        });

        newBoard.map(row => {
            row.reverse();
        });
       
        setBoard(newBoard);
    }

    const handleBoardSquareClick = async(rowNum, colNum) => {
        
        if ((fromSquare.row) < 0){ //first click - set from square
            const piece = board[rowNum][colNum]
            if (getPieceColor(piece) != currentPlayer){
                setError({show: true, message: "Select " + currentPlayer + " piece"})
            } else {
                setFromSquare({row: rowNum, col: colNum});
            }
           
        } else { //second click - set to square
            const move = { fromSquare: fromSquare, toSquare: {row: rowNum, col: colNum}}
            const isValidMove = await checkIsValidMove(move)
            
            if (isValidMove) {
                MovePiece(move);
                setError(errorInitialState);
                setTimeout(() => {
                    switchPlayers();
                    flipBoard();
                    setResetTimer(true);
                }, 1000);
                
            } else {
                setError({show: true, message: "Invalid move" })
            }

            setFromSquare(fromSquareInitialState)
        }
    }

    const checkIsValidMove = async(move) => {
        try {
            const response = await axios.post('http://localhost:5000/api/isMoveLegal', 
                                            {   
                                                board:  board, 
                                                fromRow: move.fromSquare.row, 
                                                fromCol: move.fromSquare.col,  
                                                toRow: move.toSquare.row, 
                                                toCol: move.toSquare.col
                                            });

            const isValidMove = response.data.result
            return isValidMove
        } catch (error) {
            console.error('Error:', error);
            return false //TODO: implement error logic
        }
    }

    const checkIsInCheck = async(player) => {
        try {
            const response = await axios.post('http://localhost:5000/api/isInCheck', 
                                            {   
                                                board: board, 
                                                player: player
                                            });

            const isInCheck = response.data.result
            setIsInCheck(isInCheck);
        } catch (error) {
            console.error('Error:', error);
            return false //TODO: implement error logic
        }
    }

    const checkIsCheckmate = async(player) => {
        try {
            const response = await axios.post('http://localhost:5000/api/isCheckmate', 
                                            {   
                                                board: board, 
                                                player: player
                                            });

            const isCheckmate = response.data.result
            return isCheckmate
        } catch (error) {
            console.error('Error:', error);
            return false //TODO: implement error logic
        }
    }

    function MovePiece(move) {
        const {fromSquare, toSquare} = move 
        
        const piece = board[fromSquare.row][fromSquare.col];
        const pieceTaken = board[toSquare.row][toSquare.col];

        // Create a new copy of the board
        const newBoard = [...board];

        // Update the element at fromSquare to EMPTY
        newBoard[fromSquare.row][fromSquare.col] = EMPTY;

        // Update the element at toSquare to piece
        newBoard[toSquare.row][toSquare.col] = piece;

        if (pieceTaken != EMPTY){
            const pieceTakenColor = getPieceColor(pieceTaken);
            
            if (pieceTakenColor == WHITE) { 
                setWhitePiecesTaken([...whitePiecesTaken, pieceTaken]);
            }
            else {
                setBlackPiecesTaken([...blackPiecesTaken, pieceTaken])
            };
        }
        setBoard(newBoard);
    }
    
    function switchPlayers() {
        if (currentPlayer == WHITE) setCurrentPlayer(BLACK);
        else setCurrentPlayer(WHITE);
    }

    function getPieceColor(piece) {
        if (piece==EMPTY) return EMPTY;
        else if (piece === piece.toUpperCase()) return BLACK;
        else return WHITE;
    }
  
    return (
        <div className='board'>
            <div className="board__grid">
                {board.map((row, rowNum) => {
                    return row.map((piece, colNum) => {
                        return (         
                            <BoardSquare 
                                key={rowNum.toString()+colNum.toString()} 
                                piece={piece} 
                                rowNum={rowNum} 
                                colNum={colNum} 
                                onBoardSquareClick={handleBoardSquareClick} 
                                isSelected={(fromSquare.row == rowNum && fromSquare.col == colNum)}
                                getPieceColor={getPieceColor} />
                        )
                    })
                })}
            </div>
        </div>
      
    )
}

export default Board;

