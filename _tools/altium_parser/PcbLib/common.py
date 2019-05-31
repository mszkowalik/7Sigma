#
# accept string, without preceeding 4 bytes of string length
#  |a=b|c=d|0x00 ...(trailing bytes ignored)
#
# return dictionary
#  { "a": "b", "c": "d" } 
#
def parseKeyValueString(s):
    properties = s.strip(b'|').split(b'|')
    result = {}

    for prop in properties:
        x = prop.split(b'=')
        key = x[0].decode('windows-1250')
        if len(x) > 1:
            value = x[1].decode('windows-1250')
        else:
            value = ""
        result[key] = value

    return result
