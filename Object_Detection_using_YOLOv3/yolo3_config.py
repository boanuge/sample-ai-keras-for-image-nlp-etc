import os

root_directory_windows = "C:\\AI\\ai-service" # os.getcwd() + "/"
root_directory_ubuntu = "/home/ai-service @ image"

model_path = "./output/"
yolo_image_path = "./images_test/"

# YOLO_v3
yolo_error_log_disable = True
yolo_future_error_log_disable = True

class YOLO_class_default:
    def __init__(self):
        self.model_path = 'output/yolo3_weights_trained_epoch_100.h5'
        self.anchors_path = 'yolo_anchors.txt'  # 디폴트값 사용
        self.classes_path = 'yolo_classes.txt'  # 디폴트값 사용
        self.score = 0.3  # 디폴트값 사용
        self.iou = 0.45  # 디폴트값 사용
        self.model_image_size = (416, 416)  # 디폴트값 사용
        self.gpu_num = 0,  # Only CPU # 디폴트값 사용
