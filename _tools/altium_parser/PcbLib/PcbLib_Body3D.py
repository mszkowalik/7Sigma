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
        # pprint(dict)
        self.layer_name = self.dict['V7_LAYER']




class Body3D:
    def __init__(self, data):
        SubRecord_Body3D.__init__(self, data.subrecord())

    def __str__(self):
        return "3D Body @{}".format(self.layer_name)
