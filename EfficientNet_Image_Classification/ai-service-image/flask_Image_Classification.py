from flask import Flask, jsonify, request
from waitress import serve

import datetime
from PIL import Image
import config_Image_Classification as cfg
import model_Image_Classification as model_finetuned
import numpy as np
import io
import os

os.chdir(cfg.root_directory_windows) # for windows
#os.chdir(cfg.root_directory_ubuntu) # for ubuntu

import datetime
def current_datetime(text=""):
    datetime_string = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    return text + " @ " + datetime_string

def check_filepath(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False

if check_filepath(cfg.model_path) == False:
    exit("Error: model path not found at {}".format(cfg.model_path))

model_finetuned.create_model_instance(cfg.model_path)

app = Flask(__name__)

api_counter_all = 0
api_counter_ok_safe = 0
api_counter_ok_unsafe = 0
api_counter_error = 0

@app.route('/')
def index():

    global api_counter_all
    global api_counter_ok_safe
    global api_counter_ok_unsafe
    global api_counter_error

    # Get current working directory
    sentences = ["AI Service(ai-service-image) Server"]
    sentences.append(current_datetime())
    sentences.append(os.getcwd())
    sentences.append(f'API Counter : All = {api_counter_all}')
    sentences.append(f'API Counter : OK(Safe) = {api_counter_ok_safe}')
    sentences.append(f'API Counter : OK(Unsafe) = {api_counter_ok_unsafe}')
    sentences.append(f'API Counter : Error = {api_counter_error}')

    return "<p>".join(sentences)

@app.route('/classify/image', methods=['POST'])
def classify_image_api():

    global api_counter_all
    global api_counter_ok_safe
    global api_counter_ok_unsafe
    global api_counter_error
    api_counter_all += 1

    try:
        img_binary = request.get_data()
        image_file = io.BytesIO(img_binary)
        image = Image.open(image_file)

        predicted_result = model_finetuned.get_class(image)

        # Get the predicted label name
        label_map = {0: "safe", 1: "unsafe"}
        predicted_label_id = np.argmax(predicted_result)
        predicted_label_name = label_map[predicted_label_id]

        if predicted_label_name=="unsafe":
            predicted_value = False
            api_counter_ok_unsafe += 1
        else:
            predicted_value = True
            api_counter_ok_safe += 1
        json_data = { "safe" : predicted_value }

        return jsonify(json_data), 200
    except Exception as e:
        api_counter_error += 1
        return jsonify(error="Unexpected error:" + str(e)), 400

if __name__ == '__main__':
    #serve(app, host=cfg.host_num, port=cfg.port_num)
    app.run(host=cfg.host_num, port=cfg.port_num, debug=True)
