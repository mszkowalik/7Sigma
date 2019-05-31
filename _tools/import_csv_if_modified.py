import os
from glob import glob

mdb_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'SVNDatabase_A1.mdb')

csv_files = glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir,
                          '_export', '[a-zA-Z]*.csv'))
                          

last_mdb_modification = os.path.getmtime(mdb_file)
last_csv_modification = max([os.path.getmtime(i) for i in csv_files])

if last_csv_modification > last_mdb_modification:
    import import_csv
