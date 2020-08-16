class Location:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def __str__(self):
        # print("{:.2f}".format(a))
        return "(X: {:.2f} Y: {:.2f})".format(self._x, self._y)
