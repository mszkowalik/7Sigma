from .BinarySubRecord import *


class SubRecord_Arc:
    def __init__(self, data):
        self.common = SubRecord_Common(data)

        self.X = data.read_I32() / 10000.
        self.Y = data.read_I32() / 10000.
        self.Radius = data.read_I32() / 10000.
        self.StartAngle = data.read_Float64()
        self.EndAngle = data.read_Float64()
        self.Width = data.read_I32() / 10000.


class Arc:
    def __init__(self, data):
        SubRecord_Arc.__init__(self, data.subrecord())

    def __str__(self):
        return "@({}, {})".format(self.X, self.Y)
