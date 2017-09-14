import numpy as np


class Extrapolate(object):
    """Given two input lists representing two axis, this class is able to
    extrapolate the preceding X value
    """

    def __init__(self, x_list, y_list):
        self.xp = x_list
        self.yp = y_list

    def extrap(self, x):
        """np.interp function with linear extrapolation"""
        y = np.interp(x, self.xp, self.yp)
        y = np.where(x < self.xp[0],
                     self.yp[0] + (x - self.xp[0]) * (self.yp[0] - self.yp[1]) / (self.xp[0] - self.xp[1]),
                     y)
        y = np.where(x > self.xp[-1],
                     self.yp[-1] + (x - self.xp[-1]) * (self.yp[-1] - self.yp[-2]) / (self.xp[-1] - self.xp[-2]),
                     y)
        return y

    def __getitem__(self, x):
        return self.extrap(x)
