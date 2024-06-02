import React, {useState, useEffect} from "react";

export default function Timer({resetTimer, setResetTimer}) {
    const [timer, setTimer] = useState({ time: 0, formattedTime: ""});
    const [isTimerRunning, setIsTimerRunning] = useState(true)

    useEffect(() => {
        if (resetTimer){
            setTimer({ time: 0, formattedTime: ""});
        }

        setResetTimer(false)
        
    }, [resetTimer])

    useEffect(() => {
        let intervalId;
        if (isTimerRunning) {
          intervalId = setInterval(() => 
            {
              const time = timer.time + 1
    
              const hours = Math.floor(time / 360000);
              const minutes = Math.floor((time % 360000) / 6000);
              const seconds = Math.floor((time % 6000) / 100);
              
              const formattedMinutes = String(minutes).padStart(2, '0');
              const formattedSeconds = String(seconds).padStart(2, '0');
    
              const formattedTime = `${hours}:${formattedMinutes}:${formattedSeconds}`
              setTimer({time: time, formattedTime: formattedTime});
            }, 10);
        }
        return () => clearInterval(intervalId);
    }, [isTimerRunning, timer]);

    return (
        <p className="timer">
            Elapsed Time: {timer.formattedTime}
        </p>
    );
}