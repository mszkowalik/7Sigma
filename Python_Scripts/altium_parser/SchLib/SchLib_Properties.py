from common import parseKeyValueString


def parse_XY(self, dict):
    self.X = 0
    self.Y = 0
    if 'LOCATION.X' in dict:
        self.X = 10. * int(dict['LOCATION.X'])
    if 'LOCATION.X_FRAC' in dict:
        self.X += int(dict['LOCATION.X_FRAC']) / 10000.

    if 'LOCATION.Y' in dict:
        self.Y = 10. * int(dict['LOCATION.Y'])
    if 'LOCATION.Y_FRAC' in dict:
        self.Y += int(dict['LOCATION.Y_FRAC']) / 10000.

class Color:
    def __init__(self, dict):
        self.R = 0
        self.G = 0
        self.B = 0
        if 'COLOR' in dict:
            c = int(dict['COLOR'])
            self.R = c % 256
            self.G = (c >> 8) % 256
            self.B = (c >> 16) % 256

        self._key = str(self.R) + str(self.G) + str(self.B)

def parse_Color(self, dict):
    self.color = Color(dict)


def get_str(dict, name):
    if name in dict:
        return dict[name]
    return None


class SchLib_Component():
    def __init__(self, schlib, dict):
        schlib.name = dict['LIBREFERENCE']
        schlib.part_count = int(dict['PARTCOUNT'])-1
        schlib.display_mode_count = int(dict['DISPLAYMODECOUNT'])


class SchLib_TextLabel:
    def __init__(self, schlib, dict):
        parse_XY(self, dict)
        parse_Color(self, dict)
        self.owner_id = int(dict['OWNERPARTID'])
        self.text = dict['TEXT']

        schlib.text_labels.append(self)


class SchLib_Designator:
    def __init__(self, schlib, dict):
        parse_Color(self, dict)
        self.text = dict['TEXT']
        assert dict['NAME'] == 'Designator'

        assert schlib.designator is None
        schlib.designator = self


class SchLib_Parameter:
    def __init__(self, schlib, dict):
        parse_XY(self, dict)
        parse_Color(self, dict)
        self.text = get_str(dict, 'TEXT')
        self.name = dict['NAME']

        schlib.parameters.append(self)


class Empty:
    def __init__(self, schlib, dict):
        # print(dict)
        pass


def parse_properties(schlib, data):
    mapping = {
        1: SchLib_Component,
        3: Empty,  # IEEE symbol
        4: SchLib_TextLabel,
        5: Empty,  # Bezier
        6: Empty,  # Line
        7: Empty,  # Polygon
        8: Empty,  # Ellipse
        10: Empty,  # Rounded Rectangle
        11: Empty,  # Elliptical Arc [Deprecated]
        12: Empty,  # Arc
        13: Empty,  # Line
        14: Empty,  # Rectangle
        28: Empty,  # Text Frame
        30: Empty,  # Image
        34: SchLib_Designator,
        41: SchLib_Parameter,
        44: Empty,  # PartEnd
        45: Empty,# SIM model/ foorptint
        46: Empty # Footprint model
    }

    dict = parseKeyValueString(data.data)
    typ = int(dict["RECORD"])
    if typ == 45 or typ == 46:
        print(dict)
        modeltype = dict["MODELTYPE"]
        if modeltype != "SIM":
            assert False, "Footprint model should not be included in SchLib File: " + schlib.name
    assert typ in mapping, "type " + str(typ) + " not mapped! " + str(dict) + ", report issue!"
    mapping[typ](schlib, dict)
