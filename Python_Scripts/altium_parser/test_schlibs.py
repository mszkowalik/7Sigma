from unittest import TestCase
import unittest
import itertools
import re

from SchLib.SchLib_Pin import Pin_ElectricalType

import parse
from for_all_elements import for_all_elements


all_libs = list(itertools.chain.from_iterable([schlib.libraries for schlib in parse.schlibs]))

for_all_schlibs = for_all_elements(parse.schlibs, lambda x: x.filename)
for_all_libraries = for_all_elements(all_libs, lambda x: x.name)


class TestSchLibs(TestCase):
    @for_all_schlibs
    def test_one_file_per_schlib_with_correct_name(self, schlib):
        self.assertEqual(1, len(schlib.libraries))
        self.assertEqual(schlib.filename, schlib.libraries[0].name)

    @for_all_libraries
    def test_no_empty_names(self, lib):
        self.assertNotEqual("", lib.name)

    @for_all_libraries
    def test_no_duplicated_pins_designators(self, lib):
        if len(lib.pins) == 0:
            return

        pins = {}
        for pin in lib.pins:
            if pin.alternate_mode not in pins:
                pins[pin.alternate_mode] = set()

            self.assertNotIn(pin.designator, pins[pin.alternate_mode],
                             "Duplicate pins in " + str(lib.name))
            pins[pin.alternate_mode].add(pin.designator)

        normal_mode_pins = pins[0]
        for mode in pins:
            self.assertEqual(normal_mode_pins, pins[mode],
                             "Missing pin in alternate mode! " + str(lib.name))

    @for_all_libraries
    def test_pin_length_should_not_be_zero(self, lib):
        for pin in lib.pins:
            self.assertGreater(pin.length, 0)

    @for_all_libraries
    def test_pin_length_should_be_200_mils(self, lib):
        for pin in lib.pins:
            self.assertEqual(200, pin.length)

    @for_all_libraries
    def test_schlib_designator_name(self, lib):
        for pin in lib.pins:
            self.assertRegex(pin.designator, "^(EP[1-9]|MH\\d?|\\d+|[A-Z]+\\d+|GND|IN|OUT)$")

    @for_all_libraries
    def test_gnd_should_be_power(self, lib):
        for pin in lib.pins:
            name = pin.display_name.lower()
            if name.find("gnd") != -1 or name.find("vss") != -1 or name.find("vee") != -1:
                self.assertEqual(Pin_ElectricalType.Power, pin.electrical_type, "In name: {}, {}".format(name, pin.designator))

    @for_all_libraries
    def test_power_in_should_be_input(self, lib):
        for pin in lib.pins:
            name = pin.display_name.lower()
            if (name.find('vcc') != -1 or name.find('vdd') != -1 or name.find('vin') != -1) and name.find('out') == -1:
                self.assertIn(pin.electrical_type, {Pin_ElectricalType.Input, Pin_ElectricalType.IO}, "In name: {}, {}".format(name, pin.designator))

    @for_all_libraries
    def test_outs_should_be_output(self, lib):
        for pin in lib.pins:
            name = pin.display_name.lower()
            if name.find("out") != -1:
                if pin.electrical_type != Pin_ElectricalType.Output and \
                        pin.electrical_type != Pin_ElectricalType.IO:
                    self.fail("In name: {}, {}: {}".format(name, pin.designator, pin.electrical_type))

    @for_all_libraries
    def test_ins_should_be_input(self, lib):
        for pin in lib.pins:
            name = pin.display_name.lower()
            if re.search("in($|\s)", name):
                if pin.electrical_type != Pin_ElectricalType.Input and \
                        pin.electrical_type != Pin_ElectricalType.IO:
                    self.fail("In name: {}, {}".format(name, pin.designator))

    @for_all_libraries
    def test_dnc_should_be_passive(self, lib):
        for pin in lib.pins:
            name = pin.display_name.lower()
            if name == "dnc" or name == "nc":
                self.assertEqual(Pin_ElectricalType.Passive, pin.electrical_type, "In name: {}, {}".format(name, pin.designator))

    @for_all_libraries
    def test_epad(self, lib):
        for pin in lib.pins:
            name = pin.display_name.lower()
            if name.find("pad") != -1 or pin.designator.find("EP") != -1:
                if pin.electrical_type != Pin_ElectricalType.Passive and \
                        pin.electrical_type != Pin_ElectricalType.Power:
                    self.fail("In name: {}, {}".format(name, pin.designator))
                self.assertRegex(pin.designator, "^EP\\d$")

    @for_all_libraries
    def test_pin_designators_shoud_be_visible(self, lib):
        for pin in lib.pins:
            if pin.designator == pin.display_name:
                self.assertTrue(pin.designator_visible or pin.display_name_visible, "(Designator or display name) not visible in pin: {}, {}".format(pin.display_name, pin.designator))
            else:
                self.assertTrue(pin.designator_visible, "Designator not visible in pin: {}, {}".format(pin.display_name, pin.designator))
    
    @for_all_libraries
    def test_pin_is_on_100mils_grid(self, lib):
        for pin in lib.pins:
            X = pin.X
            Y = pin.Y
            if pin.orientation == 0:
                X += pin.length
            if pin.orientation == 180:
                X -= pin.length
            if pin.orientation == 90:
                Y += pin.length
            if pin.orientation == 270:
                Y -= pin.length
            self.assertEqual(0, X % 100, "Pin " + pin.display_name + " off grid on X: {}!".format(X))
            self.assertEqual(0, Y % 100, "Pin " + pin.display_name + " off grid on Y: {}!".format(Y))

    @for_all_libraries
    def test_designator_match_prefix(self, lib):
        correct_designator = {
            'A': 'U',
            'A2': 'U',
            'A4': 'U',
            'ANT': 'ANT',
            'BUZ': 'BUZ',
            'C': 'C',
            'CB': 'CB',
            'CE': 'C',
            'CT': 'C',
            'D': 'D',
            'DB': 'DB',
            'DS': 'D',
            'DZ': 'D',
            'EF': 'EF',
            'ENC': 'ENC',
            'F': 'F',
            'FB': 'FB',
            'GDT': 'GDT',
            'J': 'J',
            'JP': 'JP',
            'L': 'L',
            'LM': 'LM',
            'CORE': 'CORE',
            'MECH': 'MECH',
            'MOD': 'MOD',
            'MOV': 'MOV',
            'NET': 'NT',
            'OC': 'OC',
            'OL': 'D',
            'P': 'P',
            'PAD': 'PAD',
            'SHIELD': 'SHIELD',
            'QN': 'Q',
            'QNP': 'Q',
            'QNS': 'Q',
            'QP': 'Q',
            'QPN': 'Q',
            'QPS': 'Q',
            'R': 'R',
            'S': 'S',
            'TP': 'TP',
            'TR': 'TR',
            'TVS': 'TVS',
            'U': 'U',
            'UP': 'U',
            'VL': 'U',
            'VS': 'U',
            'X': 'X'
        }

        prefix = lib.name.split("_")[0]
        self.assertEqual(lib.designator.text, correct_designator[prefix] + '?')


if __name__ == '__main__':
    unittest.main()
