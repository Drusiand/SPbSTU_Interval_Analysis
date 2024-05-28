import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

COLUMN_DELIMITER = ';'


class Plotter:

    @staticmethod
    def __prepare_data(file_path: str) -> tuple:
        x, y, z = list(), list(), list()
        with open(file_path) as file:
            x = file.readline()
            x = [int(i) for i in x.split(COLUMN_DELIMITER)]
            while True:
                line = file.readline()
                if not line:
                    break
                tokens = line.split(COLUMN_DELIMITER)
                y.append(float(tokens[0].replace(',', '.')))
                z.extend([float(i.replace(',', '.')) for i in tokens[1:]])
        return x, y, z

    def __init__(self, file_path: str):
        self.file_path = file_path

    def plot_3d(self):
        x, y, z = self.__prepare_data(self.file_path)

        x, y = np.meshgrid(x, y)
        z = np.array(z)
        z = z.reshape(x.shape)
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        surf = ax.plot_surface(y, x, z)
        ax.set_xlabel("Wavelength, nm")
        ax.set_ylabel("Moment of time," + "\u03bc" + " sec")
        ax.set_zlabel("Intensity, W/m^2")
        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.show()

    def plot_heatmap(self):
        x, y, z = self.__prepare_data(self.file_path)

        cols, rows = x, y

        x, y = np.meshgrid(x, y)
        z = np.array(z)
        z = z.reshape(x.shape)

        df = pd.DataFrame(z, index=rows, columns=cols)
        ax = sns.heatmap(df, cmap="crest")
        ax.set(xlabel='time (\u03BCs)', ylabel='\u03bb (nm)')

        # plt.plot([0, 16000], [465.8, 465.8])
        # plt.plot([0, 16000], [467.5, 467.5])

        # ax.axhline(y=465.8, linewidth=2, color="w")

        plt.show()

    def plot_multimodas(self, multimodas):
        # colors = ["red", 'green', 'blue']
        for i, multimoda in enumerate(multimodas):
            plt.plot([i, i], [200, 1100], lw=1, c="lightgray")
            for interval in multimoda:
                xs, ys = [], []
                xs.append(i)
                xs.append(i)
                ys.append(interval.begin)
                ys.append(interval.end)
                # color = colors[i % 3]
                color = "blue"
                plt.plot(xs, ys, lw=2, c=color)
        plt.xlabel("time (ms)")
        plt.ylabel('\u03bb (nm)')
        plt.show()
