def SubRecord_String(subrecord):
    # verify string length
    length = subrecord.read_U8()
    assert length == len(subrecord)
    return subrecord.read().decode('ascii')


#
# There is a SubRecord that can be found
# in all PCB Component records so far
# but is yet of unknown purpose.
# The length appears to be always 13. 
#
class SubRecord_Common:
    def __init__(self, data):
        # First byte:
        # Line: 0x39
        # Pad SizeAndShape: 0x4A or 0x01
        # Arc:  0x21
        # 3D Body: 0x45
        # Fill: 0x39

        # The remaining bytes are always the same:
        # 0x 0C 00
        # 10x 0xFF
        self.unknown = data.read_bytes(3)
        data.check(10 * b'\xFF')
