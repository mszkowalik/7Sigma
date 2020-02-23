from .BinarySubRecord import *

Shape_Round = 1
Shape_Rectangular = 2
Shape_Octagon = 3
# Shape_RoundedRectangle = 1


class SubRecord_SizeAndShape:
    def __init__(self, data):
        self.common = SubRecord_Common(data)

        # Location: Refers to the center of the pad
        # Units: mils
        self.X = data.read_I32() / 10000.
        self.Y = data.read_I32() / 10000.

        # Size and Shape
        self.XSize_Top = data.read_I32() / 10000.
        self.YSize_Top = data.read_I32() / 10000.
        self.XSize_Middle = data.read_I32() / 10000.
        self.YSize_Middle = data.read_I32() / 10000.
        self.XSize_Bottom = data.read_I32() / 10000.
        self.YSize_Bottom = data.read_I32() / 10000.

        # Hole Size
        self.HoleSize = data.read_I32() / 10000.

        # Pad Shape
        self.Shape_Top = data.read_U8()
        self.Shape_Middle = data.read_U8()
        self.Shape_Bottom = data.read_U8()

        self.Rotation = data.read_Float64()

        data.skip(1)
        #TODO! throws error when oblong pad
        #data.check(1 * b'\x00')
        data.skip(1)

        data.skip(1)

        data.check(4 * b'\x00')

        data.skip(3)

        # more bytes of unknown purpose
        data.check(b'\x01\x00\x04\x00')

        data.skip(20)

        data.check(3 * b'\x00')

        data.skip(7)

        data.check(10 * b'\x00')

        self.layer_id = data.read_U32()

        data.skip(3) #does not throw errors when pad with rounded edges
        #data.check(3 * b'\x00')




#
# Sometimes this record is empty / unused and length 0
# It's used though, e.g. if the shape is "Rounded Rectangle" 
#
class SubRecord_SizeAndShapeByLayer:
    def __init__(self, data):

        # assume default values
        # if subrecord is empty
        # Only 29 for Size and Shape, because Top/Middle/Bottom
        # are defined in the previous SubRecord
        self.XSize = [0 for i in range(29)]
        self.YSize = [0 for i in range(29)]
        self.Shape = [0 for i in range(29)]
        self.OffsetFromHoleCenterX = [0 for i in range(32)]
        self.OffsetFromHoleCenterY = [0 for i in range(32)]
        self.CornerRadius = [0 for i in range(32)]

        if len(data) == 0:
            return

        for i in range(29):
            self.XSize[i] = data.read_I32()

        for i in range(29):
            self.YSize[i] = data.read_I32()

        # 0x01
        for i in range(29):
            self.Shape[i] = data.read_U8()

        data.skip(5)
        #TODO! throws error when oblong pad
        #data.check(9 * b'\x00')
        data.skip(9)
        for i in range(32):
            self.OffsetFromHoleCenterX[i] = data.read_I32()

        for i in range(32):
            self.OffsetFromHoleCenterY[i] = data.read_I32()

        data.skip(33)

        # 0x3C = 60%
        # The percentage is a fraction of the half of the width/height
        # 100% = circle
        for i in range(32):
            self.CornerRadius[i] = data.read_U8()


class Pad:
    def __init__(self, data):
        # Six subrecords:
        # Designator (string)
        # unknown (binary)
        # unknown (string)
        # unknown (binary)
        # Size and Shape struct
        # Offset from Hole Center struct

        self.Designator = SubRecord_String(data.subrecord())

        _unknown1 = data.subrecord().read()
        _unknown2 = data.subrecord().read()
        _unknown3 = data.subrecord().read()

        self.SizeAndShape = SubRecord_SizeAndShape(data.subrecord())

        self.SizeAndShapeByLayer = SubRecord_SizeAndShapeByLayer(data.subrecord())

    def __str__(self):
        return "Designator = {} @({}, {})".format(self.Designator, self.SizeAndShape.X, self.SizeAndShape.Y)
