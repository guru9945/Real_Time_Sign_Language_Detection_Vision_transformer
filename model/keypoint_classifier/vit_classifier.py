#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Vision Transformer (ViT) based Hand Gesture Classifier
Replaces the simple MLP with a Vision Transformer architecture
for sign language detection using pose estimation.
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


class ViTClassifier(object):
    """
    Vision Transformer Classifier for Hand Gesture Recognition
    
    Converts 21 hand keypoints into a 2D grid representation
    and applies Transformer attention for classification.
    """
    
    def __init__(
        self,
        model_path='model/keypoint_classifier/keypoint_classifier_vit.h5',
        num_threads=1,
        image_size=7,  # 7x7 grid representing 21 keypoints (3 channels: x, y, z)
        num_classes=5,
        embed_dim=64,
        num_heads=4,
        mlp_hidden=128,
    ):
        self.image_size = image_size
        self.num_classes = num_classes
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.mlp_hidden = mlp_hidden
        self.model_path = model_path
        self.tflite_path = model_path.replace('.h5', '.tflite')
        
        if os.path.exists(self.tflite_path):
            self.interpreter = tf.lite.Interpreter(model_path=self.tflite_path,
                                                   num_threads=num_threads)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            self.use_tflite = True
        elif os.path.exists(self.model_path):
            self.model = keras.models.load_model(self.model_path)
            self.use_tflite = False
        else:
            raise FileNotFoundError(
                f"No trained ViT model found. Expected '{self.tflite_path}' or '{self.model_path}'"
            )
    
    def _build_vit_model(self):
        """
        Build Vision Transformer model for hand gesture classification.
        
        Architecture:
        - Input: 7x7x3 (21 keypoints × 3 coordinates x,y,z reshaped)
        - Patch embedding
        - Transformer encoder layers
        - Classification head
        """
        inputs = layers.Input(shape=(self.image_size, self.image_size, 3))

        # Patch Embedding: Flatten the 2D grid into a sequence of tokens
        x = layers.Conv2D(self.embed_dim, kernel_size=1, strides=1, padding='valid')(inputs)
        x = layers.Reshape((self.image_size * self.image_size, self.embed_dim))(x)
        x = layers.LayerNormalization(epsilon=1e-6)(x)

        # Transformer Encoder Blocks
        for _ in range(2):  # 2 transformer layers
            attn_output = layers.MultiHeadAttention(
                num_heads=self.num_heads,
                key_dim=self.embed_dim // self.num_heads
            )(x, x)
            x = x + attn_output
            x = layers.LayerNormalization(epsilon=1e-6)(x)

            mlp = layers.Dense(self.mlp_hidden, activation='relu')(x)
            mlp = layers.Dense(self.embed_dim)(mlp)
            x = x + mlp
            x = layers.LayerNormalization(epsilon=1e-6)(x)

        # Pool sequence tokens for classification
        x = layers.GlobalAveragePooling1D()(x)
        outputs = layers.Dense(self.mlp_hidden // 2, activation='relu')(x)
        outputs = layers.Dropout(0.3)(outputs)
        outputs = layers.Dense(self.num_classes, activation='softmax')(outputs)

        model = keras.Model(inputs=inputs, outputs=outputs)
        return model
    
    def preprocess_keypoints(self, landmark_list):
        """
        Convert 21 hand keypoints to 2D grid representation.
        
        Args:
            landmark_list: List of 21 keypoints with x,y coordinates
                          Can be: list of [x,y] pairs (21 items), 
                                 flattened [x,y,z...] (42 or 63 values), or
                                 ndarray with shape (21, 2) or (21, 3)
        
        Returns:
            Preprocessed array suitable for ViT input (7, 7, 3)
        """
        # Handle different input formats
        arr = np.array(landmark_list)
        
        if arr.ndim == 1:
            # Flat array: 42 values [x,y,x,y,...] or 63 values [x,y,z,...]
            if len(arr) == 42:
                keypoints = arr.reshape(21, 2)
                z_coords = np.zeros((21, 1))
                keypoints = np.hstack([keypoints, z_coords])
            elif len(arr) == 63:
                keypoints = arr.reshape(21, 3)
            else:
                raise ValueError(f"Expected 21 keypoints (42 or 63 values), got {len(arr)}")
        elif arr.ndim == 2:
            # 2D array: (21, 2) or (21, 3)
            if arr.shape[0] == 21 and arr.shape[1] == 2:
                z_coords = np.zeros((21, 1))
                keypoints = np.hstack([arr, z_coords])
            elif arr.shape[0] == 21 and arr.shape[1] == 3:
                keypoints = arr
            else:
                raise ValueError(f"Expected shape (21, 2) or (21, 3), got {arr.shape}")
        else:
            raise ValueError(f"Expected 1D or 2D array, got {arr.ndim}D")
        
        # Normalize keypoints like the MLP classifier (relative to wrist + global normalization)
        # Convert to relative coordinates
        keypoints_relative = keypoints - keypoints[0]  # Center around wrist
        
        # Flatten and normalize by max absolute value (same as MLP preprocessing)
        flattened = keypoints_relative[:, :2].flatten()  # Only x,y coordinates
        max_value = np.max(np.abs(flattened))
        if max_value > 0:
            flattened_normalized = flattened / max_value
        else:
            flattened_normalized = flattened
        
        # Reshape back to (21, 2) for grid mapping
        keypoints_normalized = flattened_normalized.reshape(21, 2)
        
        # Add z coordinate (0)
        z_coords = np.zeros((21, 1))
        keypoints_normalized = np.hstack([keypoints_normalized, z_coords])
        
        # Reshape to 7x7 grid (21 keypoints → 7×7 with padding)
        # Map: 21 keypoints to 7x7 grid, remaining slots filled with zeros
        grid = np.zeros((7, 7, 3))
        
        # Map keypoints to grid positions (hand topology aware)
        keypoint_positions = [
            (0, 0), (0, 3), (0, 6),  # Wrist, middle, pinky base
            (1, 1), (1, 3), (1, 5),  # Thumb, middle, pinky
            (2, 1), (2, 3), (2, 5),  # Index, middle, pinky PIP
            (3, 1), (3, 3), (3, 5),  # Index, middle, pinky DIP
            (4, 0), (4, 2), (4, 4), (4, 6),  # Fingertips row 1
            (5, 0), (5, 2), (5, 4), (5, 6),  # Fingertips row 2
            (6, 1), (6, 3), (6, 5),  # Extra points
        ]
        
        for i, pos in enumerate(keypoint_positions[:len(keypoints_normalized)]):
            grid[pos[0], pos[1]] = keypoints_normalized[i]
        
        return grid
    
    def __call__(self, landmark_list):
        """Predict gesture class from hand keypoints."""
        if self.use_tflite:
            # Use TFLite interpreter
            input_details_tensor_index = self.input_details[0]['index']
            preprocessed = self.preprocess_keypoints(landmark_list)
            self.interpreter.set_tensor(
                input_details_tensor_index,
                np.array([preprocessed], dtype=np.float32))
            self.interpreter.invoke()
            
            output_details_tensor_index = self.output_details[0]['index']
            result = self.interpreter.get_tensor(output_details_tensor_index)
            return np.argmax(np.squeeze(result))
        else:
            # Use Keras model
            preprocessed = self.preprocess_keypoints(landmark_list)
            preprocessed = np.expand_dims(preprocessed, axis=0)
            result = self.model.predict(preprocessed, verbose=0)
            return np.argmax(np.squeeze(result))
    
    def summary(self):
        """Print model architecture."""
        if not self.use_tflite:
            return self.model.summary()
        return "TFLite model loaded - use model.summary() before conversion"


class TemporalViTClassifier(ViTClassifier):
    """
    Extended ViT classifier with temporal sequence modeling.
    Uses Transformer encoder to model hand movement over time.
    """
    
    def __init__(
        self,
        model_path='model/keypoint_classifier/keypoint_classifier_temporal_vit.h5',
        num_threads=1,
        sequence_length=16,
        num_classes=5,
    ):
        self.sequence_length = sequence_length
        self.keypoint_history = []
        self.num_classes = num_classes
        self.model_path = model_path
        self.tflite_path = model_path.replace('.h5', '.tflite')
        try:
            if os.path.exists(self.tflite_path):
                self.interpreter = tf.lite.Interpreter(model_path=self.tflite_path,
                                                       num_threads=num_threads)
                self.interpreter.allocate_tensors()
                self.input_details = self.interpreter.get_input_details()
                self.output_details = self.interpreter.get_output_details()
                self.use_tflite = True
            elif os.path.exists(self.model_path):
                self.model = keras.models.load_model(self.model_path)
                self.use_tflite = False
            else:
                raise FileNotFoundError(
                    f"No trained Temporal ViT model found. Expected '{self.tflite_path}' or '{self.model_path}'"
                )
        except Exception as e:
            raise RuntimeError(
                f"Failed to load Temporal ViT model: {e}"
            )
        
    def _build_temporal_model(self):
        """
        Build Temporal Vision Transformer for sequence modeling.
        Captures hand movement patterns over time.
        """
        # Input: Sequence of keypoint grids
        inputs = layers.Input(shape=(self.sequence_length, 7, 7, 3))
        
        # Temporal encoding via Transformer
        x = layers.TimeDistributed(layers.Conv2D(32, 3, activation='relu'))(inputs)
        x = layers.TimeDistributed(layers.GlobalAveragePooling2D())(x)
        
        # Transformer for temporal modeling
        x = layers.Reshape((self.sequence_length, -1))(x)
        
        # Self-attention across time
        attn = layers.MultiHeadAttention(num_heads=4, key_dim=32)(x, x)
        x = x + attn
        x = layers.LayerNormalization(epsilon=1e-6)(x)
        
        # Feed forward
        ff = layers.Dense(64, activation='relu')(x)
        ff = layers.Dense(x.shape[-1])(ff)
        x = x + ff
        x = layers.LayerNormalization(epsilon=1e-6)(x)
        
        # Global pooling and classification
        x = layers.GlobalAveragePooling1D()(x)
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        return keras.Model(inputs=inputs, outputs=outputs)
    
    def add_to_history(self, landmark_list):
        """Add keypoints to temporal history."""
        grid = self.preprocess_keypoints(landmark_list)
        self.keypoint_history.append(grid)
        
        if len(self.keypoint_history) > self.sequence_length:
            self.keypoint_history.pop(0)
    
    def __call__(self, landmark_list):
        """Predict with temporal context."""
        self.add_to_history(landmark_list)
        
        if len(self.keypoint_history) < self.sequence_length:
            return None  # Not enough history
        
        sequence = np.array(self.keypoint_history)
        sequence = np.expand_dims(sequence, axis=0)
        
        result = self.model.predict(sequence, verbose=0)
        return np.argmax(np.squeeze(result))