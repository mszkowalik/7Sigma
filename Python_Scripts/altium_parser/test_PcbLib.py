import os
from unittest import TestCase

from PcbLib.PcbLib import PcbLib
from PcbLib.PcbLib_Arc import *
from PcbLib.PcbLib_Fill import *
from PcbLib.PcbLib_Pad import *
from PcbLib.PcbLib_Text import *
from PcbLib.PcbLib_Track import *
from PcbLib.PcbLib_Body3D import *


class TestPcbLib(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pcb = PcbLib(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'PcbLib/test.PcbLib'))

    def test_footprint(self):
        self.assertEqual("test", self.pcb.filename)
        self.assertEqual(1, len(self.pcb.Footprints))
        self.assertEqual("testaaa", self.pcb.Footprints[0].name)

        f = self.pcb.Footprints[0]
        self.assertEqual(2, len(f.Pad))
        self.assertEqual(1, len(f.Text))
        self.assertEqual(1, len(f.Arc))
        self.assertEqual(1, len(f.Fill))
        self.assertEqual(1, len(f.Track))

    def test_pad_smd(self):
        padss = None
        for i in self.pcb.Footprints[0].Pad:
            if i.Designator == 'test1':
                padss = i

        self.assertEqual("test1", padss.Designator)
        padss = padss.SizeAndShape
        self.assertEqual(0, padss.HoleSize)
        self.assertEqual(0, padss.Rotation)

        self.assertEqual(Shape_Rectangular, padss.Shape_Bottom)
        self.assertEqual(Shape_Rectangular, padss.Shape_Middle)
        self.assertEqual(Shape_Rectangular, padss.Shape_Top)

        self.assertAlmostEqual(100., padss.X)
        self.assertAlmostEqual(0., padss.Y)

        self.assertEqual(50., padss.XSize_Bottom)
        self.assertEqual(50., padss.XSize_Middle)
        self.assertEqual(50., padss.XSize_Top)

        self.assertEqual(70., padss.YSize_Bottom)
        self.assertEqual(70., padss.YSize_Middle)
        self.assertEqual(70., padss.YSize_Top)

        self.assertEqual(16777217, padss.layer_id)

    def test_pad_tht(self):
        padss = None
        for i in self.pcb.Footprints[0].Pad:
            if i.Designator == 'test2':
                padss = i

        self.assertEqual("test2", padss.Designator)
        padss = padss.SizeAndShape
        self.assertEqual(5, padss.HoleSize)
        self.assertEqual(90, padss.Rotation)

        self.assertEqual(Shape_Round, padss.Shape_Top)
        self.assertEqual(Shape_Octagon, padss.Shape_Middle)
        self.assertEqual(Shape_Round, padss.Shape_Bottom)

        self.assertAlmostEqual(padss.X, -90.)
        self.assertAlmostEqual(padss.Y, 120.)

        self.assertEqual(11., padss.XSize_Top)
        self.assertEqual(13., padss.XSize_Middle)
        self.assertEqual(15., padss.XSize_Bottom)

        self.assertEqual(12., padss.YSize_Top)
        self.assertEqual(14., padss.YSize_Middle)
        self.assertEqual(16., padss.YSize_Bottom)

        self.assertEqual(16973839, padss.layer_id)

    def test_text(self):
        t = next(iter(self.pcb.Footprints[0].Text))
        self.assertEqual('AB', t.text)
        self.assertEqual(41, t.Height)
        self.assertEqual(75, t.Rotation)
        self.assertEqual(-101, t.X)
        self.assertEqual(-79, t.Y)
        self.assertEqual(16908301, t.layer_id)

    def test_arc(self):
        arc = next(iter(self.pcb.Footprints[0].Arc))
        self.assertEqual(53, arc.X)
        self.assertEqual(149, arc.Y)
        self.assertEqual(11, arc.Width)
        self.assertEqual(32.57, arc.Radius)
        self.assertAlmostEqual(253.74, arc.StartAngle, places=2)
        self.assertAlmostEqual(31.608, arc.EndAngle, places=2)

    def test_fills(self):
        fill = next(iter(self.pcb.Footprints[0].Fill))
        self.assertEqual(90, fill.Rotation)
        self.assertEqual(-9.5, fill.X1)
        self.assertEqual(10.5, fill.X2)
        self.assertEqual(-0.5, fill.Y1)
        self.assertEqual(10.5, fill.Y2)

    def test_tracks(self):
        track = next(iter(self.pcb.Footprints[0].Track))
        self.assertEqual(3.937, track.Width)
        self.assertEqual(-73, track.X1)
        self.assertEqual(21, track.X2)
        self.assertEqual(-28, track.Y1)
        self.assertEqual(66, track.Y2)

    def test_layers(self):
        self.layers = {}

        for key in self.pcb.Properties:
            if key.find('LAYERID') >= 0:
                id = int(self.pcb.Properties[key])
                name = self.pcb.Properties[key[:-7] + "NAME"]

                if id not in self.layers:
                    self.layers[id] = name

                self.assertEqual(name, self.layers[id])

        names = []
        for key in self.layers:
            self.assertEqual(0, names.count(self.layers[key]))
            names.append(self.layers[key])

        # pprint(self.layers)

        self.assertEqual('Top Layer', self.layers[16777217])
        self.assertEqual('Multi-Layer', self.layers[16973839])
        self.assertEqual('Mechanical 13', self.layers[16908301])

    def test_body3d(self):
        body3d = self.pcb.Footprints[0].Body3D
        self.assertEqual(1, len(body3d))
        body3d = next(iter(body3d))
        self.assertEqual('MECHANICAL17', body3d.layer_name)

