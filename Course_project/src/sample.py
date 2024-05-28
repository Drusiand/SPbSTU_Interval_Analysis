from copy import deepcopy

from matplotlib.patches import Rectangle

from interval import Interval
import matplotlib.pyplot as plt
import numpy as np

from src.multiinterval import MultiInterval

COLUMN_DELIMITER = ';'
DAT_COLUMN_DELIMITER = "\t"
DEFAULT_BLUE = '#1f77b4'


class Sample:

    @staticmethod
    def __read_file_column(file_path: str, column_num: int = 0, is_dat: bool = False) -> list[float]:
        raw_data = list()
        with open(file_path) as file:
            _ = file.readline()
            while True:
                line = file.readline()
                if not line:
                    break
                if is_dat:
                    raw_data.append(float(line.split(DAT_COLUMN_DELIMITER)[column_num].strip().replace(',', '.')))
                else:
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

    def __init__(self, data_path: str = None, col_num: int = 17):
        self.multimoda = MultiInterval()
        if data_path:
            self.wave_length = self.__read_file_column(data_path)
            self.data = self.__read_file_column(data_path, col_num)
        else:
            self.wave_length = list()
            self.data = list()

    def __len__(self):
        return len(self.data)

    def read_dat_file(self, path: str):
        self.wave_length = self.__read_file_column(path, 1, is_dat=True)
        self.data = self.__read_file_column(path, 2, is_dat=True)
        self.wave_length.sort()

    def extend(self, another: 'Sample'):
        self.data.extend(another.data)
        self.wave_length.extend(another.wave_length)

    def draw_sample_plot(self, title="", show=True):
        xs, ys = list(), list()
        for elem, value in zip(self.data, self.wave_length):
            xs.append(value)
            ys.append(elem)
        if len(self.multimoda) != 0:
            for moda in self.multimoda.intervals:
                plt.plot([moda.begin, moda.begin], [0, max(self.data)], "r--")
                plt.plot([moda.end, moda.end], [0, max(self.data)], "r--")

                plt.gca().add_patch(
                    Rectangle((moda.begin, 0), moda.width(), max(self.data), fill=True, color='r', alpha=0.1,
                              zorder=100))
        if show:
            plt.title(title)
            plt.plot(xs, ys)
            plt.xlabel("\u03BB (nm)")
            plt.ylabel("I (a.u.)")
            plt.show()

    def __widen_border(self):
        pass

    def find_moda(self, noise: float = 0, delta_step: int = 12, factor: float = 3, max_ints: float = float('inf')):
        tmp_self = deepcopy(self)
        moda = list()
        break_flag = False
        while True:
            step = 0
            max_moda = max(tmp_self.data)
            if max_moda == 0:
                break
            # cur_index = tmp_self.data.index(max_moda)
            cur_index = np.argmax(tmp_self.data)
            wide_moda = Interval(max_moda, max_moda)

            mean = np.mean(tmp_self.data)
            if mean * factor > max_moda:
                break

            while True:
                if cur_index - step < 0 or cur_index + step >= len(self):
                    break
                wide_moda.begin = self.data[cur_index - step]
                wide_moda.end = self.data[cur_index + step]
                for i in range(cur_index - step, cur_index + step + 1):
                    tmp_self.data[i] = 0

                if max_moda < max(wide_moda.begin, wide_moda.end) + noise:
                    if len(moda) == max_ints - 1:
                        break_flag = True
                    break

                max_moda = max(wide_moda.begin, wide_moda.end)
                step += delta_step

            moda.append(Interval(self.wave_length[self.data.index(wide_moda.begin)],
                                 self.wave_length[self.data.index(wide_moda.end)]))
            if break_flag:
                break

        self.multimoda = MultiInterval(moda)
        return moda

    def find_moda_interval(self) -> tuple[Interval, dict]:
        initial_interval = self.data[0]
        return_flag = True
        for elem in self.data:
            initial_interval = initial_interval.intersection(elem)
            if type(initial_interval) != Interval:
                return_flag = False
                break

        if return_flag:
            return initial_interval, {initial_interval: len(self)}

        y_list = list()
        for elem in self.data:
            y_list.append(elem.begin)
            y_list.append(elem.end)
        y_list.sort()

        z_list = list()
        i = 0
        while i < len(y_list):
            z_list.append(Interval(y_list[i], y_list[i + 1]))
            i += 2

        mu_dict = dict()
        for z in z_list:
            mu_dict[z] = 0
            for x in self.data:
                if x.includes(z):
                    mu_dict[z] += 1

        max_mu = max(mu_dict.values())
        mode_intervals = list()
        for key in mu_dict.keys():
            if mu_dict[key] == max_mu:
                mode_intervals.append(key)

        mode = mode_intervals[0]
        for interval in mode_intervals:
            mode = mode.union(interval)

        return mode, mu_dict
