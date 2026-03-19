from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import csv
import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 홈 페이지 (로그인)
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        name = request.form.get("name")

        users = load_users()
        if student_id in users and users[student_id] == name:
            session["student_id"] = student_id
            session["name"] = name
            return redirect(url_for("attendance_page"))
        else:
            return render_template("home.html", error="학번 또는 이름이 올바르지 않습니다.")
    return render_template("home.html")

# 출석 페이지
@app.route("/attendance", methods=["GET"])
def attendance_page():
    if "student_id" not in session:
        return redirect(url_for("home"))
    return render_template("attendance.html", student_name=session["name"])

# 출석 처리 API
@app.route("/stamp_attendance", methods=["POST"])
def stamp_attendance():
    data = request.get_json()
    student_id = data.get("student_id")
    subject = data.get("subject", "공통출석")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not student_id:
        return jsonify({"error": "학생 ID 없음"}), 400

    users = load_users()
    if student_id not in users:
        return jsonify({"error": "유효하지 않은 학생 ID입니다."}), 400

    file_path = "attendance_log.csv"
    need_header = not os.path.exists(file_path) or os.stat(file_path).st_size == 0

    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if need_header:
            writer.writerow(["student_id", "subject", "timestamp"])
        writer.writerow([student_id, subject, now])

    return jsonify({"message": "출석 완료!"})

# 로그아웃
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# 사용자 로드
def load_users():
    users = {}
    if os.path.exists("users.csv"):
        with open("users.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row["student_id"]] = row["name"]
    return users

# 루트 리디렉션
@app.route("/")
def root():
    return redirect(url_for("home"))

# HTTPS 실행
if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=5000, ssl_context=("cert.pem", "key.pem"))
    app.run(host="0.0.0.0", port=5000, debug=True)
