from flask import Flask
from flask import render_template, Response, jsonify
import time
import cv2
from importlib import import_module
from camera import LocalCamera

# vars
DISABLE_FUNCS = False
FUNC_PANELS = ['controler.html', 'monitor.html']
DISABLE_CAMERA = False | DISABLE_FUNCS 

PORT = 8090
#-----------------------------------------------
# camera
cap = LocalCamera()
if DISABLE_CAMERA == False:
    cap.open()
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

# App
app = Flask(__name__)
@app.route("/")
def home():
    panels =[]
    bk_colors = ['lightcyan', 'lightgray', 'lightpink']
    for i in range(2):
        panels.append({
            "url":FUNC_PANELS[i],
            "bk_color":bk_colors[i]
            })
    #print(render_template("home.html", panels = panels, dis_funcs = DISABLE_FUNCS))
    return render_template("home.html", panels = panels, dis_funcs = DISABLE_FUNCS)
 
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(
        cap.gen(),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/info', methods=["GET"])
def info():
    json_data = dict()
    json_data["frame_count"] = cap.frame_count
    return jsonify(json_data)

@app.route('/camera/info', methods=["GET"])
def camera_info():
    json_data = dict()
    json_data["frame_rate"] = cap.frame_rate
    cap.set_performance()
    return jsonify(json_data)

@app.route("/monitor")
def monitor():
    return render_template("monitor.html")

@app.route("/controler")
def controler():
    return render_template("controler.html")

app.run(port=PORT, debug=True)
