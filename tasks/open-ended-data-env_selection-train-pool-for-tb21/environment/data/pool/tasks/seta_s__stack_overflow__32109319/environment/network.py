import numpy as np
from activations import relu, relu_derivative, leaky_relu, leaky_relu_derivative


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, activation="leaky_relu", learning_rate=0.1):
        self.learning_rate = learning_rate
        self.activation_name = activation

        if activation == "relu":
            self.activation = relu
            self.activation_derivative = relu_derivative
        elif activation == "leaky_relu":
            self.activation = leaky_relu
            self.activation_derivative = leaky_relu_derivative
        else:
            raise ValueError(f"Unknown activation: {activation}")

        self.weights_ih = np.random.randn(input_size, hidden_size) * 0.5
        self.bias_h = np.zeros((1, hidden_size))
        self.weights_ho = np.random.randn(hidden_size, output_size) * 0.5
        self.bias_o = np.zeros((1, output_size))

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))

    def sigmoid_derivative(self, x):
        s = self.sigmoid(x)
        return s * (1 - s)

    def forward(self, X):
        self.hidden_input = X.dot(self.weights_ih) + self.bias_h
        self.hidden_output = self.activation(self.hidden_input)
        self.output_input = self.hidden_output.dot(self.weights_ho) + self.bias_o
        self.output = self.sigmoid(self.output_input)
        return self.output

    def backward(self, X, y):
        m = X.shape[0]
        output_error = self.output - y
        delta_output = output_error * self.sigmoid_derivative(self.output_input)

        error_hidden = delta_output.dot(self.weights_ho)
        delta_hidden = error_hidden * self.activation_derivative(self.hidden_input)

        self.weights_ho -= self.learning_rate * self.hidden_output.T.dot(delta_output) / m
        self.bias_o -= self.learning_rate * np.sum(delta_output, axis=0, keepdims=True) / m
        self.weights_ih -= self.learning_rate * X.T.dot(delta_hidden) / m
        self.bias_h -= self.learning_rate * np.sum(delta_hidden, axis=0, keepdims=True) / m

    def compute_loss(self, y):
        eps = 1e-8
        return -np.mean(y * np.log(self.output + eps) + (1 - y) * np.log(1 - self.output + eps))
