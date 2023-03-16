from flask import Flask, jsonify, request
from waitress import serve

import datetime
from timeit import default_timer
import config_KoGPT2_CS_Comment_Generation as cfg
import model_KoGPT2_CS_Comment_Generation as model_finetuned
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

@app.route("/generate/cs_comment", methods=["POST"])
def classify_labs_cs_summary():

    start = default_timer()

    data = request.get_json()

    print(data)
    '''
    {
        "cs_refund" : "환불 요청 안함",
        "cs_time" : "탑승 전",
        "cs_error" : "엑셀,바퀴",
        "cs_reason" : "엑셀이 작동을 안해요"
    }
    '''

    JSON_error = True

    # 예) 환불 요청 안함 | 탑승 전 | 엑셀,바퀴 | 엑셀이 작동을 안해요
    if data is not None and "cs_reason" in data:
        if "cs_refund" in data:
            if "cs_time" in data:
                if "cs_error" in data:
                    cs_reason = data["cs_reason"] # 엑셀이 작동을 안해요
                    cs_refund = data["cs_refund"] # 환불 요청 안함
                    cs_time = data["cs_time"] # 탑승 전
                    cs_error = data["cs_error"] # 엑셀,바퀴
                    JSON_error = False

    if JSON_error:
        json_data = { "error" : "Invalid JSON data" }
        return jsonify(json_data), 400

    text = cs_refund + "|" + cs_time + "|" + cs_error + "|" + cs_reason

    print(text)

    text = model_finetuned.get_text(text)

    json_data = { "text" : text }

    print(json_data)

    end = default_timer()
    print("Time duration(in seconds):", end - start)

    return jsonify(json_data), 200

if __name__ == '__main__':
    #serve(app, host=cfg.host_num, port=cfg.port_num)
    app.run(host=cfg.host_num, port=cfg.port_num, debug=True)
