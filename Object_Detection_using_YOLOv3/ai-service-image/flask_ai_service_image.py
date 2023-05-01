from flask import Flask, jsonify, request
from waitress import serve

from PIL import Image
import datetime
import tensorflow as tf
import numpy as np
import os
import io

import config_ai_service_image as cfg
import yolo3_model_for_inferencing

#os.chdir(cfg.root_directory_windows) # for windows
os.chdir(cfg.root_directory_ubuntu) # for ubuntu

import datetime
def current_datetime(text=""):
    datetime_string = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    return text + " @ " + datetime_string

app = Flask(__name__)

yoloClass = yolo3_model_for_inferencing.YOLO()

api_counter_all = 0
api_counter_detected = 0
api_counter_undetected = 0
api_counter_error = 0

@app.route('/')
def index():

    global api_counter_all
    global api_counter_detected
    global api_counter_undetected
    global api_counter_error

    # Get current working directory
    sentences = ["AI Service(ai-service-image) Server"]
    sentences.append(current_datetime())
    sentences.append(os.getcwd())
    sentences.append(f'API Counter : All = {api_counter_all}')
    sentences.append(f'API Counter : Detected = {api_counter_detected}')
    sentences.append(f'API Counter : Undetected = {api_counter_undetected}')
    sentences.append(f'API Counter : Error = {api_counter_error}')

    return "<p>".join(sentences)

@app.route('/detect/image', methods=['POST'])
def detect_image_restapi():

    global api_counter_all
    global api_counter_detected
    global api_counter_undetected
    global api_counter_error
    api_counter_all += 1

    try:
        img_binary = request.get_data()
        image_file = io.BytesIO(img_binary)
        image = Image.open(image_file)

        info_detected = yoloClass.get_score(image)

        detection_score = 0
        if len(info_detected) != 0:
            detection_score = np.max(info_detected)

        # if object is detected
        if detection_score > 0.20:
            json_data = { "object_detected" : True }
            api_counter_detected += 1
        else:
            json_data = { "object_detected" : False }
            api_counter_undetected += 1

        return jsonify(json_data), 200
    except Exception as e:
        api_counter_error += 1
        return jsonify(error="Unexpected error:" + str(e)), 400

if __name__ == '__main__':
    serve(app, host=cfg.host_num, port=cfg.port_num)
    #app.run(host=cfg.host_num, port=cfg.port_num, debug=True)
