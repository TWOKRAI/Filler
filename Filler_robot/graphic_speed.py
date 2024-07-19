import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, data, distance):
        self.data = data
        self.distance = distance


    def plot(self):
        x = range(self.distance) 
        plt.plot(x, self.data[:self.distance]) 
        plt.xlabel('Distance')
        plt.ylabel('Data')
        plt.title('Plot of Data vs Distance')
        plt.show()