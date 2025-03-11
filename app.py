from flask import Flask, render_template, request, redirect, url_for, session, send_file
import cv2
import os
from generate_pdf import create_pdf

app = Flask(__name__)
app.secret_key = "secret_key"

# User credentials (Multiple users)
USERS = {
    "prince": "50125",
    "pritam": "17280",
    "shagun": "17289",
    "mohit": "11438",
    "aditya": "14583",
    "jagjit": "10810",
    "yenumula bala": "10571",
    "bharat": "14818",
    "ravinder": "16181",
    "sahil": "14873",
    "komal": "12005",
    "deepak": "80053",
    "ravi": "14557",
    "aman": "16421",
    "parshant": "80050",
    "pranav": "50037",
    "kushagar": "10429",
    "kapil": "80032",
    "mannat": "12713",
    "keshav": "16461",
    "anubabh": "12402",
    "kurumaddali": "10990",
    "kasak": "10584",
    "rishabh": "16254",
    "bhaviya": "17195",
    "ayush": "80086",
    "kashish": "14636",
    "sumit": "10406",
    "kanishk": "10804",
    "manjeet": "10015",
    "anmol": "11897",
    "sakshi": "12460",
    "atul": "16177",
    "sagar": "16655",
    "aryan": "16369",
    "monika": "17771"
}


# Home (Login Page)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in USERS and USERS[username] == password:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("form"))
        return render_template("login.html", error="Invalid Credentials! Try Again.")
    
    return render_template("login.html")

# Form Page (User Info Input)
@app.route("/form", methods=["GET", "POST"])
def form():
    if "logged_in" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        session["name"] = request.form["name"]
        session["age"] = request.form["age"]
        session["blood_group"] = request.form["blood_group"]
        return redirect(url_for("capture"))
    
    return render_template("form.html", username=session["username"])

# Capture Image
@app.route("/capture")
def capture():
    if "logged_in" not in session:
        return redirect(url_for("login"))

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    img_path = "static/captured_image.jpg"
    
    if ret:
        cv2.imwrite(img_path, frame)
    cap.release()

    session["image_path"] = img_path
    return redirect(url_for("preview"))

# Show Preview Before Downloading PDF
@app.route("/preview")
def preview():
    if "logged_in" not in session:
        return redirect(url_for("login"))

    # Simulating sensor data (no actual pulse sensor connected)
    sensor_data = None  # Replace this with actual sensor data when available

    return render_template(
        "preview.html",
        username=session.get("username"),
        name=session.get("name"),
        age=session.get("age"),
        blood_group=session.get("blood_group"),
        image_path=session.get("image_path"),
        sensor_data=sensor_data  # Pass sensor data (None for now)
    )

# Download PDF
@app.route("/download")
def download():
    if "logged_in" not in session:
        return redirect(url_for("login"))

    pdf_path = create_pdf(session["name"], session["age"], session["blood_group"], session["image_path"])
    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
