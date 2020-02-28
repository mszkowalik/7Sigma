import os
import csv
from glob import glob

from PcbLib.PcbLib import PcbLib
from SchLib.SchLib import SchLib
# from AltiumDatabase.AltiumDatabase import AltiumDatabase
from AltiumDatabase.Database_SQL import AltiumDatabase

def parse_pcblib():
    files = glob(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, 'PCB/**/*.[pP][cC][bB][lL][iI][bB]'),
        recursive=True)
    footprints = []
    for i in files:
        footprints.append(PcbLib(i))
    return footprints


def parse_schlib():
    files = glob(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, 'SCH/**/*.[sS][cC][hH][lL][iI][bB]'),
        recursive=True)

    schlibs = []
    for i in files:
        schlibs.append(SchLib(i))
    return schlibs


def get_schematics(schlibs):
    schematics = {}
    for lib in schlibs:
        for sch in lib.libraries:
            assert sch.name not in schematics, "Schematic " + sch.name + " duplicated! " \
                                               "One file: " + lib.filename
            schematics[sch.name] = sch
    return schematics


def get_footprints(pcblibs):
    footprints = {}
    for lib in pcblibs:
        for footprint in lib.Footprints:
            assert footprint.name not in footprints, "Footprint " + footprint.name + " duplicated! " \
                                                     "One file: "
            footprints[footprint.name] = footprint
    return footprints


def parse_manufacturers():
    manufacturers = set()
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            os.pardir, os.pardir, '_export', '_Manufacturers.csv')
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            manufacturers.add(row["ID"])
    return manufacturers


pcblibs = parse_pcblib()
footprints = get_footprints(pcblibs)

schlibs = parse_schlib()
schematics = get_schematics(schlibs)

# database = AltiumDatabase().database

# altium_database_class = AltiumDatabase()
# database = _altium_database_class.database
# database_files = _altium_database_class.files

# manufacturers = parse_manufacturers()

from pprint import pprint

# Uncomment to print unused libs info.
#pprint('Schematics unused:')
#pprint(schematics.keys() - {i.schlib for i in database})
#pprint('Footprints unused:')
#pprint(footprints.keys() - {i.pcblib for i in database})
