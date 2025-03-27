from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy user attendance data
USER_ATTENDANCE = {
    "Alice": "Present",
    "Bob": "Absent",
    "Charlie": "Present",
    "Diana": "Absent",
    "Edward": "Present",
}

@app.route('/attendance/<string:username>', methods=['GET'])
def get_attendance(username):
    """Fetch attendance status by username"""
    status = USER_ATTENDANCE.get(username, "Not Found")

    if status == "Not Found":
        return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"username": username, "status": status})

if __name__ == '__main__':
    app.run(debug=True)  # Runs on http://127.0.0.1:5000
