#!/usr/bin/env python
import sys
import os

from pprint import pprint

from PcbLib.PcbLib import PcbLib
from SchLib.SchLib import SchLib
from deepdiff import DeepDiff


# Subversion provides the paths we need as the last two parameters.
# file  = sys.argv[-3]
LEFT  = sys.argv[-2]
RIGHT = sys.argv[-1]



def diff_schlib(old, new):
    old = SchLib(old)
    new = SchLib(new)
    pprint(DeepDiff(old, new, verbose_level=0, exclude_paths={"root._ole", "root.filename"}))


def diff_pcblib(old, new):
    old = PcbLib(old)
    new = PcbLib(new)
    pprint(DeepDiff(old, new, verbose_level=0, exclude_paths={"root.OleFile", "root.filename", 'root.Properties'}))

if LEFT.lower().find(".schlib") > 0:
    diff_schlib(LEFT, RIGHT)
elif LEFT.lower().find(".pcblib") > 0:
    diff_pcblib(LEFT, RIGHT)
else:
    cmd = ['diff', LEFT, RIGHT]
    os.system(' '.join(cmd))
