from unittest import TestCase
import warnings
import parse
import re

from for_all_elements import for_all_elements

for_all_parts = for_all_elements(parse.database, lambda x: x.part_number)

class TestDatabase(TestCase):
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
        self.assertNotEqual(part.datasheet,None, "HelpURL is null")
        self.assertTrue(part.datasheet,"HelpURL is Empty")
        # if part.datasheet != '-' and part.datasheet != None:
        #     with warnings.catch_warnings():
        #         warnings.filterwarnings("ignore", category=DeprecationWarning)
        #         import validators
        #         self.assertTrue(validators.url(part.datasheet), "Invalid HelpURL!")

    @for_all_parts
    def test_no_whitespace_at_begin_or_end_of_each_field(self, part):
        for i in part.dictionary.values():
            if type(i) == str:
                self.assertEqual(i.strip(), i, "Whitespace in field |" + i + "|")

if __name__ == '__main__':
    unittest.main()

