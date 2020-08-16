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
        return f'Location:\n\tX: {self._x}\n\tY: {self._y}'
