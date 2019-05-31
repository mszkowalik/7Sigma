import csv, pyodbc, os
from glob import glob
import pyodbc_connect

con = pyodbc_connect.db

print("Import!")

files = glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir,
                          '_export', '[_a-zA-Z]*.csv'))
for file in files:
    with open(file, 'r') as csvfile:
        filename = os.path.splitext(os.path.basename(file))[0]
        print(filename)

        cursor = con.cursor()
        create_query = 'DELETE FROM \"' + filename + '\"'
        cursor.execute(create_query)
        
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        columns = next(reader)
        
        columns = ['[' + i + ']' for i in columns]
        query = 'insert into \"' + filename + '\"({0}) values ({1})'
        query = query.format(', '.join(columns), ','.join('?' * len(columns)))

        
        for data in reader:
            #print(data)
            #print(query)
            #print()
            cursor.execute(query, data)

        cursor.commit()
        cursor.close()
