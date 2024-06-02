import React, {useEffect, useState} from 'react';
import '../styles/boardSquare.css'
import {EMPTY} from './board';
import { getPieceIconPath } from '../App';

const LIGHT = "light"
const DARK = "dark"
const SELECTED = "selected"

function BoardSquare({piece, rowNum, colNum, onBoardSquareClick, isSelected, getPieceColor}){
    const [squareColor, setSquareColor] = useState("");
    const [pieceColor, setPieceColor] = useState("")
    const [pieceIconPath, setPieceIconPath] = useState("");
    
    useEffect( ()=> { 
        setSquareColor(getSquareColor());
    }, [isSelected] )

    useEffect( () => {
        const newPieceColor = getPieceColor(piece);
        const newPieceIconPath = getPieceIconPath(piece, newPieceColor);

        setPieceColor(newPieceColor);
        setPieceIconPath(newPieceIconPath);
    }, [piece])

    function getSquareColor() {
        if (isSelected){
            return SELECTED;
        }
        else if (rowNum % 2 == 0){
            if (colNum % 2 == 0){
                return LIGHT;
            } 
            return DARK;
        } else {
            if (colNum % 2 == 0){
                return DARK;
            } 
            return LIGHT;
        }
    }


    return (
        <div className={"square square--" + squareColor}>
            <button className='square__button' onClick={() => onBoardSquareClick(rowNum, colNum)}>
                { EMPTY!=piece && <img className="square__button__icon" alt={pieceColor + " " + piece} src={pieceIconPath} />}
            </button>    
        </div>
    )
}

export default BoardSquare;
