from unittest import TestCase

import parse
from PcbLib.PcbLib_Body3D import Body3D
from PcbLib.PcbLib_Pad import Pad
from PcbLib.PcbLib_Text import Text

from for_all_elements import for_all_elements


for_all_pcblibs = for_all_elements(parse.pcblibs, lambda x: x.filename)


class TestPcbLibs(TestCase):
    @for_all_pcblibs
    def test_one_file_in_pcblib(self, f):
        self.assertEqual(1, len(f.Footprints))

    @for_all_pcblibs
    def test_footprint_name_same_as_filename(self, f):
        self.assertEqual(f.filename, f.Footprints[0].name)

    @for_all_pcblibs
    def test_no_duplicated_pads_designators(self, pcblib):
        for footprint in pcblib.Footprints:
            already = set()            
            for r in footprint.Pad:
                name = r.Designator
                if name == "DNC" or name[0:2] == "MH" or name == "GND":
                    continue
                self.assertNotIn(name, already)
                already.add(name)

    @for_all_pcblibs
    def test_correct_layer_names(self, pcblib):
        layers = ['Top Layer','Bottom Layer','Top Paste','Bottom Paste','Top Solder','Bottom Solder','Top Overlay','Bottom Overlay','Multi-Layer','Drill Guide','Top 3D Body','Bottom 3D Body','Top Assembly','Bottom Assembly','Top Courtyard','Bottom Courtyard']
        # '3D Body Bottom','3D Body Top','Courtyard Bottom','Courtyard Top','Assembly Bottom','Assembly Top',
        for layer in layers:
            self.assertIn(layer, pcblib.layers, layer + " not found")    

        

    @for_all_pcblibs
    def test_pads_on_top_or_multi_layer(self, pcblib):
        for footprint in pcblib.Footprints:
            for r in footprint.Pad:
                id = r.SizeAndShape.layer_id
                if 'Top Layer' not in pcblib.layers or 'Bottom Layer' not in pcblib.layers or 'Multi-Layer' not in pcblib.layers:
                    continue

                self.assertEqual((id != pcblib.layers['Top Layer']) and (id != pcblib.layers['Bottom Layer']) and
                                 (id != pcblib.layers['Multi-Layer']), False,
                                 "Pad on wrong layer " + pcblib.filename + " -> " + pcblib.layers_by_id[id])

    @for_all_pcblibs
    def test_no_empty_names(self, f):
        for footprint in f.Footprints:
            self.assertNotEqual("", footprint.name)

    @for_all_pcblibs
    def test_3d_model_exists(self, f):
        for footprint in f.Footprints:
            x = footprint.Body3D
            self.assertIsNotNone(x,"No  3D model on footprint{}".format(footprint.name))

            # for body3d in x:
            #     self.assertEqual('MECHANICAL13', body3d.layer_name)

    # @for_all_pcblibs
    # def test_letter_d_on_layer_17(self, f):
    #     for footprint in f.Footprints:
    #         texts = footprint.Text

    #         found = False
    #         for i in texts:
    #             if i.text == 'd':
    #                 if i.layer_id == f.layers['Mechanical 17']:
    #                     found = True

    #         self.assertTrue(found, "Cannot find d on layer 17")

    # @for_all_pcblibs
    # def test_dash_on__layer(self, f):
    #     for footprint in f.Footprints:
    #         texts = footprint.Text

    #         found = False
    #         for i in texts:
    #             if i.text == '-':
    #                 if i.layer_id == f.layers['Top Courtyard']:
    #                     found = True

    #         self.assertTrue(found, "Cannot find - on layer 19")

    @for_all_pcblibs
    def test_correct_name_for_typical_packages(self, f):
        for footprint in f.Footprints:
            n = footprint.name

            def test_format(text, prefix, regex):
                if n.startswith(prefix):
                    self.assertRegex(text, prefix + regex)

            test_format(n, "DFN", "\d{1,2}P\d{1,3}X\d{1,3}X\d{1,3}-\d{1,3}[A-Z]{1}")
            test_format(n, "LGA", "\d{1,2}P\d{1,3}X\d{1,3}X\d{1,3}-\d{1,3}[A-Z]{1}")
            test_format(n, "LQFP", "\d{1,2}P\d{1,3}X\d{1,3}X\d{1,3}-\d{1,3}[A-Z]{1}")
            test_format(n, "QFN", "\d{1,2}P\d{1,3}X\d{1,3}X\d{1,3}-\d{1,3}[A-Z]{1}")
            test_format(n, "TQFP", "\d{1,2}P\d{1,3}X\d{1,3}X\d{1,3}-\d{1,3}[A-Z]{1}")
            test_format(n, "TSSOP", "\d{1,2}P\d{1,3}X\d{1,3}X\d{1,3}-\d{1,3}[A-Z]{1}")
            test_format(n, "VQFN", "\d{1,2}P\d{1,3}X\d{1,3}X\d{1,3}-\d{1,3}[A-Z]{1}")
            test_format(n, "VSON", "\d{1,2}P\d{1,3}X\d{1,3}X\d{1,3}-\d{1,3}[A-Z]{1}")
            test_format(n, "VSSOP", "\d{1,2}P\d{1,3}X\d{1,3}X\d{1,3}-\d{1,3}[A-Z]{1}")
            test_format(n, "WQFN", "\d{1,2}P\d{1,3}X\d{1,3}X\d{1,3}-\d{1,3}[A-Z]{1}")
            test_format(n, "WSON", "\d{1,2}P\d{1,3}X\d{1,3}X\d{1,3}-\d{1,3}[A-Z]{1}")

    @for_all_pcblibs
    def test_pcblib_designator_name(self, pcblib):
        
        for footprint in pcblib.Footprints:
            for r in footprint.Pad:
                self.assertRegex(r.Designator, "^(MH\\d?|\\d+|[A-Z]+\\d+|DNC|GND|IN|OUT)$")
                
