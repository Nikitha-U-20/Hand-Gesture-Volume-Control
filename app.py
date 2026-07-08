from flask import Flask, render_template, Response, request
from gesture_control import generate_frames
import os
import time
from voice_control import listen_command, process_command

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/gesture')
def gesture():
    return render_template("gesture.html")

@app.route('/video')
def video():
    return Response(generate_frames(),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/calibration', methods=['GET','POST'])
def calibration():

    if request.method == 'POST':

        min_vol = request.form['min_vol']
        max_vol = request.form['max_vol']

        with open("calibration.txt","w") as f:
            f.write(min_vol + "," + max_vol)

    return render_template("calibration.html")

@app.route('/remove_calibration', methods=['POST'])
def remove_calibration():

    if os.path.exists("calibration.txt"):
        os.remove("calibration.txt")

    return render_template("calibration.html")

@app.route('/voice_command')
def voice_command():

    command = listen_command()
    result = process_command(command)

    return {"result": result}

@app.route('/audio')
def audio():
    return render_template('audio.html')

from audio_mapping import get_audio_level

@app.route('/audio_data')
def audio_data():
    level, muted = get_audio_level()
    return {"level": level, "muted": muted}

@app.route('/system')
def system():

    calibration_status = "Not Set"

    if os.path.exists("calibration.txt"):
        with open("calibration.txt","r") as f:
            data = f.read()
            calibration_status = "Active (" + data + ")"

    return render_template("system.html",
                           calibration=calibration_status,
                           camera="Active",
                           microphone="Active")

if __name__ == "__main__":
    app.run(debug=True)