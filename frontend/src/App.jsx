import { useState, useEffect } from "react";
import axios from "axios";

export default function App() {
  const [alarmActive, setAlarmActive] = useState(false);
  const [problem, setProblem] = useState("");
  const [audio, setAudio] = useState(null);
  const [sleepHours, setSleepHours] = useState(1);
  const [username, setUsername] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [showPlayButton, setShowPlayButton] = useState(false);

  useEffect(() => {
    if (alarmActive) {
      const interval = setInterval(() => {
        axios.get("http://127.0.0.1:5000/check-alarm", { params: { username } })
          .then(res => {
            if (res.data.alarm) {
              setProblem(res.data.problem);
              setAlarmActive(true);
              const alarmSound = new Audio("/iphone_alarm.mp3");
              alarmSound.loop = true;
              alarmSound.play().catch(() => setShowPlayButton(true));
              setAudio(alarmSound);
              clearInterval(interval);
            }
          })
          .catch(console.error);
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [alarmActive, username]);

  const setAlarm = async () => {
    if (!username) {
      setErrorMessage("Enter your LeetCode username.");
      return;
    }

    try {
      await axios.post("http://127.0.0.1:5000/set-alarm", {
        sleep_hours: sleepHours,
        leetcode_username: username
      });
      setAlarmActive(true);
      setErrorMessage("");
    } catch (error) {
      setErrorMessage("Failed to set alarm.");
    }
  };

  const stopAlarm = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:5000/stop-alarm", {
        leetcode_username: username
      });

      if (res.data.success) {
        setAlarmActive(false);
        setProblem("");
        setErrorMessage(""); // Clear error message on success
        if (audio) {
          audio.pause();
          audio.currentTime = 0;
        }
        setShowPlayButton(false);
      }
    } catch (error) {
      setErrorMessage(error.response?.data?.error || "Error stopping alarm.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center w-screen h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-4">LeetCode Alarm Clock ⏰</h1>

      {!alarmActive ? (
        <div className="flex flex-col items-center gap-4">
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="LeetCode Username"
            className="p-2 rounded bg-white text-black"
          />
          <input
            type="number"
            value={sleepHours}
            onChange={(e) => setSleepHours(e.target.valueAsNumber)}
            min="1"
            className="p-2 rounded bg-white text-black"
          />
          <button onClick={setAlarm} className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded">
            Set Alarm
          </button>
          {errorMessage && <p className="text-red-400">{errorMessage}</p>}
        </div>
      ) : (
        <div className="text-center">
          <h2 className="text-xl font-semibold mb-2">🚨 Solve This Problem! 🚨</h2>
          <a href={problem} target="_blank" rel="noopener noreferrer" className="text-yellow-400 underline">
            {problem}
          </a>
          {showPlayButton && (
            <button onClick={() => audio.play().catch(console.error)} className="mt-2 bg-green-500 px-4 py-2 rounded">
              Play Alarm
            </button>
          )}
          <button onClick={stopAlarm} className="mt-4 bg-red-500 hover:bg-red-600 px-4 py-2 rounded block mx-auto">
            Stop Alarm
          </button>
          {errorMessage && <p className="text-red-400">{errorMessage}</p>}
        </div>
      )}
    </div>
  );
}