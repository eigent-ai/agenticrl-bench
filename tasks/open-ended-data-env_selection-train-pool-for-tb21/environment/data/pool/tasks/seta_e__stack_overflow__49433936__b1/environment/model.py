import tensorflow as tf


class MLP(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.fc1 = tf.keras.layers.Dense(300, activation='relu', name='fc1')
        self.fc2 = tf.keras.layers.Dense(100, activation='relu', name='fc2')
        self.output_layer = tf.keras.layers.Dense(10, name='output')

    def call(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        return self.output_layer(x)


class TinyRNN(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.rnn = tf.keras.layers.SimpleRNN(32, name='rnn')

    def call(self, x):
        return self.rnn(x)
