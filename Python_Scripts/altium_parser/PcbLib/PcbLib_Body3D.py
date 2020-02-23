from .BinarySubRecord import *
from .common import parseKeyValueString


class SubRecord_Body3D:
    def __init__(self, data):
        self.common = SubRecord_Common(data)

        data.check(5 * b'\x00')

        properties = data.subrecord()
        self.dict = parseKeyValueString(properties.read_bytes(len(properties)-1))
        properties.check(b'\x00')
        assert len(properties) == 0

        # from pprint import pprint
        # pprint(self.dict)
        self.layer_name = self.dict['V7_LAYER']




class Body3D:
    def __init__(self, data):
        SubRecord_Body3D.__init__(self, data.subrecord())

    def __str__(self):
        return "3D Body @{}".format(self.layer_name)


# Dictionary positions:
# {'ARCRESOLUTION': '0.5mil',
#  'BODYCOLOR3D': '8421504',
#  'BODYOPACITY3D': '1.000',
#  'BODYPROJECTION': '0',
#  'CAVITYHEIGHT': '0mil',
#  'IDENTIFIER': '85,115,101,114,32,76,105,98,114,97,114,121,45,83,79,73,67,45,49,54,45,49',
#  'ISSHAPEBASED': 'FALSE',
#  'KIND': '0',
#  'MODEL.2D.ROTATION': '0.000',
#  'MODEL.2D.X': '0.0064mil',
#  'MODEL.2D.Y': '0.0064mil',
#  'MODEL.3D.DZ': '0mil',
#  'MODEL.3D.ROTX': '0.000',
#  'MODEL.3D.ROTY': '0.000',
#  'MODEL.3D.ROTZ': '0.000',
#  'MODEL.CHECKSUM': '4194818968',
#  'MODEL.EMBED': 'TRUE',
#  'MODEL.MODELSOURCE': 'Undefined',
#  'MODEL.MODELTYPE': '1',
#  'MODEL.NAME': 'User Library-SOIC-16-1.step',
#  'MODELID': '{1F093B0C-3855-4625-8E45-9631980E842B}',
#  'NAME': ' ',
#  'OVERALLHEIGHT': '194.8819mil',
#  'STANDOFFHEIGHT': '-194.8819mil',
#  'SUBPOLYINDEX': '-1',
#  'TEXTURE': '',
#  'TEXTURECENTERX': '0mil',
#  'TEXTURECENTERY': '0mil',
#  'TEXTUREROTATION': ' 0.00000000000000E+0000',
#  'TEXTURESIZEX': '0.0001mil',
#  'TEXTURESIZEY': '0.0001mil',
#  'UNIONINDEX': '0',
#  'V7_LAYER': 'MECHANICAL17'}