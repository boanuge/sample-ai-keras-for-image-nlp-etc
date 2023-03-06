# -*- coding: utf-8 -*-
"""
Class definition of YOLO_v3 style detection model on image
"""

import colorsys
import os

import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.models import load_model
from keras.layers import Input
from PIL import Image, ImageFont, ImageDraw

from yolo3_model import yolo_eval, yolo_body, tiny_yolo_body
from yolo3_utils import letterbox_image
import yolo3_config as cfg
import os
#from keras.utils import multi_gpu_model

# Need to comment out for Yolo model training
from tensorflow.python.framework.ops import disable_eager_execution
disable_eager_execution()

yolo_model_global = None
boxes = None
scores = None
classes = None

class YOLO:
    config = cfg.YOLO_class_default()

    _defaults = {
        "model_path": config.model_path,
        "anchors_path": config.anchors_path, # 디폴트값 사용
        "classes_path": config.classes_path, # 디폴트값 사용
        "score" : config.score, # 디폴트값 사용
        "iou" : config.iou, # 디폴트값 사용
        "model_image_size" : config.model_image_size, # 디폴트값 사용
        "gpu_num" : config.gpu_num, # Only CPU # 디폴트값 사용
    }

    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults) # set up default values
        self.__dict__.update(kwargs) # and update with user overrides
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        
        # turn off tensorflow/core/grappler/optimizers/meta_optimizer.cc by tf.OptimizerOptions.L0
        #session_conf = tf.compat.v1.ConfigProto(
        #    graph_options=tf.compat.v1.GraphOptions(optimizer_options=tf.compat.v1.OptimizerOptions(
        #        opt_level=tf.compat.v1.OptimizerOptions.L0)))
        #self.sess = K.get_session(session_conf)
        self.sess = K.get_session()

        #self.yolo_model = self.load_model()
        self.K_learning_phase = K.learning_phase()
        self.boxes, self.scores, self.classes = self.generate()
        print("self.boxes, self.scores, self.classes:")
        print(self.boxes, self.scores, self.classes)

    def _get_class(self):
        classes_path = os.path.expanduser(self.classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def _get_anchors(self):
        anchors_path = os.path.expanduser(self.anchors_path)
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)

    '''
    def load_model(self):
        global yolo_model_global

        if yolo_model_global is None:
            model_path = os.path.expanduser(self.model_path)
            assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

            # Load model, or construct model and load weights.
            num_anchors = len(self.anchors)
            num_classes = len(self.class_names)
            is_tiny_version = num_anchors==6 # default setting
            try:
                yolo_model_global = load_model(model_path, compile=False)
            except:
                yolo_model_global = tiny_yolo_body(Input(shape=(None,None,3)), num_anchors//2, num_classes) \
                    if is_tiny_version else yolo_body(Input(shape=(None,None,3)), num_anchors//3, num_classes)
                yolo_model_global.load_weights(self.model_path) # make sure model, anchors and classes match
            else:
                assert yolo_model_global.layers[-1].output_shape[-1] == \
                    num_anchors/len(yolo_model_global.output) * (num_classes + 5), \
                    'Mismatch between model and given anchor and class sizes'

            print('{} : model, anchors, and classes loaded.'.format(model_path))
        else:
            print('{} : yolo_model has been already loaded.'.format(self.model_path))
        return yolo_model_global
    '''

    def generate(self):

        model_path = os.path.expanduser(self.model_path)
        assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

        # Load model, or construct model and load weights.
        num_anchors = len(self.anchors)
        num_classes = len(self.class_names)
        is_tiny_version = num_anchors==6 # default setting
        try:
            self.yolo_model = load_model(model_path, compile=False)
        except:
            self.yolo_model = tiny_yolo_body(Input(shape=(None,None,3)), num_anchors//2, num_classes) \
                if is_tiny_version else yolo_body(Input(shape=(None,None,3)), num_anchors//3, num_classes)
            self.yolo_model.load_weights(self.model_path) # make sure model, anchors and classes match
        else:
            assert self.yolo_model.layers[-1].output_shape[-1] == \
                num_anchors/len(self.yolo_model.output) * (num_classes + 5), \
                'Mismatch between model and given anchor and class sizes'

        print('{} model, anchors, and classes loaded.'.format(model_path))

        # Generate colors for drawing bounding boxes.
        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))
        np.random.seed(10101)  # Fixed seed for consistent colors across runs.
        np.random.shuffle(self.colors)  # Shuffle colors to decorrelate adjacent classes.
        np.random.seed(None)  # Reset seed to default.

        # Generate output tensor targets for filtered bounding boxes.
        self.input_image_shape = K.placeholder(shape=(2, ))
        '''
        if self.gpu_num>=2:
            self.yolo_model = multi_gpu_model(self.yolo_model, gpus=self.gpu_num)
        '''

        '''
        global boxes, scores, classes
        print("boxes, scores, classes:")
        print(boxes, scores, classes)

        if classes is None:
            boxes, scores, classes = yolo_eval(self.yolo_model.output, self.anchors,
                    len(self.class_names), self.input_image_shape,
                    score_threshold=self.score, iou_threshold=self.iou)
        '''

        boxes, scores, classes = yolo_eval(self.yolo_model.output, self.anchors,
                len(self.class_names), self.input_image_shape,
                score_threshold=self.score, iou_threshold=self.iou)

        return boxes, scores, classes

    def popup_image(self, image):

        if self.model_image_size != (None, None):
            assert self.model_image_size[0]%32 == 0, 'Multiples of 32 required'
            assert self.model_image_size[1]%32 == 0, 'Multiples of 32 required'
            boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))
        else:
            new_image_size = (image.width - (image.width % 32),
                              image.height - (image.height % 32))
            boxed_image = letterbox_image(image, new_image_size)

        image_data = np.array(boxed_image, dtype='float32')
        image_data /= 255.
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                self.K_learning_phase: 0
            })
        K.clear_session()
        print('Found {} boxes for {}'.format(len(out_boxes), image))

        font = ImageFont.truetype(font='font/FiraMono-Medium.otf',
                    size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
        thickness = (image.size[0] + image.size[1]) // 300

        for i, c in reversed(list(enumerate(out_classes))):
            predicted_class = self.class_names[c]
            box = out_boxes[i]
            score = out_scores[i]

            label = '{} {:.2f}'.format(predicted_class, score)
            draw = ImageDraw.Draw(image)
            label_size = draw.textsize(label, font)

            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
            print(label, (left, top), (right, bottom))

            if top - label_size[1] >= 0:
                text_origin = np.array([left, top - label_size[1]])
            else:
                text_origin = np.array([left, top + 1])

            # My kingdom for a good redistributable image drawing library.
            for i in range(thickness):
                draw.rectangle(
                    [left + i, top + i, right - i, bottom - i],
                    outline=self.colors[c])
            draw.rectangle(
                [tuple(text_origin), tuple(text_origin + label_size)],
                fill=self.colors[c])
            draw.text(text_origin, label, fill=(0, 0, 0), font=font)
            del draw

        return image

    def detect_image(self, image):

        if self.model_image_size != (None, None):
            assert self.model_image_size[0]%32 == 0, 'Multiples of 32 required'
            assert self.model_image_size[1]%32 == 0, 'Multiples of 32 required'
            boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))
        else:
            new_image_size = (image.width - (image.width % 32),
                              image.height - (image.height % 32))
            boxed_image = letterbox_image(image, new_image_size)

        image_data = np.array(boxed_image, dtype='float32')
        image_data /= 255.
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

        feed_data = {
            self.yolo_model.input: image_data,
            self.input_image_shape: [image.size[1], image.size[0]],
            self.K_learning_phase: 0
        }

        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes], feed_dict=feed_data)

        K.clear_session()
        print('Found {} boxes for {}'.format(len(out_boxes), image))

        '''
        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                K.learning_phase(): 0
            })
        '''

        print("out_boxes:", out_boxes)
        print("out_scores", out_scores)
        print("out_classes", out_classes)

        return out_scores

    def close_session(self):
        self.sess.close()