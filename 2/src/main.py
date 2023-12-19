from interval import Interval
from sample import Sample
from utils import UtilHelper


def main():
    values = [-0.5, -0.25, 0.25, 0.5]
    strings = ['-0_5V', '-0_25V', '+0_25V', '+0_5V']
    number = 4

    sample = Sample(values)
    for string in strings:
        sample.append(Interval.create_from_data("../../data/" + string + "/" + string + "_" + str(number) + ".txt",
                                                "../../data/ZeroLine/ZeroLine_" + str(number) + ".txt"))

    for interval in sample.data:
        print(interval)

    sample.draw_sample_plot()
    coeffs = UtilHelper.calculate_regression(sample)
    UtilHelper.plot_regression(coeffs, sample)
    inform_set = UtilHelper.build_inform_set(sample, coeffs, plot=True)
    UtilHelper.plot_corridor(sample, inform_set)


if __name__ == '__main__':
    main()
