from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import io
import os

from timeit import default_timer

loaded_model = None

def create_model_instance(model_path):
    print("create_model_instance()...")

    start = default_timer()

    global loaded_model

    loaded_model = load_model(model_path)

    end = default_timer()
    print("Time duration(in seconds):", end - start)
    return

def get_class(image):
    print("get_class()...")

    start = default_timer()

    new_size = (456, 456) # EfficientNetB5
    img_resized = image.resize(new_size)
    img_vectorized = tf.keras.preprocessing.image.img_to_array(img_resized)
    img_vectorized = tf.keras.applications.efficientnet.preprocess_input(img_vectorized)
    img_vectorized = np.expand_dims(img_vectorized, axis=0)

    predicted_result = loaded_model.predict(img_vectorized)

    '''
    # Create the image file
    temporary_image_file = "temporary_image_file.jpg"
    image.save(temporary_image_file, format='JPEG')
    img_resized = tf.keras.preprocessing.image.load_img(temporary_image_file, target_size=(456, 456)) # EfficientNetB5
    img_vectorized = tf.keras.preprocessing.image.img_to_array(img_resized)
    img_vectorized = tf.keras.applications.efficientnet.preprocess_input(img_vectorized)
    img_vectorized = np.expand_dims(img_vectorized, axis=0)
    predicted_result = loaded_model.predict(img_vectorized)
    # Delete the image file
    if os.path.exists(temporary_image_file):
        os.remove(temporary_image_file)
        print("File deleted successfully:", temporary_image_file)
    else:
        print("File not found:", temporary_image_file)
    '''

    end = default_timer()
    print("Time duration(in seconds):", end - start)
    return predicted_result
