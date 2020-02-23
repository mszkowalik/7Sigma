from .BinarySubRecord import *


class SubRecord_Text:
    def __init__(self, data):
        self.common = SubRecord_Common(data)

        self.X = data.read_I32() / 10000.
        self.Y = data.read_I32() / 10000.
        self.Height = data.read_I32() / 10000.

        # Something about Stroke Font Number here
        data.skip(1)

        data.check(b'\x00')

        self.Rotation = data.read_Float64()

        data.skip(191)

        self.layer_id = data.read_U32()


class Text:
    def __init__(self, data):
        SubRecord_Text.__init__(self, data.subrecord())
        self.text = SubRecord_String(data.subrecord())

    def __str__(self):
        return self.text + " @({}, {})".format(self.X, self.Y)