#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    # Fallback to tensorflow if tflite_runtime is not available
    import tensorflow as tf
    class Interpreter:
        def __init__(self, model_path, num_threads=1):
            self._interpreter = tf.lite.Interpreter(model_path=model_path, num_threads=num_threads)
        def allocate_tensors(self):
            return self._interpreter.allocate_tensors()
        def get_input_details(self):
            return self._interpreter.get_input_details()
        def get_output_details(self):
            return self._interpreter.get_output_details()
        def set_tensor(self, index, data):
            return self._interpreter.set_tensor(index, data)
        def invoke(self):
            return self._interpreter.invoke()
        def get_tensor(self, index):
            return self._interpreter.get_tensor(index)


class KeyPointClassifier(object):
    def __init__(
        self,
        model_path='model/keypoint_classifier/keypoint_classifier.tflite',
        num_threads=1,
    ):
        self.interpreter = Interpreter(model_path=model_path,
                                       num_threads=num_threads)

        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def __call__(
        self,
        landmark_list,
    ):
        input_details_tensor_index = self.input_details[0]['index']
        self.interpreter.set_tensor(
            input_details_tensor_index,
            np.array([landmark_list], dtype=np.float32))
        self.interpreter.invoke()

        output_details_tensor_index = self.output_details[0]['index']

        result = self.interpreter.get_tensor(output_details_tensor_index)

        result_index = np.argmax(np.squeeze(result))

        return result_index
