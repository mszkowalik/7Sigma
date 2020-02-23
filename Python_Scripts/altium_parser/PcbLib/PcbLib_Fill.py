from .BinarySubRecord import *


class SubRecord_Fill:
    def __init__(self, data):
        self.common = SubRecord_Common(data)

        self.X1 = data.read_I32() / 10000.
        self.Y1 = data.read_I32() / 10000.
        self.X2 = data.read_I32() / 10000.
        self.Y2 = data.read_I32() / 10000.

        self.Rotation = data.read_Float64()


class Fill:
    def __init__(self, data):
        SubRecord_Fill.__init__(self, data.subrecord())

    def __str__(self):
        return "@({}, {})".format(self.X1, self.Y1, self.X2, self.Y2)
