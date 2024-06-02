import './styles/App.css';
import Board, {WHITE, BLACK} from './components/board';
import {useState, useEffect} from 'react'
import Timer from './components/timer';

export function getPieceIconPath(piece, newPieceColor){
  const basePath = "/images/pieces/";
  const iconPath = basePath + newPieceColor + "_" + piece.toLowerCase() + ".svg";
  return iconPath;
}

function App() {
  const errorInitialState = {show: false, message:"errorMessage"};
  const [error, setError] = useState(errorInitialState);

  const [isInCheck, setIsInCheck] = useState(false)
  const [isCheckmate, setIsCheckmate] = useState(false)

  const [currentPlayer, setCurrentPlayer] = useState(WHITE)

  const [resetTimer, setResetTimer] = useState(false);

  const [whitePiecesTaken, setWhitePiecesTaken] = useState([]);
  const [blackPiecesTaken, setBlackPiecesTaken] = useState([]);

  
  return (
    <div className="app">
      <div className="app__inner">
        <h1 className='title'>
          Chess
        </h1>
        <div>
          {isInCheck && <p>Check!</p>}
          {isCheckmate && <p>Checkmate!</p>}
        </div>
        <div className="board">
          <div className='board__pieces-taken'>
            {whitePiecesTaken.map( (piece, idx) => {
              const iconPath = getPieceIconPath(piece, WHITE);
              return (
                <img key={idx} alt={"white " + piece} src={iconPath}></img>
              )
            })}
          </div>
          <Board 
            currentPlayer={currentPlayer} 
            setCurrentPlayer={setCurrentPlayer} 
            setIsInCheck={setIsInCheck}
            setIsCheckmate={setIsCheckmate}
            setError={setError} 
            errorInitialState={errorInitialState}
            setResetTimer={setResetTimer}
            whitePiecesTaken={whitePiecesTaken}
            setWhitePiecesTaken={setWhitePiecesTaken}
            blackPiecesTaken={blackPiecesTaken}
            setBlackPiecesTaken={setBlackPiecesTaken}
          />
          <div className='board__pieces-taken'>
            {blackPiecesTaken.map( (piece, idx) => {
              const iconPath = getPieceIconPath(piece, BLACK);
              return (
                <img key={idx} alt={"black " + piece} src={iconPath}></img>
              )
            })}
          </div>
        </div>
        <div className={"shake error error--" + (error.show ? "show" : "hide")}>
          <p>{error.message}</p>
        </div>
        <div className="turn-information">
          <Timer 
            resetTimer={resetTimer}
            setResetTimer={setResetTimer}
          />
          <p className='"turn-information_player'>
            Player: {currentPlayer}
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
