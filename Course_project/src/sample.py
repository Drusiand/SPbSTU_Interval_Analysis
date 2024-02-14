from copy import deepcopy
from math import sin, pi

from matplotlib.patches import Rectangle

from interval import Interval
import matplotlib.pyplot as plt
import numpy as np

from src.multiinterval import MultiInterval

COLUMN_DELIMITER = ';'
DEFAULT_BLUE = '#1f77b4'


class Sample:

    @staticmethod
    def __read_file_column(file_path: str, column_num: int = 0) -> list[float]:
        raw_data = list()
        with open(file_path) as file:
            _ = file.readline()
            while True:
                line = file.readline()
                if not line:
                    break

                raw_data.append(float(line.split(COLUMN_DELIMITER)[column_num].strip().replace(',', '.')))
        return raw_data

    @staticmethod
    def __read_file_line(file_path: str, line_num: int = 0) -> list[Interval]:
        DELTA = 10
        raw_data = list()
        with open(file_path) as file:
            i = 0
            while i < line_num:
                _ = file.readline()
                i += 1
            line = file.readline()
            for elem in line.split(COLUMN_DELIMITER)[1:]:
                raw_data.append(Interval(float(elem.strip().replace(',', '.')) - DELTA,
                                         float(elem.strip().replace(',', '.')) + DELTA))
        return raw_data

    def __init__(self, data_path: str, col_num: int = 17):
        self.multimoda = MultiInterval()
        if data_path:
            self.values = self.__read_file_column(data_path)
            self.data = self.__read_file_column(data_path, col_num)
        else:
            self.values = list()
            self.data = list()

    def __len__(self):
        return len(self.data)

    def extend(self, another: 'Sample'):
        self.data.extend(another.data)
        self.values.extend(another.values)

    def draw_sample_plot(self, title="", show=True):
        xs, ys = list(), list()
        for elem, value in zip(self.data, self.values):
            xs.append(value)
            ys.append(elem)
        # if len(self.multimoda) != 0:
        #     for moda in self.multimoda.intervals:
        #         plt.plot([moda.begin, moda.begin], [0, max(self.data)], "r--")
        #         plt.plot([moda.end, moda.end], [0, max(self.data)], "r--")
        #
        #         plt.gca().add_patch(
        #             Rectangle((moda.begin, 0), moda.width(), max(self.data), fill=True, color='r', alpha=0.1,
        #                       zorder=100))
        if show:
            plt.title(title)
            plt.plot(xs, ys)
            plt.xlabel("time")
            plt.ylabel("value")
            plt.show()

    # def __find_single_moda(self):
    # max_elem_index = self.data.index(max_elem)
    # if max_elem_index == 0:
    #     return Interval(max_elem, self.data[max_elem_index + 1]), (max_elem_index, max_elem_index + 1)
    # elif max_elem_index == len(self) - 1:
    #     return Interval(self.data[max_elem_index - 1], max_elem), (max_elem_index - 1, max_elem_index)
    # else:
    #     if self.data[max_elem_index - 1] > self.data[max_elem_index + 1]:
    #         return Interval(self.data[max_elem_index - 1], max_elem), (max_elem_index - 1, max_elem_index)
    #     else:
    #         return Interval(max_elem, self.data[max_elem_index + 1]), (max_elem_index, max_elem_index + 1)

    def __widen_border(self):
        pass

    def find_moda(self, noise: float = 0, delta_step: int = 12):
        tmp_self = deepcopy(self)
        moda = list()
        # for _ in range(3):
        while True:

            step = 0
            max_moda = max(tmp_self.data)
            cur_index = self.data.index(max_moda)
            wide_moda = Interval(max_moda, max_moda)

            mean = np.mean(tmp_self.data)
            if np.mean(tmp_self.data) * 2 > max_moda:
                break

            while True:
                wide_moda.begin = self.data[cur_index - step]
                wide_moda.end = self.data[cur_index + step]
                for i in range(cur_index - step, cur_index + step + 1):
                    tmp_self.data[i] = 0

                if max_moda < max(wide_moda.begin, wide_moda.end) + noise:
                    break

                max_moda = max(wide_moda.begin, wide_moda.end)
                step += delta_step

            moda.append(Interval(self.values[self.data.index(wide_moda.begin)],
                                 self.values[self.data.index(wide_moda.end)]))

        self.multimoda = MultiInterval(moda)
        return moda
    # def __update_borders(self):
    #     self.lower_min = min(self.data, key=lambda x: x.begin).begin
    #     self.upper_min = min(self.data, key=lambda x: x.end).end
    #
    #     self.lower_max = max(self.data, key=lambda x: x.begin).begin
    #     self.upper_max = max(self.data, key=lambda x: x.end).end

    # def append(self, interval: Interval):
    #     self.data.append(interval)
    #     self.__update_borders()

    # def find_moda(self) -> tuple[Interval, dict]:
    #     initial_interval = self.data[0]
    #     return_flag = True
    #     for elem in self.data:
    #         initial_interval = initial_interval.intersection(elem)
    #         if type(initial_interval) != Interval:
    #             return_flag = False
    #             break
    #
    #     if return_flag:
    #         return initial_interval, {initial_interval: len(self)}
    #
    #     y_list = list()
    #     for elem in self.data:
    #         y_list.append(elem.begin)
    #         y_list.append(elem.end)
    #     y_list.sort()
    #
    #     z_list = list()
    #     i = 0
    #     while i < len(y_list):
    #         z_list.append(Interval(y_list[i], y_list[i + 1]))
    #         i += 2
    #
    #     mu_dict = dict()
    #     for z in z_list:
    #         mu_dict[z] = 0
    #         for x in self.data:
    #             if x.includes(z):
    #                 mu_dict[z] += 1
    #
    #     max_mu = max(mu_dict.values())
    #     mode_intervals = list()
    #     for key in mu_dict.keys():
    #         if mu_dict[key] == max_mu:
    #             mode_intervals.append(key)
    #
    #     mode = mode_intervals[0]
    #     for interval in mode_intervals:
    #         mode = mode.union(interval)
    #
    #     return mode, mu_dict
    #
    # @staticmethod
    # def generate_synthetic(delta: float = 0.1, step: float = 0.1):
    #     values, data = list(), list()
    #     for i in np.arange(-4, 0, step):
    #         values.append(i)
    #         data.append(Interval(i - delta, i + delta))
    #
    #     for i in np.arange(0, 5, step):
    #         values.append(i)
    #         data.append(Interval(sin(i) - delta, sin(i) + delta))
    #
    #     for i in np.arange(5, 9, step):
    #         values.append(i)
    #         data.append(Interval(i - (2 * pi) - delta, i - (2 * pi) + delta))
    #     sample = Sample("")
    #
    #     sample.values = values
    #     sample.data = data
    #     sample.__update_borders()
    #     return sample
