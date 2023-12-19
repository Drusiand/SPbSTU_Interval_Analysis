STOP_POS_MARKER = "STOP Position"
SHIFT_DELIMITER = "="
COLUMN_DELIMITER = "    "

DEFAULT_BLUE = '#1f77b4'


class Interval:

    @staticmethod
    def __read_file(file_path: str, column_num: int) -> list[float]:
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

    @staticmethod
    def create_from_data(sample_path: str, zeros_path: str, column_num: int = 1) -> 'Interval':

        raw_data = Interval.__read_file(sample_path, column_num)
        zeros = Interval.__read_file(zeros_path, column_num)

        processed_data = list()
        for elem, zero in zip(raw_data, zeros):
            processed_data.append(elem - zero)

        return Interval(min(processed_data), max(processed_data))

    def __init__(self, begin: float, end: float):
        self.begin = begin
        self.end = end

    def __mul__(self, other):
        if type(other) == float or int:
            return Interval(min(self.begin * other, self.end * other),
                            max(self.begin * other, self.end * other))
        elif type(other) == Interval:
            return Interval(min(self.begin * other.begin,
                                self.begin * other.end,
                                self.end * other.begin,
                                self.end * other.end),
                            max(self.begin * other.begin,
                                self.begin * other.end,
                                self.end * other.begin,
                                self.end * other.end))

    def intersection(self, other: 'Interval') -> any:
        if self.end < other.begin or self.begin > other.end:
            return
        else:
            return Interval(max(self.begin, other.begin), min(self.end, other.end))

    def union(self, other: 'Interval') -> 'Interval':
        return Interval(min(self.begin, other.begin), max(self.end, other.end))

    def includes(self, other: 'Interval') -> bool:
        return self.begin <= other.begin and self.end >= other.end

    def mid(self) -> float:
        return (self.begin + self.end) / 2

    def rad(self) -> float:
        return abs((self.end - self.begin) / 2)

    def __str__(self):
        return "[" + str(self.begin) + ", " + str(self.end) + "]"
