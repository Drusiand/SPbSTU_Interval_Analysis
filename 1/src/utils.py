import copy
import matplotlib.pyplot as plt

from sample import Sample
from numpy import linspace


def jaccard_index(sample: Sample) -> float:
    try:
        index = (sample.upper_min - sample.lower_max) / (sample.upper_max - sample.lower_min)
    except ZeroDivisionError:
        return float('inf')
    return index


def jaccard_index_corrected(sample_pos, sample_neg, r) -> float:
    tmp_sample = copy.deepcopy(sample_pos)
    tmp_neg = copy.deepcopy(sample_neg)
    tmp_neg.apply_correction(r)
    tmp_sample.extend(tmp_neg)
    return jaccard_index(tmp_sample)


def find_correction_factor(sample_pos: Sample, sample_neg: Sample, steps=100) -> tuple[float, dict]:
    sample = copy.deepcopy(sample_pos)
    sample.extend(sample_neg)

    r_lower = min(sample.lower_max / sample.upper_min, sample.lower_min / sample.upper_max)
    r_upper = max(sample.lower_max / sample.upper_min, sample.lower_min / sample.upper_max)

    tmp_r = r_lower
    r_jk_dict = dict()

    eps = 1e-5
    l_border = r_lower
    r_border = r_upper
    prev = float('inf')
    while abs(prev - tmp_r) > 1e-20:
        prev = tmp_r
        tmp_r = (l_border + r_border) / 2
        if jaccard_index_corrected(sample_pos, sample_neg, tmp_r - eps) < \
                jaccard_index_corrected(sample_pos, sample_neg, tmp_r + eps):
            l_border = tmp_r
        else:
            r_border = tmp_r
        r_jk_dict[str(tmp_r)] = jaccard_index_corrected(sample_pos, sample_neg, tmp_r)

    return tmp_r, r_jk_dict


def draw_r_jk_graph(r: float, sample_pos: Sample, sample_neg: Sample, offset: float = 1):
    plt.title("JK(R_opt) plot")
    x = linspace(r - offset, r + offset, 101)
    y = list()
    plt.scatter(r, jaccard_index_corrected(sample_pos, sample_neg, r), c='red')
    for r_i in x:
        y.append(jaccard_index_corrected(sample_pos, sample_neg, r_i))
    plt.plot(x, y)
    plt.legend(("R_opt", "R_i"))
    plt.show()


def draw_mode_frequency_plot(data: dict, title: str):
    plt.title(title)
    lists = [[key, value] for key, value in data.items()]
    x, y = list(), list()
    for elem in lists:
        x.append(elem[0].begin)
        x.append(elem[0].end)
        y.append(elem[1])
        y.append(elem[1])
    plt.plot(x, y)
    plt.show()
