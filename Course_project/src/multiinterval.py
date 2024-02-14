from typing import Iterable

from interval import Interval


class MultiInterval:
    def __init__(self, data: Iterable[Interval] | None = None):
        if data is None:
            self.intervals = list()
        else:
            self.intervals = [x for x in data]
            self.intervals.sort(key=lambda x: x.begin)

    def __len__(self):
        return len(self.intervals)

    def __str__(self):
        return str([str(x) for x in self.intervals])

    @staticmethod
    def intersection(self: 'MultiInterval', other: 'MultiInterval') -> 'MultiInterval':
        new = MultiInterval()
        for interval in self.intervals:
            for other_interval in other.intervals:
                _intersection = interval.intersection(other_interval)
                if _intersection is not None:
                    new.intervals.append(_intersection)
                    break
        return new

    @staticmethod
    def union(self: 'MultiInterval', other: 'MultiInterval') -> 'MultiInterval':
        new = MultiInterval()
        for interval in self.intervals:
            for other_interval in other.intervals:
                _intersection = interval.intersection(other_interval)
                if _intersection is not None:
                    new.intervals.append(interval.union(other_interval))
                    break
                else:
                    if interval not in new.intervals:
                        new.intervals.append(interval)
                    if other_interval not in new.intervals:
                        new.intervals.append(other_interval)

        new.intervals = set(new.intervals)
        new.intervals = list(new.intervals)
        new.intervals.sort(key=lambda x: x.begin)

        united = MultiInterval()
        i = 0
        while i < len(new) - 1:
            if new.intervals[i].intersection(new.intervals[i + 1]) is None:
                united.intervals.append(new.intervals[i])
                united.intervals.append(new.intervals[i + 1])
            else:
                united.intervals.append(new.intervals[i].intersection(new.intervals[i + 1]))
            i += 1
        return united
