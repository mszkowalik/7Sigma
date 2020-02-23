from unittest import TestCase

import parse
from PcbLib.PcbLib_Pad import Pad
from for_all_elements import for_all_elements


for_all_parts = for_all_elements(parse.database, lambda x: x.part_number)


class TestParts(TestCase):
    @for_all_parts
    def test_sch_found(self, part):
        if part.schlib not in parse.schematics:
            self.fail("Schematic " + part.schlib + " not found in SchLibs! Requested by " + part.part_number)

    @for_all_parts
    def test_pcb_found(self, part):
        if part.pcblib not in parse.footprints and part.part_number.split("_")[0] != "CORE":
            self.fail("Footprint " + part.pcblib + " not found in PcbLibs! Requested by " + part.part_number)
        if part.part_number.split("_")[0] == "CORE" and part.pcblib != "":
            self.fail("Footprint for " + part.part_number + " should be empty")

    @for_all_parts
    def test_all_pins_from_schlib_are_on_pcblib(self, part):
        try:
            sch = parse.schematics[part.schlib]
            pcb = parse.footprints[part.pcblib]
        except KeyError:
            return

        pins_sch = {pin.designator for pin in sch.pins}
        pads_pcb = {record.Designator for record in pcb.Pad}

        diff = pins_sch - pads_pcb
        if diff != set():
            print(part.part_number, part.schlib, part.pcblib, diff, pins_sch, pads_pcb)

        self.assertEqual(diff, set(), "Missing pads on pcblib!")

    @for_all_parts
    def test_all_pins_from_pcblib_are_on_schlib(self, part):
        try:
            sch = parse.schematics[part.schlib]
            pcb = parse.footprints[part.pcblib]
        except KeyError:
            return

        pins_sch = {pin.designator for pin in sch.pins}
        pads_pcb = {record.Designator for record in pcb.Pad}

        diff = pads_pcb - pins_sch
        if "DNC" in diff:
            diff.remove("DNC")

        self.assertEqual(diff, set(), "Missing pins on schlib!")
