from sample import Sample
from src.multiinterval import MultiInterval


def main():
    sample_1 = Sample("../data/41000.txt", col_num=17)
    sample_1.find_moda()
    # sample_1.draw_sample_plot()
    print(sample_1.multimoda)

    sample_2 = Sample("../data/41000.txt", col_num=59)
    sample_2.find_moda()
    # sample_2.draw_sample_plot()
    print(sample_2.multimoda)

    sample_3 = Sample("../data/41000.txt", col_num=102)
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

    sample_1.multimoda = MultiInterval.union(sample_1_multimoda, sample_2_multimoda)
    sample_2.multimoda = MultiInterval.union(sample_1_multimoda, sample_2_multimoda)
    sample_1.draw_sample_plot()
    sample_2.draw_sample_plot()


if __name__ == '__main__':
    main()
