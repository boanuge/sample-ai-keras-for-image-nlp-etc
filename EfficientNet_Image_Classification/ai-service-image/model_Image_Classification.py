from keras.models import load_model
import tensorflow as tf
import numpy as np

loaded_model = None

def create_model_instance(model_path):

    global loaded_model

    loaded_model = load_model(model_path)

    return

def get_class(image):

    global loaded_model

    new_size = (456, 456) # EfficientNetB5

    img_resized = image.resize(new_size)
    img_vectorized = (np.array(img_resized) / 255.0).astype('float32')
    img_vectorized = np.expand_dims(img_vectorized, axis=0)
    
    #img_resized = image.resize(new_size)
    #img_vectorized = tf.keras.preprocessing.image.img_to_array(img_resized)
    #img_vectorized = tf.keras.applications.efficientnet.preprocess_input(img_vectorized)
    #img_vectorized = np.expand_dims(img_vectorized, axis=0)
    
    predicted_result = loaded_model.predict(img_vectorized, verbose=0)

    return predicted_result
