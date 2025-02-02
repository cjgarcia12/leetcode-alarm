from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time
import requests
import threading

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

leetcode_problems = [
    "https://leetcode.com/problems/two-sum/",
    "https://leetcode.com/problems/reverse-linked-list/",
    "https://leetcode.com/problems/longest-palindromic-substring/",
    "https://leetcode.com/problems/valid-parentheses/",
    "https://leetcode.com/problems/merge-two-sorted-lists/"
]

# Store alarms per user: {username: {trigger_time, problem, triggered}}
alarms = {}
lock = threading.Lock()


def get_problem_slug(url):
    parts = url.strip("/").split("/")
    if "problems" in parts:
        return parts[parts.index("problems") + 1]
    return None


@app.route("/set-alarm", methods=["POST"])
def set_alarm():
    data = request.get_json()
    try:
        sleep_hours = float(data.get("sleep_hours", 0.00027777777))  # Cast to float
    except ValueError:
        return jsonify({"error": "Invalid sleep_hours value"}), 400
    username = data.get("leetcode_username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    sleep_seconds = sleep_hours * 3600
    trigger_time = time.time() + sleep_seconds
    problem = random.choice(leetcode_problems)

    with lock:
        alarms[username] = {
            "trigger_time": trigger_time,
            "problem": problem,
            "triggered": False
        }

    return jsonify({"message": "Alarm set!", "problem": problem})


@app.route("/check-alarm", methods=["GET"])
def check_alarm():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Username required"}), 400

    with lock:
        alarm = alarms.get(username)
        if not alarm:
            return jsonify({"alarm": False})

        current_time = time.time()
        if current_time >= alarm["trigger_time"] and not alarm["triggered"]:
            alarm["triggered"] = True

        return jsonify({
            "alarm": alarm["triggered"],
            "problem": alarm["problem"] if alarm["triggered"] else None
        })


def check_leetcode_submission(username, problem_url):
    problem_slug = get_problem_slug(problem_url)
    if not problem_slug:
        return False

    try:
        query = {
            "query": """
            query recentAcSubmissions($username: String!) {
                recentAcSubmissionList(username: $username) {
                    title
                }
            }
            """,
            "variables": {"username": username}
        }
        resp = requests.post("https://leetcode.com/graphql", json=query)
        data = resp.json()

        submissions = data.get("data", {}).get("recentAcSubmissionList", [])
        for sub in submissions:
            title_slug = sub["title"].lower().replace(" ", "-")
            if title_slug == problem_slug:
                return True
        return False
    except Exception as e:
        print("Error checking submissions:", e)
        return False


@app.route("/stop-alarm", methods=["POST"])
def stop_alarm():
    data = request.get_json()
    username = data.get("leetcode_username")

    if not username:
        return jsonify({"error": "Username required"}), 400

    with lock:
        alarm = alarms.get(username)
        if not alarm or not alarm["triggered"]:
            return jsonify({"error": "Alarm not active"}), 400

        problem_url = alarm["problem"]
        if check_leetcode_submission(username, problem_url):
            del alarms[username]
            return jsonify({"success": "Alarm stopped!"})
        else:
            return jsonify({"error": "Solve the problem first!"}), 403


if __name__ == "__main__":
    app.run(debug=True)