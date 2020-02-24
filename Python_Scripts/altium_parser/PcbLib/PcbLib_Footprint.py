#!/usr/bin/python
from enum import Enum

from .BinarySubRecord import *
from .PcbLib_Arc import Arc
from .PcbLib_Fill import Fill
from .PcbLib_Pad import Pad
from .PcbLib_Text import Text
from .PcbLib_Track import Track
from .PcbLib_Body3D import Body3D
from .PcbLib_Via import Via
from .PcbLib_Region import Region


#
# A PCB library contains PCB footprint definitions.
# The data of a footprint is a serialization of records.
# Records are apparently always binary-encoded
# but may contain text-based SubRecords ("|"-separated list of key=value pairs).
#
# The following record types are recognized:
#
class RecordType(Enum):
    Arc = 1  # binary
    Pad = 2  # binary
    Via = 3
    Track = 4  # binary
    Text = 5  # binary + string
    Fill = 6  # binary
    Region = 11
    Body3D = 12  # binary with text-based SubRecord


#
# A footprint as it is stored in a PcbLib:
# subfolder with footprint's name
# file "Data" in the subfolder contains the footprint composing records
#
class Footprint:

    # read Data from OleFile
    def __init__(self, datapack):
        self.datapack = datapack

        self.Arc = set()
        self.Pad = set()
        self.Via = set()
        self.Track = set()
        self.Text = set()
        self.Fill = set()
        self.Region = set()
        self.Body3D = set()

        # first entry is the footprint's name
        self.name = SubRecord_String(self.datapack.subrecord())
        # parse all records
        while len(self.datapack) > 0:
            self.parseRecord()

    def parseRecord(self):
        # The first byte defines the type of the record that follows.
        record_type = self.datapack.read_U8()

        record_map = {
            RecordType.Arc: [Arc, self.Arc],
            RecordType.Pad: [Pad, self.Pad],
            RecordType.Via: [Via, self.Via],
            RecordType.Track: [Track, self.Track],
            RecordType.Text: [Text, self.Text],
            RecordType.Fill: [Fill, self.Fill],
            RecordType.Region: [Region, self.Region],
            RecordType.Body3D: [Body3D, self.Body3D],
        }
        
        t = record_map[RecordType(record_type)]
        t[1].add(t[0](self.datapack))
