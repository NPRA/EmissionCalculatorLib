from bisect import bisect_left


class Interpolate(object):
    def __init__(self, x_list, y_list):
        if any([y - x <= 0 for x, y in zip(x_list, x_list[1:])]):
            raise ValueError("x_list must be in strictly ascending order!")
        x_list = self.x_list = list(map(float, x_list))
        y_list = self.y_list = list(map(float, y_list))
        intervals = zip(x_list, x_list[1:], y_list, y_list[1:])
        self.slopes = [(y2 - y1)/(x2 - x1) for x1, x2, y1, y2 in intervals]

    def __getitem__(self, x):
        if x <= self.x_list[0]:
            return self.y_list[0]
        elif x >= self.x_list[-1]:
            return self.y_list[-1]
        else:
            i = bisect_left(self.x_list, x) - 1
            return self.y_list[i] + self.slopes[i] * (x - self.x_list[i])

if __name__ == "__main__":
    Interpolate([],[])