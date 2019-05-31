import pyodbc, os

def show_odbc_sources():
    sources = pyodbc.dataSources()
    dsns = sources.keys()
    # dsns.sort()
    sl = []
    for dsn in dsns:
        sl.append('%s [%s]' % (dsn, sources[dsn]))
    print('\n'.join(sl))


Drivers = ['{Microsoft Access Driver (*.mdb)}',
           '{Microsoft Access Driver (*.mdb, *.accdb)}']
file = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, '7Sigma.mdb')
PWD = 'pw'


for drv in Drivers:
    try:
        db = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(drv, file, PWD))
    except:
        db = None
    else:
        break

if db is None:
    print("Failed to connect to access.")
    print("Debug info: ")
    show_odbc_sources()
    exit(1)
