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

    # r_lower -= 2
    # r_upper += 2

    tmp_r = r_lower
    r_jk_dict = dict()

    # step = abs(r_upper - r_lower) / steps
    # r_jk_dict[str(r_lower)] = jaccard_index_corrected(sample_pos, sample_neg, r_lower)
    # r_jk_dict[str(r_upper)] = jaccard_index_corrected(sample_pos, sample_neg, r_upper)

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

    # while tmp_r <= r_upper:
    #     r_jk_dict[str(tmp_r)] = jaccard_index_corrected(sample_pos, sample_neg, tmp_r)
    #     tmp_r += step

    # max_jk = max(r_jk_dict.values())
    # for key in r_jk_dict.keys():
    #     if r_jk_dict[key] == max_jk:
    #         return float(key), r_jk_dict
    return tmp_r, r_jk_dict


# def draw_r_jk_graph(data: dict):
#     lists = [[float(key), value] for key, value in sorted(data.items(), key=lambda key: float(key[0]))]
#     x, y = zip(*lists)
#     plt.plot(x, y)
#     plt.show()


def draw_r_jk_graph(r: float, sample_pos: Sample, sample_neg: Sample, offset: float = 1):
    x = linspace(r - offset, r + offset, 101)
    y = list()
    for r_i in x:
        y.append(jaccard_index_corrected(sample_pos, sample_neg, r_i))
    plt.plot(x, y)
    plt.scatter(r, jaccard_index_corrected(sample_pos, sample_neg, r), c='red')
    plt.show()


def draw_mode_frequency_plot(data: dict):
    lists = [[key, value] for key, value in data.items()]
    x, y = list(), list()
    for elem in lists:
        x.append(elem[0].begin)
        x.append(elem[0].end)
        y.append(elem[1])
        y.append(elem[1])
    plt.plot(x, y)
    plt.show()
