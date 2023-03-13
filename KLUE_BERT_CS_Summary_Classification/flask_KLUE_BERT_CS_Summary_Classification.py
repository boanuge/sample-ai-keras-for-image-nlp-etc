from flask import Flask, jsonify, request
from waitress import serve

import datetime
from timeit import default_timer
import config_KLUE_BERT_CS_Summary_Classification as cfg
import model_KLUE_BERT_CS_Summary_Classification as model_finetuned
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

    return "AI-Service Server @ Current date and time: " + datetime_string

@app.route("/classify/cs_summary", methods=["POST"])
def classify_labs_cs_summary():

    start = default_timer()

    data = request.get_json()

    print(data)

    if data is not None and "cs_summary" in data:
        text = data["cs_summary"]
    else:
        text = "Invalid JSON data"

    label = model_finetuned.get_label(text)

    json_data = { "classification" : label }

    end = default_timer()
    print("Time duration(in seconds):", end - start)

    return jsonify(json_data), 200

if __name__ == '__main__':
    #serve(app, host=cfg.host_num, port=cfg.port_num)
    app.run(host=cfg.host_num, port=cfg.port_num, debug=True)
