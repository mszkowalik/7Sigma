import os
from unittest import TestCase

from SchLib.SchLib import SchLib
from SchLib.SchLib_Pin import Pin_ElectricalType


class TestSchLib(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sch = SchLib(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SchLib/test.SchLib'))

    def test_component_count(self):
        self.assertEqual(2, len(self.sch.libraries))

    def test_component_names(self):
        self.assertEqual("testowo", self.sch.libraries[0].name)
        self.assertEqual("xyzabc", self.sch.libraries[1].name)

    def test_component_part_count(self):
        self.assertEqual(1, self.sch.libraries[1].part_count)
        self.assertEqual(2, self.sch.libraries[0].part_count)

    def test_component_display_mode_count(self):
        self.assertEqual(2, self.sch.libraries[1].display_mode_count)
        self.assertEqual(1, self.sch.libraries[0].display_mode_count)

    def test_text(self):
        self.assertEqual(2, len(self.sch.libraries[0].text_labels))

        text = self.sch.libraries[0].text_labels[0]
        self.assertEqual("Text on testowo Part A", text.text)
        self.assertEqual(-456.75, text.X)
        self.assertEqual(-2563.52, text.Y)
        self.assertEqual(1, text.owner_id)

        text = self.sch.libraries[0].text_labels[1]
        self.assertEqual("Text on testowo Part B", text.text)
        self.assertEqual(443.25, text.X)
        self.assertEqual(236.48, text.Y)
        self.assertEqual(2, text.owner_id)
        self.assertEqual(123, text.color.R)
        self.assertEqual(98, text.color.G)
        self.assertEqual(173, text.color.B)

    def test_designators(self):
        self.assertEqual("AAA?", self.sch.libraries[0].designator.text)
        self.assertEqual("X", self.sch.libraries[1].designator.text)

    def test_parameters(self):
        self.assertEqual(2, len(self.sch.libraries[1].parameters))

        p = self.sch.libraries[1].parameters[0]
        self.assertEqual(-15, p.X)
        self.assertEqual(-157, p.Y)
        self.assertEqual(0, p.color.R)
        self.assertEqual(50, p.color.G)
        self.assertEqual(128, p.color.B)
        self.assertEqual("test1", p.text)
        self.assertEqual("SCH_ABC", p.name)

        p = self.sch.libraries[1].parameters[1]
        self.assertEqual("comm?", p.text)
        self.assertEqual("Comment", p.name)

        self.assertEqual(1, len(self.sch.libraries[0].parameters))
        p = self.sch.libraries[0].parameters[0]
        self.assertEqual("*", p.text)
        self.assertEqual("Comment", p.name)


    def test_pin(self):
        pins = self.sch.libraries[0].pins
        self.assertEqual(2, len(pins))

        p = pins[1]
        self.assertEqual("Testowy opis", p.description)
        self.assertEqual("NAMEA1", p.display_name)
        self.assertEqual("A1", p.designator)
        self.assertEqual(1, p.part_number)
        self.assertEqual(0, p.orientation)
        self.assertEqual(True, p.display_name_visible)
        self.assertEqual(False, p.designator_visible)
        self.assertEqual(-570, p.length)
        self.assertEqual(-270, p.X)
        self.assertEqual(-200, p.Y)
        self.assertEqual(123, p.color.R)
        self.assertEqual(45, p.color.G)
        self.assertEqual(175, p.color.B)
        self.assertEqual(False, p.pin_hidden)

        p = pins[0]
        self.assertEqual("pis2", p.description)
        self.assertEqual("AAA2", p.display_name)
        self.assertEqual("3", p.designator)
        self.assertEqual(2, p.part_number)
        self.assertEqual(90, p.orientation)
        self.assertEqual(False, p.display_name_visible)
        self.assertEqual(True, p.designator_visible)
        self.assertEqual(330, p.length)
        self.assertEqual(600, p.X)
        self.assertEqual(-500, p.Y)
        self.assertEqual(0, p.color.R)
        self.assertEqual(0, p.color.G)
        self.assertEqual(0, p.color.B)
        self.assertEqual(True, p.pin_hidden)

    def find_pin(self, pins, designator):
        for i in pins:
            if i.designator == str(designator):
                return i
        self.fail()

    def test_pin_electrical_type(self):
        pins = self.sch.libraries[1].pins
        self.assertEqual(9, len(pins))

        mapa = {
            1: Pin_ElectricalType.Input,
            2: Pin_ElectricalType.IO,
            3: Pin_ElectricalType.Output,
            4: Pin_ElectricalType.OpenCollector,
            5: Pin_ElectricalType.Passive,
            6: Pin_ElectricalType.HiZ,
            7: Pin_ElectricalType.OpenEmitter,
            8: Pin_ElectricalType.Power
        }
        for i in mapa:
            self.assertEqual(mapa[i], self.find_pin(pins, i).electrical_type)

    def test_pin_alternate_mode(self):
        pins = self.sch.libraries[0].pins
        for i in pins:
            if i.designator == "ALT1":
                self.assertEqual(1, i.alternate_mode)
            else:
                self.assertEqual(0, i.alternate_mode)