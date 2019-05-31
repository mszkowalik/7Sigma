from unittest import TestCase

import warnings
import parse
import re

from for_all_elements import for_all_elements


for_all_parts = for_all_elements(parse.database, lambda x: x.part_number)

for_all_capacitors = for_all_elements(parse.database_files['Capacitors'], lambda x: x['Part Number'])
all_capacitors_part_numbers = [i['Part Number'] for i in parse.database_files['Capacitors']]

for_all_resistors = for_all_elements(parse.database_files['Resistors'], lambda x: x['Part Number'])
all_resistors_part_numbers = [i['Part Number'] for i in parse.database_files['Resistors']]

for_all_inductors = for_all_elements(parse.database_files['Inductors'], lambda x: x['Part Number'])

for_all_diodes = for_all_elements(parse.database_files['Diodes'], lambda x: x['Part Number'])


class TestDatabase(TestCase):
    def setUp(self):
        self.capacitors_already = set()
        self.resistors_already = set()

    def is_metric(self, value, allowed_prefix='n|u|m||k|M', unit='', prefix_without_lower_bound=None, bounds=(1, 1000), msg='Incorrect value format'):
        found = re.findall('^(([1-9]\d*|0)(\.\d*[1-9])?)(' + allowed_prefix + ')' + unit + '$', value)

        msg = msg + ": " + value
        self.assertEqual(1, len(found), msg)

        val = float(found[0][0])
        prefix = found[0][-1]

        self.assertEqual(found[0][0] + prefix + unit, value, "Test issue in element " + value)

        if prefix != prefix_without_lower_bound:
            self.assertGreaterEqual(val, bounds[0], msg)

        self.assertLess(val, bounds[1], msg)

    @for_all_parts
    def test_datasheet_valid_url(self, part):
        if part.datasheet != '-':
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                import validators
                self.assertTrue(validators.url(part.datasheet), "Invalid HelpURL!")

    @for_all_parts
    def test_proper_suppliers(self, part):
        self.assertEqual(part.row['Supplier 1'], "TME")
        self.assertEqual(part.row['Supplier 2'], "RS Components")
        self.assertEqual(part.row['Supplier 3'], "Farnell")
        self.assertEqual(part.row['Supplier 4'], "Mouser")
        self.assertEqual(part.row['Supplier 5'], "Digi-Key")

        if part.row['Supplier 6'] != '':
            self.assertNotEqual('', part.row['Supplier Part Number 6'], "Supplier Part Number 6")
        if part.row['Supplier Part Number 6'] != '':
            self.assertNotEqual('', part.row['Supplier 6'], "Supplier 6")
            
        suppliers = set()
    
        for i in range(1, 6):
            if  part.row['Supplier Part Number ' + str(i)] != '':
                suppliers.add(part.row['Supplier ' + str(i)])
        #print(part.row['Part Number'], suppliers)
        self.assertTrue(len(suppliers) > 1 or part.row['Supplier 6'] != '' or ('TME' in suppliers) or ('RS Components' in suppliers),
            "Supplier requierements not met")
        
    @for_all_parts
    def test_manufacturer_filled(self, part):
        self.assertIn(part.manufacturer, parse.manufacturers, "Incorrect Manufacturer")
        # '-' means no manufacturer, then part number should be also '-'
        if part.manufacturer == '-':
            self.assertEqual('-', part.manufacturer_part_number, "Manufacturer part number should be '-' when Manufacturer == '-'")
        else:
            self.assertNotEqual('', part.manufacturer_part_number, "Manufacturer part number not filled")

    @for_all_parts
    def test_no_space(self, part):
        self.assertNotRegex(part.row['Part Number'], '\s', "Whitespace in field Part Number")
        self.assertNotRegex(part.row['Library Ref'], '\s', "Whitespace in field Library ref")
        self.assertNotRegex(part.row['Footprint Ref'], '\s', "Whitespace in field Footpint Ref")
            
    @for_all_parts
    def test_no_whitespace_except_space(self, part):
        for i in part.row:
            self.assertNotRegex(part.row[i], '\r|\n|\t', "Whitespace in field |" + part.row[i] + "|")

    @for_all_parts
    def test_no_whitespace_at_begin_or_end_of_each_field(self, part):
        for i in part.row:
            self.assertEqual(part.row[i].strip(), part.row[i], "Whitespace in field |" + part.row[i] + "|")

    @for_all_capacitors
    def test_database_capacitors(self, row):
        part_number = row['Part Number']
        footprint = row['SCH_Footprint'] 
        voltage = row['Voltage']
        value = row['Value']
        dielectric = row['Dielectric']
        tolerance = row['Tolerance (%)']
        
        sch = row['Library Ref']
        pcb = row['Footprint Ref']

        self.assertNotIn(part_number, self.capacitors_already)
        self.capacitors_already.add(part_number)

        if part_number.find("C_GENERIC_") != -1:
            return

        self.is_metric(voltage, '|k', 'V')
        self.assertNotEqual(-1, pcb.find(footprint), "\"Sch_Footprint\" string is not a part of \"Footprint Ref\"")

        self.is_metric(value, 'p|n|u|m', 'F', prefix_without_lower_bound='p')

        dielectrics = {'C0G', 'X5R', 'X7R', 'X6S', 'U2J', 'Y5U', 'PP', 'AL2O3', 'TA2O5', 'Polymer'}
        self.assertIn(dielectric, dielectrics)

        tolerance = str(tolerance).rstrip('0').rstrip('.')
        self.is_metric(tolerance, prefix_without_lower_bound='', bounds=(0, 100))
        tolerance_float = float(tolerance)

        prefix = part_number[:part_number.index("_")]
        prefixes = {'C', 'CE', 'CT'}
        self.assertIn(prefix, prefixes)

        expected = prefix + "_" + value + "_" + voltage + "_" + dielectric + "_" + footprint + "_" + tolerance
        
        found = re.findall('^' + expected + "(|_(\d))$", part_number)

        if len(found) == 1 and found[0][1] != '':
            nr = int(found[0][1])
            
            self.assertIn(expected, all_capacitors_part_numbers, "Multiple capacitors wrong numeration!")
            for i in range(2, nr):
                s = expected + "_{}".format(i)
                #print(s)
                self.assertIn(s, all_capacitors_part_numbers, "Multiple capacitors wrong numeration!")
        else:
            self.assertEqual(expected, part_number, "Incorrect value format!")

    @for_all_resistors
    def test_database_resistors(self, row):
        part_number = row['Part Number']
        footprint = row['SCH_Footprint']
        comment = row['Comment']
        voltage = row['Voltage']
        power = row['Power']
        value = row['Value']
        tolerance = row['Tolerance']

        sch = row['Library Ref']
        pcb = row['Footprint Ref']

        self.assertNotIn(part_number, self.resistors_already)
        self.resistors_already.add(part_number)

        if part_number.find("R_GENERIC_") != -1:
            return

        self.assertEqual("Resistor", comment)
        self.is_metric(voltage, 'm|k|', 'V', msg="Incorrect voltage")
        self.is_metric(power, 'm|', 'W', msg="Incorrect power")
        if value != "0R":
            self.is_metric(value, 'm|R|k|M|G', msg="Incorrect value")
        self.is_metric(tolerance, '', '%', bounds=(0, 100))

        self.assertNotEqual(-1, pcb.find(footprint), "Footprint not found in Part Number")

        expected = 'R_' + value + '_' + footprint + '_' + tolerance[:-1]
        self.assertEqual(expected, part_number)

    @for_all_inductors
    def test_database_inductors(self, row):
        part_number = row['Part Number']
        footprint = row['SCH_Footprint']
        comment = row['Comment']
        current = row['Current']
        resistance = row['Resistance']
        value = row['Value']

        if value == 'NC' or re.search('^(CORE_)', part_number) or re.search('(\d*)PIN_(\d)', part_number):
            return

        if comment == 'Inductor' or comment == 'Ferrite bead' or comment == 'Common mode filter':
            self.is_metric(current, 'm|', 'A', msg='Current')
            self.is_metric(resistance, 'm|k|', 'R', msg='Resistance')

        if comment == 'Inductor':
            self.is_metric(value, 'n|u|m', 'H', msg="Value")
            expected = '^LM?_' + value + '_' + current + '_' + footprint
            self.assertRegex(part_number, expected)
