import copy

from sample import Sample
from utils import jaccard_index, find_correction_factor, draw_r_jk_graph, draw_mode_frequency_plot


def main():
    sample_positive = Sample("../../data/+0_5V/+0_5V_4.txt", "../../data/ZeroLine/ZeroLine_4.txt", delta=1 / 2 ** 10)
    sample_negative = Sample("../../data/-0_5V/-0_5V_8.txt", "../../data/ZeroLine/ZeroLine_8.txt", delta=1 / 2 ** 10)

    sample_general = copy.deepcopy(sample_positive)
    sample_general.extend(sample_negative)

    sample_positive.draw_sample_plot()

    r, aux_data = find_correction_factor(sample_positive, sample_negative)
    draw_r_jk_graph(r, sample_positive, sample_negative)

    print("r =", r)
    sample_negative.apply_correction(r)

    sample_corrected = copy.deepcopy(sample_positive)
    sample_corrected.extend(sample_negative)

    sample_corrected.draw_sample_plot()

    mode, mode_freq_dict = sample_positive.find_mode()
    print(mode)
    if len(mode_freq_dict) > 1:
        draw_mode_frequency_plot(mode_freq_dict)
    else:
        print("sample is conjoint")


if __name__ == '__main__':
    main()
