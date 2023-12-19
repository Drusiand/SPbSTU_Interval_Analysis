class Interval:
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

    def __str__(self):
        return "[" + str(self.begin) + ", " + str(self.end) + "]"
