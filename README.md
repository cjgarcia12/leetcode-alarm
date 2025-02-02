**Project Name**: LeetCode Alarm Clock ⏰  
**Description**: An alarm clock that won't stop ringing until you solve a LeetCode problem. Built with Flask (Python backend) and React (frontend).

**Features**:  
- Sets customizable alarm duration  
- Randomly selects LeetCode problems  
- Verifies submissions via LeetCode's API  
- Persistent alarm until problem is solved  
- User-specific alarm tracking  
- Handles browser audio autoplay restrictions  

**Installation**:  
 
1. Clone repo  
2. cd to the backend directory:

   ```cd backend```
3. Create virtual environment:  
   ```python -m venv venv```  
3. Activate venv:  
   - Mac/Linux: ```source venv/bin/activate```  
   - Windows: ```venv\Scripts\activate```  
4. Install dependencies: ```pip install flask flask-cors requests```  
5. Run: ```python main.py```  

*Frontend (React)*:  
1. Navigate to frontend directory  
2. Install dependencies: ```npm install axios react react-dom```  
3. Run: ```npm start```  

**Usage**:  
1. Enter LeetCode username  
2. Set alarm duration (hours)  
3. Solve problem when alarm triggers  
4. Click "Stop Alarm" after solving  

**API Endpoints**:  
- POST /set-alarm : {sleep_hours, leetcode_username}  
- GET /check-alarm?username= : Poll alarm status  
- POST /stop-alarm : {leetcode_username}  

**Troubleshooting**:  
- Alarm not triggering? Check backend is running  
- Submission not detected? LeetCode API might delay 2-3 minutes  
- Audio issues? Click "Play Alarm" button due to browser restrictions  

**Contributing**:  
1. Fork repository  
2. Create feature branch  
3. Submit PR with detailed description  

**License**: MIT  
**Acknowledgments**: LeetCode API, Flask-React integration patterns  

---

Replace placeholder values (like your repo URL) and add screenshots/demo links when ready. You might want to add system requirements (Python 3.8+, Node 16+) if needed.