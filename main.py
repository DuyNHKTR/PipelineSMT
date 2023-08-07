import os
import json
import sys
import time
import cv2
from backend.function import *


from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit
from backend.function import recognize_faces
from backend.function import *
from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
socketio = SocketIO(app)

def load_users():
    with open('static/users.json', 'r', encoding='utf-8') as file:
        users_data = json.load(file)
    return users_data

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    global users_data
    users_data = load_users()
    user = next((user for user in users_data if user["username"] == username and user["password"] == password), None)

    if user:
        session["isLoggedIn"] = True
        session["face"] = False
        session["user"] = user  # Store the user data in the session
        return redirect("/dashboard")
    else:
        return redirect("/?error=invalid_credentials")

@app.route("/dashboard")
def dashboard():
    if not session.get("isLoggedIn"):
        return redirect("/")
    user = session.get("user")
    if not user:
        return redirect("/?error=user_not_found")
    return render_template("dashboard.html", user=user)

@app.route("/redirect_dashboard")
def redirect_dashboard():
    user_face = session.get("user_face")
    return render_template('dashboard.html', user=user_face)


@app.route('/faceid')
def faceid():
    users_data = load_users()
    capture = cv2.VideoCapture(-1,cv2.CAP_V4L)
    prev_frame_time = 0
    new_frame_time = 0
    while True:
        ret, frame = capture.read()
        if ret:
            new_frame_time = time.time()
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time
            fps = int(fps)
            fps = str(fps)
            print("FPS is :",fps)
            gal_dir = "./static/images/face_img/"
            results = recognize_faces(gal_dir,frame)
            if len(results) == 1:
                for result in results:
                    _, _, ids = result
                    name, _, _, _ = ids
                    print("NAME JSON: ",[data['image'].split(".")[0] for data in users_data])
                    if name in [data['image'].split(".")[0] for data in users_data]:
                        user_face = next((user for user in users_data if user["image"].split(".")[0] == name), None)
                        session["user_face"] = user_face
                        session["isLoggedIn"] = True
                        session["face"] = True
                        # session["user"] = user
                        return redirect("/redirect_dashboard")
            
# @socketio.on("connect", namespace="/second_display")
# def handle_second_display_connect():
#     if session.get("isLoggedIn"):
#         if session.get("face"):
#             user = session["user_face"]
#             emit("user_login", {"fullName": user["fullName"], "title": user["title"]})
#         user = session["user"]
#         emit("user_login", {"fullName": user["fullName"], "title": user["title"]})

@app.route("/second_display")
def second_display():
    
    if session.get("face") == False:
        if session.get("isLoggedIn"):
            user = {
                "fullName": session["user"]["fullName"],
                "title": session["user"]["title"]
            }
    elif session.get("face") == True:
        if session.get("isLoggedIn"):
            user = {
                "fullName": session["user_face"]["fullName"],
                "title": session["user_face"]["title"]
            }
    return render_template("second_display.html", user = user) 
    # return render_template("second_display.html")
        
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    socketio = SocketIO(app)
    app.run(host="0.0.0.0", port=8000, threaded=True, debug=True)
