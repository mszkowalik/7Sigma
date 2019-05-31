import xml.etree.ElementTree
import argparse
from pprint import pprint

from PcbLib.PcbLib import PcbLib
from SchLib.SchLib import SchLib
from deepdiff import DeepDiff


def diff_summary_working_copy(self, old, rel_path=None):
    """
    Provides a summarized output of a diff between two revisions
    (file, change type, file type)
    """
    full_url_or_path = self._CommonClient__url_or_path
    if rel_path is not None:
        full_url_or_path += '/' + rel_path
    result = self.run_command(
        'diff',
        ['--revision', '{}'.format(old),
         '--summarize', '--xml'],
        do_combine=True)
    root = xml.etree.ElementTree.fromstring(result)
    diff = []
    for element in root.findall('paths/path'):
        diff.append({
            'path': element.text,
            'item': element.attrib['item'],
            'kind': element.attrib['kind']})
    return diff


parser = argparse.ArgumentParser(description='Diff altium lib.')
parser.add_argument('--old', type=int, help='First (old) revision to diff. Default: HEAD-1')

args = parser.parse_args()



url = 'https://svn.embe.tech/altium_lib_db/'


def diff_schlib(old, new):
    old = SchLib(old)
    new = SchLib(new)
    pprint(DeepDiff(old, new, verbose_level=0, exclude_paths={"root._ole", "root.filename"}))


def diff_pcblib(old, new):
    old = PcbLib(old)
    new = PcbLib(new)
    pprint(DeepDiff(old, new, verbose_level=0, exclude_paths={"root.OleFile", "root.filename", 'root.Properties'}))


import svn.local
import difflib
import os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))

repo = svn.local.LocalClient('.')
import svn.remote
repo_remote = svn.remote.RemoteClient(url)

repo.update()

c = repo.info()['entry_revision']

old_revision = c-1
if getattr(args, 'old') is not None:
    old_revision = getattr(args, 'old')


diff_list = diff_summary_working_copy(repo, old_revision)
pprint(diff_list)
print("\n\n")

base = lambda x: os.path.basename(x)

modified = [i['path'].replace('\\', '/') for i in diff_list if i['kind'] == 'file' and i['item'] == 'modified']
modified_base = [base(i) for i in modified]

added = [i['path'].replace('\\', '/') for i in diff_list if i['kind'] == 'file' and i['item'] == 'added']
added_base = [base(i) for i in added]

deleted = [i['path'].replace('\\', '/') for i in diff_list if i['kind'] == 'file' and i['item'] == 'deleted']
deleted_base = [base(i) for i in deleted]


def get_and_diff(old_filename, new_filename):
    ending = old_filename[-7:]

    mapa = {".SchLib": diff_schlib, ".PcbLib": diff_pcblib}

    if ending in mapa:
        tmp = 'tmp' + ending
        diff_function = mapa[ending]

        print(80 * '*')
        print(" Modified {} -----> {} ".format(old_filename, new_filename).center(80, '*'))
        print(80 * '*')

        f = open(tmp, 'wb')
        f.write(repo_remote.cat(old_filename + '@{}'.format(old_revision), old_revision))
        f.close()
        diff_function(tmp, new_filename)
        os.remove(tmp)

        print(80 * '*')
        print("")
        print("")


for full, short in zip(modified, modified_base):
    try:
        get_and_diff(full, full)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        pprint(e)


used = set()
for new_full in added:
    match = difflib.get_close_matches(base(new_full), deleted_base)
    ending = new_full[-7:]
    if len(match) > 0:
        old_full = deleted[deleted_base.index(match[0])]
        used.add(old_full)
        get_and_diff(old_full, new_full)
    else:
        print(80 * '*')
        print(" File {} added! ".format(base(new_full)).center(80, '*'))
        print(80 * '*')
        print("")
        print("")

for i in used:
    deleted.remove(i)

for del_full in deleted:
    print(80 * '*')
    print(" File {} removed! ".format(base(del_full)).center(80, '*'))
    print(80 * '*')
    print("")
    print("")


if os.path.exists('tmp.SchLib'):
    os.remove('tmp.SchLib')
if os.path.exists('tmp.PcbLib'):
    os.remove('tmp.PcbLib')