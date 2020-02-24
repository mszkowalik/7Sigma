from .BinarySubRecord import *


class SubRecord_Track:
    def __init__(self, data):
        self.common = SubRecord_Common(data)

        self.X1 = data.read_I32() / 10000.
        self.Y1 = data.read_I32() / 10000.
        self.X2 = data.read_I32() / 10000.
        self.Y2 = data.read_I32() / 10000.

        self.Width = data.read_I32() / 10000.


class Track:
    def __init__(self, data):
        #print(data)
        SubRecord_Track.__init__(self, data.subrecord())

    def __str__(self):
        return "({}, {}) -> ({}, {})".format(self.X1, self.Y1, self.X2, self.Y2)