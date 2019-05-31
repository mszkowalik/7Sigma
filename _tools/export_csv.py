import csv, pyodbc, os
from glob import glob
import pyodbc_connect

con = pyodbc_connect.db

print("Export!")

cur = con.cursor()
tables = [i[2] for i in cur.tables() if i[3] == 'TABLE']

for table in tables:
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "_export", table + ".csv")

    with open(file, 'w', newline='\r\n') as csvfile:
        filename = os.path.splitext(os.path.basename(file))[0]
        print(filename)

        # get first column name to sort by it
        first_column = [i.column_name for i in cur.columns(table=table)][0]
        
        # run a query and get the results
        SQL = 'SELECT * FROM [' + table + '] order by [' + first_column + '];'
        rows = cur.execute(SQL).fetchall()

        header = [i[0] for i in cur.description]

        print(",".join(['\"' + i + '\"' for i in header]), file=csvfile)

        all_data = []
        for row in rows:
            row2 = list(row)
            
            for i in range(0, len(row2)):
                now = row2[i]
                if type(now) == float:
                    first = '{:.2f}'.format(now)
                    second = '{}'.format(now)
                    row2[i] = max((first, second), key=len)
                    
                elif type(now) == str:
                    if now == '':
                        row2[i] = now
                    else:
                        now = now.replace('\"', '\"\"')
                        row2[i] = '\"{}\"'.format(now)
                elif now == None:
                    row2[i] = ''
                else:
                    print(type(now))
                    exit(1)

            # print(row2)
            print(','.join(row2), file=csvfile)

cur.commit()
cur.close()

os.utime(pyodbc_connect.file)
