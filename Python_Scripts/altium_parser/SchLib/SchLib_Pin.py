from .sch_data_pack import DataPack
from enum import Enum


class Color:
    def __init__(self, data):
        self.R = data.read_U8()
        self.G = data.read_U8()
        self.B = data.read_U8()

class Pin_ElectricalType(Enum):
    Input = 0
    IO = 1
    Output = 2
    OpenCollector = 3
    Passive = 4
    HiZ = 5
    OpenEmitter = 6
    Power = 7

class Pin_Symbols_Inside:
    NoSymbol = 0
    PostponedOutput = 1
    OpenCollector = 2
    HiZ = 3
    HighCurrent = 4
    Pulse = 5
    Schmitt = 6
    OpenCollectorPullUp = 7
    OpenEmitter = 8
    OpenEmitterPullUp = 9
    ShiftLeft = 10
    OpenOutput = 11


class Pin_Symbols_InsideEdge:
    NoSymbol = 0
    Clock = 3


class Pin_Symbols_OutsideEdge:
    NoSymbol = 0
    Dot = 1
    ActiveLowInput = 4
    ActiveLowOutput = 17


class Pin_Symbols_Outside:
    NoSymbol = 0
    RightLeftSignalFlow = 1
    AnalogSignalIn = 2
    NotLogicConnection = 3
    DigitalSignalIn = 4
    LeftRightSignalFlow = 5
    BidirectionalSignalFlow = 6


class Pin_Symbols_LineWidth:
    Smallest = 0
    Small = 1


class Pin:
    #
    # Parse pin properties from binary string
    # e.g. as read from a SchLib file
    #

    def __init__(self, data: DataPack):
        # 0: 0x02 = Record Type: Pin
        data.check(b'\x02')

        # unknown (0x 00 00 00 00)
        data.check(4 * b'\x00')

        # Part number (from 1)
        self.part_number = data.read_U8()

        # unknown (0x 00)
        data.check(b'\x00')

        # Alternate mode nr (from 0)
        self.alternate_mode = data.read_U8()

        # Symbols -> Inside Edge
        self._symbols_inside_edge = data.read_U8()

        # Symbols -> Outside Edge
        self._symbols_outside_edge = data.read_U8()

        # Symbols -> Inside
        self._symbols_inside = data.read_U8()

        # Symbols -> Outside
        self._symbols_outside = data.read_U8()

        # Description
        strlen = data.read_U8()
        self.description = data.read_bytes(strlen).decode('ascii')

        # one byte: unknown
        data.skip(1)

        # one byte: Electrical Type
        self.electrical_type = Pin_ElectricalType(data.read_U8() & 0x0f)

        # 15: lower two or four bits are for pin orientation
        b = data.read_U8()
        self.display_name_visible = (b & 0x08) > 0  # LSB of higher nibble
        self.designator_visible = (b & 0x10) > 0  # MSB of lower nibble
        self.pin_hidden = (b & 0x04) > 0
        self.orientation = (b & 0x03) * 90

        # 16-17: Graphical->Length
        # The pin length is a signed? little-endian 16-bit short integer
        # e.g. 0x1400 => 0020 + "0" => 200mil
        self.length = data.read_I16() * 10

        # 18-19: X
        # 20-21: Y
        # X and Y are signed little-endian 16-bit short integers
        self.X = data.read_I16() * 10
        self.Y = data.read_I16() * 10

        # three bytes: RGB color
        self.color = Color(data)

        # one byte: unknown (0x00)
        data.check(b'\x00')

        # 26...: Display Name and Designator
        strlen = data.read_U8()
        self.display_name = data.read_bytes(strlen).decode('ascii')

        strlen = data.read_U8()
        self.designator = data.read_bytes(strlen).decode('ascii')

        # last three bytes: unknown