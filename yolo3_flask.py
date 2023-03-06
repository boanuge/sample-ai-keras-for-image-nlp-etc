from flask import Flask, Response, jsonify, send_file
from waitress import serve

from PIL import Image
from timeit import default_timer
from yolo3_class import YOLO
import yolo3_config as cfg
from tensorflow.python.framework.ops import disable_eager_execution
import tensorflow as tf

import io
import numpy as np
import os

# os.chdir(os.getcwd() + "/") # for windows
os.chdir(cfg.root_directory_windows) # for windows
# os.chdir(cfg.root_directory_ubuntu) # for ubuntu

# Application parameters
# Configure before runing the application
# image_path = "images_test/"
image_path = cfg.yolo_image_path

# Warning log disable
if cfg.yolo_error_log_disable:
    os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
    disable_eager_execution()

# Future warning log disable
if cfg.yolo_future_error_log_disable:
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

app = Flask(__name__)

yoloClass = YOLO()

def check_filename(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False



@app.route('/')
def index():

    # get current working directory
    cwd = os.getcwd()

    # get files in directory
    files = os.listdir(cwd)

    print(files)

    return "AI-Service Server"

@app.route('/print/image/<fileName>')
def print_image(fileName):

    if check_filename(image_path + fileName) == False:
        return jsonify(error="File not found: " + fileName), 404 

    print(f"AI-Service : Printing an image @ image folder, {image_path + fileName}")
    
    with open(image_path + fileName, "rb") as f:
        image = f.read()
    return Response(image, content_type="image/jpeg")



@app.route('/popup/image/<fileName>')
def popup_image(fileName):

    if check_filename(image_path + fileName) == False:
        return jsonify(error="File not found: " + fileName), 404 

    start = default_timer()

    print(f"AI-Service : Printing detected image @ image folder, {image_path + fileName}")

    image = Image.open(image_path + fileName)

    # yoloClass.popup_image(image)
    
    image_detected = yoloClass.popup_image(image)
    #image_detected.show()
    #return "The detected image will popup."

    image_io = io.BytesIO()
    image_detected.save(image_io, 'JPEG')
    image_io.seek(0)

    end = default_timer()
    print("Time duration(in seconds):")
    print(end - start)

    return send_file(image_io, mimetype='image/jpeg')



@app.route('/detect/image/<fileName>')
def detect_image(fileName):

    if check_filename(image_path + fileName) == False:
        return jsonify(error="File not found: " + fileName), 404 

    start = default_timer()

    print(f"AI-Service : Sending detected result @ image folder, {image_path + fileName}")

    image = Image.open(image_path + fileName)

    info_detected = yoloClass.detect_image(image)
    print(info_detected)

    detection_score = 0
    if len(info_detected) != 0:
        detection_score = np.max(info_detected)

    print("# of detected object:", len(info_detected))
    print("Detection score:", detection_score)

    # if an object is detected
    if detection_score > 0.30:
        json_data = {"detected" : "true"}
    else:
        json_data = {"detected" : "false"}

    end = default_timer()
    print("Time duration(in seconds):")
    print(end - start)

    return jsonify(json_data), 200



if __name__ == '__main__':
    #serve(app, host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port=5555, debug=True)
