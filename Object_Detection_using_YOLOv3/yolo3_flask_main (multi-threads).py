from flask import Flask, Response, jsonify, send_file,request
from waitress import serve
import concurrent.futures

import datetime
from PIL import Image
from timeit import default_timer
from yolo3_class import YOLO
import yolo3_config as cfg
from tensorflow.python.framework.ops import disable_eager_execution
import tensorflow as tf
import pandas as pd

import io
import numpy as np
import os

os.chdir(cfg.root_directory_windows) # for windows
#os.chdir(cfg.root_directory_ubuntu) # for ubuntu

# Application parameters
# Configure before runing the application
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

def check_filepath(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False

if check_filepath(cfg.model_path) == False:
    exit("Error: model path not found at {}".format(cfg.model_path))

@app.route('/')
def index():

    # get current working directory
    cwd = os.getcwd()
    print(cwd)

    # Print the current date and time in the format:
    # "YYYY-MM-DD HH:MM:SS.microseconds"
    datetime_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    print("AI-Service-Server @ Current date and time:", datetime_string)

    image = Image.open("ai-service-server.jpg")
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)
    return send_file(buffer, mimetype='image/jpeg')

@app.route('/popup/image/<fileName>')
def popup_image(fileName):

    if check_filename(image_path + fileName) == False:
        return jsonify(error="File not found:" + fileName), 404 

    start = default_timer()

    print(f"AI-Service : Printing image @ image folder, {image_path + fileName}")

    image = Image.open(image_path + fileName)

    image_detected, _ = yoloClass.demo_image(image)

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
        return jsonify(error="File not found:" + fileName), 404 

    start = default_timer()

    print(f"AI-Service : Detecting image @ image folder, {image_path + fileName}")

    image = Image.open(image_path + fileName)

    info_detected = yoloClass.detect_image(image)
    print(info_detected)

    detection_score = 0
    if len(info_detected) != 0:
        detection_score = np.max(info_detected)

    print("# of object detected:", len(info_detected))
    print("Detection score:", detection_score)

    # if object is detected
    if detection_score > 0.20:
        json_data = { "object_detected" : True }
    else:
        json_data = { "object_detected" : False }

    end = default_timer()
    print("Time duration(in seconds):")
    print(end - start)

    return jsonify(json_data), 200

@app.route('/demo/image/<fileName>')
def demo_image(fileName):

    if check_filename(image_path + fileName) == False:
        return jsonify(error="File not found:" + fileName), 404 

    start = default_timer()

    print(f"AI-Service : Printing image @ image folder, {image_path + fileName}")

    image = Image.open(image_path + fileName)

    image_detected, _ = yoloClass.demo_image(image)

    image_io = io.BytesIO()
    image_detected.save(image_io, 'JPEG')
    image_io.seek(0)

    end = default_timer()
    print("Time duration(in seconds):")
    print(end - start)

    return send_file(image_io, mimetype='image/jpeg')

def thread_yolo_process(img_binary):
    image_file = io.BytesIO(img_binary)
    image = Image.open(image_file)
    info_detected = yoloClass.detect_image(image)
    # if Class box presents
    detection_score = 0
    if len(info_detected) != 0:
        detection_score = np.max(info_detected)
    # if object is detected
    if detection_score > 0.20:
        json_data = { "object_detected" : True }
    else:
        json_data = { "object_detected" : False }
    return json_data

@app.route('/detect/image', methods=['POST'])
def detect_image_restapi():

    try:
        img_binary = request.get_data()

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor: # cfg.max_threads
            future = executor.submit(thread_yolo_process, img_binary)
            json_data = future.result()

        return jsonify(json_data), 200
    except Exception as e:
        return jsonify(error="Unexpected error:" + str(e)), 400

if __name__ == '__main__':
    #serve(app, host=cfg.host_num, port=cfg.port_num)
    app.run(host=cfg.host_num, port=cfg.port_num, debug=True)
