import math

import matplotlib.pyplot as plt
from interval import Interval

STOP_POS_MARKER = "STOP Position"
SHIFT_DELIMITER = "="
COLUMN_DELIMITER = "    "

DEFAULT_BLUE = '#1f77b4'


class Sample:

    @staticmethod
    def __read_file(file_path: str, column_num: int = 1) -> list[float]:
        raw_data = list()
        with open(file_path) as file:
            line = file.readline()
            shift_size = int(line.split(SHIFT_DELIMITER)[-1].strip())
            while True:
                line = file.readline()
                if not line:
                    break
                raw_data.append(float(line.split(COLUMN_DELIMITER)[column_num].strip()))

        tmp_data = raw_data[:len(raw_data) - shift_size]
        result_data = raw_data[len(raw_data) - shift_size:]

        result_data.extend(tmp_data)
        return result_data

    def __init__(self, sample_path: str, zeros_path: str, column_num: int = 1, delta: float = 0.005):
        raw_data = self.__read_file(sample_path, column_num)
        zeros = self.__read_file(zeros_path, column_num)

        processed_data = list()
        self.__zeros = list()
        for elem, zero in zip(raw_data, zeros):
            processed_data.append(elem - zero)
            self.__zeros.append(zero)

        self.data = list()
        for elem in processed_data:
            self.data.append(Interval(elem - delta, elem + delta))
            self.data.append(Interval(elem, elem))
        self.__update_borders()

    def __len__(self):
        return len(self.data)

    def draw_sample_plot(self, title: str):
        plt.title(title)
        for i, elem in enumerate(self.data):
            plt.plot([i, i], [elem.begin, elem.end], c=DEFAULT_BLUE)
        plt.show()

    def draw_zeros_hist(self, title: str):
        plt.title(title)
        plt.hist(self.__zeros)
        plt.show()

    def extend(self, another: 'Sample'):
        self.data.extend(another.data)
        self.__update_borders()

    def __mul_by_number(self, number: float):
        for i in range(len(self.data)):
            self.data[i] *= number

    def apply_correction(self, correction_factor: float):
        self.__mul_by_number(correction_factor)
        self.__update_borders()

    def __update_borders(self):
        self.lower_min = min(self.data, key=lambda x: x.begin).begin
        self.upper_min = min(self.data, key=lambda x: x.end).end

        self.lower_max = max(self.data, key=lambda x: x.begin).begin
        self.upper_max = max(self.data, key=lambda x: x.end).end

    def find_mode(self) -> tuple[Interval, dict]:
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
