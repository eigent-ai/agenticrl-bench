"""model_def.py -- CNN model definition for MNIST-like classification using Keras."""
import tensorflow as tf
from tensorflow import keras
from keras import layers


def build_simple_cnn(num_classes=5):
    """A small CNN for 1-channel 28x28 image classification.

    Args:
        num_classes: Number of output classes.

    Returns:
        A compiled Keras Sequential model.
    """
    model = keras.Sequential([
        layers.Input(shape=(28, 28, 1)),
        layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes),
    ])
    return model
