import copy

from sample import Sample
from utils import jaccard_index, find_correction_factor, draw_r_jk_graph, draw_mode_frequency_plot


def main():
    sample_positive = Sample("../../data/+0_5V/+0_5V_4.txt", "../../data/ZeroLine/ZeroLine_4.txt", delta=1 / 2 ** 14)
    sample_negative = Sample("../../data/-0_5V/-0_5V_8.txt", "../../data/ZeroLine/ZeroLine_8.txt", delta=1 / 2 ** 14)

    sample_general = copy.deepcopy(sample_positive)
    sample_general.extend(sample_negative)

    sample_positive.draw_sample_plot("{X_positive} interval sample elements")
    sample_positive.draw_zeros_hist("{X_positive} interval sample deltas")
    mode_positive, mode_freq_dict_positive = sample_positive.find_mode()
    print(mode_positive)
    if len(mode_freq_dict_positive) > 1:
        draw_mode_frequency_plot(mode_freq_dict_positive, "{X_positive} moda frequency plot")
    else:
        print("sample is conjoint")

    sample_negative.draw_sample_plot("{X_negative} interval sample elements")
    sample_negative.draw_zeros_hist("{X_negative} interval sample deltas")
    mode_negative, mode_freq_dict_negative = sample_negative.find_mode()
    print(mode_negative)
    if len(mode_freq_dict_negative) > 1:
        draw_mode_frequency_plot(mode_freq_dict_negative, "{X_negative} moda frequency plot")
    else:
        print("sample is conjoint")

    r, aux_data = find_correction_factor(sample_positive, sample_negative)
    draw_r_jk_graph(r, sample_positive, sample_negative)

    print("r =", r)
    print("JK =", aux_data[str(r)])

    sample_negative.apply_correction(r)

    sample_corrected = copy.deepcopy(sample_positive)
    sample_corrected.extend(sample_negative)
    sample_corrected.draw_sample_plot("{X_positive U R_opt * X_negative} interval sample elements")
    mode_corrected, mode_freq_dict_corrected = sample_corrected.find_mode()
    print(mode_corrected)
    if len(mode_freq_dict_corrected) > 1:
        draw_mode_frequency_plot(mode_freq_dict_corrected, "{X_positive U R_opt * X_negative} moda frequency plot")
    else:
        print("sample is conjoint")


if __name__ == '__main__':
    main()
