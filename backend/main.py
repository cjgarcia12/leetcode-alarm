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
    "https://leetcode.com/problems/merge-two-sorted-lists/",
    "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/",
    "https://leetcode.com/problems/valid-anagram/",
    "https://leetcode.com/problems/binary-tree-inorder-traversal/",
    "https://leetcode.com/problems/climbing-stairs/",
    "https://leetcode.com/problems/maximum-subarray/",
    "https://leetcode.com/problems/valid-palindrome/",
    "https://leetcode.com/problems/is-subsequence/",
    "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/",
    "https://leetcode.com/problems/container-with-most-water/",
    "https://leetcode.com/problems/3sum/",
    "https://leetcode.com/problems/minimum-size-subarray-sum/",
    "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
    "https://leetcode.com/problems/substring-with-concatenation-of-all-words/",
    "https://leetcode.com/problems/minimum-window-substring/",
    "https://leetcode.com/problems/valid-sudoku/",
    "https://leetcode.com/problems/spiral-matrix/",
    "https://leetcode.com/problems/rotate-image/",
    "https://leetcode.com/problems/set-matrix-zeroes/",
    "https://leetcode.com/problems/game-of-life/",
    "https://leetcode.com/problems/ransom-note/",
    "https://leetcode.com/problems/isomorphic-strings/",
    "https://leetcode.com/problems/word-pattern/",
    "https://leetcode.com/problems/group-anagrams/",
    "https://leetcode.com/problems/happy-number/",
    "https://leetcode.com/problems/contains-duplicate-ii/",
    "https://leetcode.com/problems/longest-consecutive-sequence/",
    "https://leetcode.com/problems/summary-ranges/",
    "https://leetcode.com/problems/merge-intervals/",
    "https://leetcode.com/problems/insert-interval/",
    "https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/",
    "https://leetcode.com/problems/simplify-path/",
    "https://leetcode.com/problems/min-stack/",
    "https://leetcode.com/problems/evaluate-reverse-polish-notation/",
    "https://leetcode.com/problems/basic-calculator/",
    "https://leetcode.com/problems/linked-list-cycle/",
    "https://leetcode.com/problems/add-two-numbers/",
    "https://leetcode.com/problems/copy-list-with-random-pointer/",
    "https://leetcode.com/problems/reverse-linked-list-ii/",
    "https://leetcode.com/problems/reverse-nodes-in-k-group/",
    "https://leetcode.com/problems/remove-nth-node-from-end-of-list/",
    "https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/",
    "https://leetcode.com/problems/rotate-list/",
    "https://leetcode.com/problems/partition-list/",
    "https://leetcode.com/problems/lru-cache/",
    "https://leetcode.com/problems/maximum-depth-of-binary-tree/",
    "https://leetcode.com/problems/same-tree/",
    "https://leetcode.com/problems/invert-binary-tree/",
    "https://leetcode.com/problems/symmetric-tree/",
    "https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/",
    "https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/",
    "https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/",
    "https://leetcode.com/problems/flatten-binary-tree-to-linked-list/",
    "https://leetcode.com/problems/path-sum/",
    "https://leetcode.com/problems/sum-root-to-leaf-numbers/",
    "https://leetcode.com/problems/binary-tree-maximum-path-sum/",
    "https://leetcode.com/problems/binary-search-tree-iterator/",
    "https://leetcode.com/problems/count-complete-tree-nodes/",
    "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/",
    "https://leetcode.com/problems/binary-tree-right-side-view/",
    "https://leetcode.com/problems/average-of-levels-in-binary-tree/",
    "https://leetcode.com/problems/binary-tree-level-order-traversal/",
    "https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/",
    "https://leetcode.com/problems/minimum-absolute-difference-in-bst/",
    "https://leetcode.com/problems/kth-smallest-element-in-a-bst/",
    "https://leetcode.com/problems/validate-binary-search-tree/",
    "https://leetcode.com/problems/number-of-islands/",
    "https://leetcode.com/problems/surrounded-regions/",
    "https://leetcode.com/problems/clone-graph/",
    "https://leetcode.com/problems/evaluate-division/",
    "https://leetcode.com/problems/course-schedule/",
    "https://leetcode.com/problems/course-schedule-ii/",
    "https://leetcode.com/problems/snakes-and-ladders/",
    "https://leetcode.com/problems/minimum-genetic-mutation/",
    "https://leetcode.com/problems/word-ladder/",
    "https://leetcode.com/problems/implement-trie-prefix-tree/",
    "https://leetcode.com/problems/design-add-and-search-words-data-structure/",
    "https://leetcode.com/problems/word-search-ii/",
    "https://leetcode.com/problems/letter-combinations-of-a-phone-number/",
    "https://leetcode.com/problems/combinations/",
    "https://leetcode.com/problems/permutations/",
    "https://leetcode.com/problems/combination-sum/",
    "https://leetcode.com/problems/n-queens-ii/",
    "https://leetcode.com/problems/generate-parentheses/",
    "https://leetcode.com/problems/word-search/",
    "https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/",
    "https://leetcode.com/problems/sort-list/",
    "https://leetcode.com/problems/construct-quad-tree/",
    "https://leetcode.com/problems/merge-k-sorted-lists/",
    "https://leetcode.com/problems/maximum-subarray/",
    "https://leetcode.com/problems/maximum-sum-circular-subarray/",
    "https://leetcode.com/problems/search-insert-position/",
    "https://leetcode.com/problems/search-a-2d-matrix/",
    "https://leetcode.com/problems/find-peak-element/",
    "https://leetcode.com/problems/search-in-rotated-sorted-array/",
    "https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/",
    "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/",
    "https://leetcode.com/problems/median-of-two-sorted-arrays/",
    "https://leetcode.com/problems/kth-largest-element-in-an-array/",
    "https://leetcode.com/problems/ipo/",
    "https://leetcode.com/problems/find-k-pairs-with-smallest-sums/",
    "https://leetcode.com/problems/find-median-from-data-stream/",
    "https://leetcode.com/problems/add-binary/",
    "https://leetcode.com/problems/reverse-bits/"
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