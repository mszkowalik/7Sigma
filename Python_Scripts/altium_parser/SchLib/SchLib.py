import os

from olefile.olefile import OleFileIO

from .SchLib_Pin import Pin
from .SchLib_Properties import parse_properties
from .common import parseKeyValueString
from .sch_data_pack import DataPack


class SchLib:
    def __init__(self, filename):
        self.filename = os.path.splitext(os.path.basename(filename))[0]
        self.libraries = []

        self._ole = OleFileIO(filename)

        libraries = self.parse_header()

        self.parse_libraries(libraries)

        self._ole.close()

    def parse_header(self):
        data = self._ole.openstream(['FileHeader']).read()
        data = DataPack(data)

        libraries = []

        dic = parseKeyValueString(data.subrecord().data.read())

        for key in dic:
            if key.find("LIBREF") == 0:
                libraries.append(dic[key][:31])
        return libraries

    def parse_libraries(self, libraries):
        for name in libraries:
            data = DataPack(self._ole.openstream([name, 'Data']).read())
            self.libraries.append(self.Library(data))
        self.libraries.sort(key=lambda x: x.name)

    class Library:
        def __init__(self, data):
            self.pins = []
            self.name = ""
            self.part_count = 0
            self.display_mode_count = 0
            self.text_labels = []
            self.designator = None
            self.parameters = []

            while len(data) > 0:
                record = data.subrecord()

                if record.type == 0:
                    parse_properties(self, record.data)
                elif record.type == 1:
                    self.pins.append(Pin(record.data))
                else:
                    assert False, "incorrect record " + record.type

            self.pins.sort(key=lambda x: x.designator)