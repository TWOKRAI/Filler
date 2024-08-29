import numpy as np

class Perceptron:
    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size
        self.weights = np.random.rand(input_size, output_size)
        self.bias = np.random.rand(output_size)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def predict(self, inputs):
        linear_output = np.dot(inputs, self.weights) + self.bias
        y_predicted = self.sigmoid(linear_output)
        return y_predicted

    def train(self, inputs, labels, epochs, learning_rate):
        for epoch in range(epochs):
            for i in range(len(inputs)):
                inputs_i = inputs[i]
                label_i = labels[i]

                # Forward pass
                linear_output = np.dot(inputs_i, self.weights) + self.bias
                y_predicted = self.sigmoid(linear_output)

                # Compute loss (mean squared error)
                loss = np.mean((y_predicted - label_i) ** 2)

                # Backward pass
                d_loss = 2 * (y_predicted - label_i) / len(y_predicted)
                d_y_predicted = self.sigmoid(linear_output) * (1 - self.sigmoid(linear_output))
                d_linear_output = d_loss * d_y_predicted

                # Update weights and bias
                self.weights -= learning_rate * np.dot(inputs_i.reshape(-1, 1), d_linear_output.reshape(1, -1))
                self.bias -= learning_rate * d_linear_output

            if epoch % 100 == 0:
                #print(f'Epoch {epoch}, Loss: {loss}')
                pass

# Пример использования
if __name__ == "__main__":
    # Создаем перцептрон с 8 входами и 10 выходами
    perceptron = Perceptron(input_size=8, output_size=10)

    # Пример входных данных (8 чисел от 0.0 до 1.0)
    inputs = np.array([
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
        [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
        # Добавьте больше данных для обучения
    ])

    # Пример меток (один из 10 выходных нейронов зажигается)
    labels = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        # Добавьте больше меток для обучения
    ])

    # Обучаем перцептрон
    perceptron.train(inputs, labels, epochs=1000, learning_rate=0.01)

    # Пример предсказания
    test_input = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.1])
    prediction = perceptron.predict(test_input)
    predicted_class = np.argmax(prediction) + 1  # +1, чтобы классы были от 1 до 10
    print("Prediction:", prediction)
    print("Predicted class:", predicted_class)
