import os

from olefile import OleFileIO

from .BinarySubRecord import *
from .PcbLib_Footprint import Footprint
from .common import *
from .pcb_data_pack import DataPack


#
# A PCB library (PcbLib) stores PCB components' footprints 
#
class PcbLib:

    #
    # Open and parse PcbLib file
    #
    def __init__(self, filename):
        self.filename = os.path.splitext(os.path.basename(filename))[0]

        self.OleFile = OleFileIO(filename)

        #
        # Parse library parameters
        # Library/Data contains a list of parameters (string: "|"-separated key-value pairs)
        # followed by the count and names of footprints in the library
        #
        buffer = self.readStream("Library/Data")

        # Properties
        self.Properties = parseKeyValueString(buffer.subrecord().read())

        # Footprint list
        count = buffer.read_U32()

        footprints = []
        for _ in range(count):
            name = SubRecord_String(buffer.subrecord())
            footprints.append(name)

        # Parse all the footprints
        self.Footprints = []
        for footprint in footprints:
            if len(footprint) > 31:
                footprint = footprint[:31]

            self.Footprints.append(Footprint(self.readStream(footprint + "/Data")))

        # Parse layers from Properties
        self.parse_layers()

        self.OleFile.close()

    #
    # Read file from OLE container and return it's contents
    #
    def readStream(self, path):
        f = self.OleFile.openstream(path)
        return DataPack(f.read())

    def parse_layers(self):
        self.layers = {}
        self.layers_by_id = {}
        for key in self.Properties:
            if key.find('LAYERID') >= 0:
                id = int(self.Properties[key])
                name = self.Properties[key[:-7] + "NAME"]

                if name not in self.layers:
                    self.layers[name] = id

                if name not in self.layers_by_id:
                    self.layers_by_id[id] = name
                
                assert self.layers[name] == id
                assert self.layers_by_id[id] == name
