from struct import unpack


class DataPack:
    def __init__(self, data):
        self.data = bytearray(data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def skip(self, nr_of_bytes):
        self.data[:] = self.data[nr_of_bytes:]

    def read_U8(self):
        ret = int(self.data[0])
        self.data[:] = self.data[1:]
        return ret

    def read_U32(self):
        (ret,) = unpack('<I', self.data[:4])
        self.data[:] = self.data[4:]
        return ret

    def read_I32(self):
        (ret,) = unpack('<i', self.data[:4])
        self.data[:] = self.data[4:]
        return ret

    def read_Float64(self):
        (ret,) = unpack('<d', self.data[:8])
        self.data[:] = self.data[8:]
        return ret

    def read_bytes(self, length):
        ret = self.data[:length]
        self.skip(length)
        return ret

    def read(self):
        ret = self.data[:]
        self.skip(len(ret))
        return ret

    def check(self, correct):
        length = len(correct)
        if self.data[:length] != correct:
            print(self.data[:length], "!=", correct)
            assert self.data[:length] == correct

        self.data[:] = self.data[length:]

    #
    # A SubRecord is something you find inside files named "Data"
    # extracted from an Altium PcbLib
    #
    # Several SubRecords can be present within one record,
    # e.g. Pad records consist of six SubRecords.
    #
    # A subrecord begins with 4 bytes representing the subrecord content length
    # followed by the subrecord content.
    #
    def subrecord(self):
        # first four bytes are length
        length = self.read_U32()
        return DataPack(self.read_bytes(length))
