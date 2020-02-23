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
        self.assertIn('Top Layer', pcblib.layers)
        self.assertIn('Bottom Layer', pcblib.layers)
        self.assertIn('Top Paste', pcblib.layers)
        self.assertIn('Bottom Paste', pcblib.layers)
        self.assertIn('Top Solder', pcblib.layers)
        self.assertIn('Bottom Solder', pcblib.layers)
        self.assertIn('Top Overlay', pcblib.layers)
        self.assertIn('Bottom Overlay', pcblib.layers)
        self.assertIn('Multi-Layer', pcblib.layers)
        self.assertIn('Drill Guide', pcblib.layers)
        self.assertIn('Keep-Out Layer', pcblib.layers)
        self.assertIn('Drill Drawing', pcblib.layers)
        self.assertIn('Mechanical 13', pcblib.layers)
        self.assertIn('Mechanical 15', pcblib.layers)
        self.assertIn('Mechanical 17', pcblib.layers)
        self.assertIn('Mechanical 19', pcblib.layers)

        

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
    def test_3d_model_on_layer_13(self, f):
        for footprint in f.Footprints:
            x = footprint.Body3D
            for body3d in x:
                self.assertEqual('MECHANICAL13', body3d.layer_name)

    @for_all_pcblibs
    def test_letter_d_on_layer_17(self, f):
        for footprint in f.Footprints:
            texts = footprint.Text

            found = False
            for i in texts:
                if i.text == 'd':
                    if i.layer_id == f.layers['Mechanical 17']:
                        found = True

            self.assertTrue(found, "Cannot find d on layer 17")

    @for_all_pcblibs
    def test_dash_on_layer_19(self, f):
        for footprint in f.Footprints:
            texts = footprint.Text

            found = False
            for i in texts:
                if i.text == '-':
                    if i.layer_id == f.layers['Mechanical 19']:
                        found = True

            self.assertTrue(found, "Cannot find - on layer 19")

    @for_all_pcblibs
    def test_correct_name_for_typical_packages(self, f):
        for footprint in f.Footprints:
            n = footprint.name

            def test_format(text, prefix):
                if n.startswith(prefix):
                    self.assertRegex(text, prefix + "\\d+_[\\d\\.]+x[\\d\\.]+$")

            test_format(n, "DFN")
            test_format(n, "LGA")
            test_format(n, "LQFP")
            test_format(n, "QFN")
            test_format(n, "TQFP")
            test_format(n, "TSSOP")
            test_format(n, "VQFN")
            test_format(n, "VSON")
            test_format(n, "VSSOP")
            test_format(n, "WQFN")
            test_format(n, "WSON")

    @for_all_pcblibs
    def test_pcblib_designator_name(self, pcblib):
        exposed_pads = []

        for footprint in pcblib.Footprints:
            for r in footprint.Pad:
                self.assertRegex(r.Designator, "^(EP[1-9]|MH\\d?|\\d+|[A-Z]+\\d+|DNC|GND|IN|OUT)$")
                if r.Designator.find('EP') != -1:
                    exposed_pads.append(int(r.Designator[2:]))
        
        exposed_pads = list(set(sorted(exposed_pads)))
        for i in range(0, len(exposed_pads)):
            self.assertEqual(i+1, exposed_pads[i], "Exposed pads not numbered correctly (on pad EP{})".format(exposed_pads[i]))
