from flask import Flask, jsonify, request
from waitress import serve

import datetime
from PIL import Image
from timeit import default_timer
import config_EfficientNet_Image_Classification as cfg
import model_EfficientNet_Image_Classification as model_finetuned
import numpy as np
import io
import os

os.chdir(cfg.root_directory_windows) # for windows
#os.chdir(cfg.root_directory_ubuntu) # for ubuntu

def check_filepath(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False

if check_filepath(cfg.model_path) == False:
    exit("Error: model path not found at {}".format(cfg.model_path))

model_finetuned.create_model_instance(cfg.model_path)

app = Flask(__name__)

@app.route('/')
def index():

    # get current working directory
    cwd = os.getcwd()

    print(cwd)

    # Print the current date and time in the format:
    # "YYYY-MM-DD HH:MM:SS.microseconds"
    datetime_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    return "AI Service Server @ Current date and time: " + datetime_string

@app.route('/classify/image', methods=['POST'])
def classify_image_api():

    try:
        img_binary = request.get_data()
        image_file = io.BytesIO(img_binary)
        image = Image.open(image_file)

        start = default_timer()

        #print(f"AI-Service : Sending detected result @ requested file")

        predicted_result = model_finetuned.get_class(image)

        # Get the predicted label name: class1(0), class2(1), class3(2)
        label_map = {0: "Cat", 1: "Dog", 2: "Human"}
        predicted_label_id = np.argmax(predicted_result)
        predicted_label_name = label_map[predicted_label_id]

        json_data = { "class" : predicted_label_name }

        return jsonify(json_data), 200
    except Exception as e:
        return jsonify(error="Unexpected error:" + str(e)), 400

if __name__ == '__main__':
    #serve(app, host=cfg.host_num, port=cfg.port_num)
    app.run(host=cfg.host_num, port=cfg.port_num, debug=True)
