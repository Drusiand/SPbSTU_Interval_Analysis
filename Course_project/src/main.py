from sample import Sample
from src.multiinterval import MultiInterval
import matplotlib.pyplot as plt
import pandas as pd
from utils import UtilHelper
from src.plotter import Plotter


def test_course():
    sample_1 = Sample("../data/41000.txt", col_num=4)
    sample_1.find_moda()
    # sample_1.draw_sample_plot()
    print(sample_1.multimoda)

    sample_2 = Sample("../data/41000.txt", col_num=35)
    sample_2.find_moda()
    # sample_2.draw_sample_plot()
    print(sample_2.multimoda)

    sample_3 = Sample("../data/41000.txt", col_num=36)
    sample_3.find_moda()
    sample_2.draw_sample_plot()
    print(sample_3.multimoda)

    sample_1_multimoda = sample_1.multimoda
    sample_2_multimoda = sample_2.multimoda

    # sample_1.multimoda = sample_2_multimoda
    # sample_1.draw_sample_plot()
    #
    # sample_2.multimoda = sample_1_multimoda
    # sample_2.draw_sample_plot()
    #
    # sample_1.multimoda = MultiInterval.intersection(sample_1_multimoda, sample_2_multimoda)
    # sample_2.multimoda = MultiInterval.intersection(sample_1_multimoda, sample_2_multimoda)
    # sample_1.draw_sample_plot()
    # sample_2.draw_sample_plot()

    sample_1.multimoda = MultiInterval.union_1(sample_1_multimoda, sample_2_multimoda)
    sample_2.multimoda = MultiInterval.union_1(sample_1_multimoda, sample_2_multimoda)
    sample_1.draw_sample_plot()
    sample_2.draw_sample_plot()


def main():
    # sample = Sample("../data/41000.txt", col_num=4)
    sample = Sample()
    sample.read_dat_file("../data/РУС-2_1.DAT")
    sample_moda = sample.find_moda(delta_step=3, max_ints=10)
    sample.draw_sample_plot()

    for interval in sample_moda:
        print(interval)

    # global_multimoda_1 = sample.multimoda
    # global_multimoda_2 = sample.multimoda

    # plotter = Plotter("../data/41000.csv")
    # plotter.plot_heatmap()
    #
    # mms = []
    #
    # for i in range(4, 157):  # [4-157]
    #     if i == 68:
    #         pass
    #     print(f"Processing column {i}/156")
    #     sample_tmp = Sample("../data/41000.txt", col_num=i)
    #     sample_tmp.find_moda()
    #
    #     # global_multimoda_1 = MultiInterval.union_1(global_multimoda_1, sample_tmp.multimoda)
    #     print(sample_tmp.multimoda)
    #     mms.append(sample_tmp.multimoda)
    #
    # # sample.multimoda = global_multimoda_1
    # # sample.draw_sample_plot()
    # #
    # # sample.multimoda = global_multimoda_2
    # # sample.draw_sample_plot()
    #
    # plotter.plot_multimodas(mms)
    #
    # # sample_interval = Sample()
    # # for i, mm in enumerate(mms):
    # #     for interval in mm:
    # #         sample_interval.data.append(interval)
    # #         sample_interval.wave_length.append(i)


if __name__ == '__main__':
    main()
    # test_course()
