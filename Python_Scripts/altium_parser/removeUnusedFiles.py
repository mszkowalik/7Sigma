import parse
import os

dbPCBLibs = parse.database


liblist = parse.footprints.keys()


database = parse.database

dblist = list()

for part in database:
    dblist.append(part.pcblib)

unused = liblist - dblist

path = os.path.abspath(__file__ + "/../../../")
print(path)
for lib in unused:
    os.rename(path+"/PCB/"+lib+".pcblib", path+"/UNUSED/"+lib+".pcblib")