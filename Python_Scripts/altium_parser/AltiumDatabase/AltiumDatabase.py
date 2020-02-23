import sys, os, csv, re
from glob import glob


class Part:
    def __init__(self, row):
        self.row = row

        self.part_number = row['Part Number']
        self.schlib = row['Library Ref']
        self.pcblib = row['Footprint Ref']
        self.datasheet = row['HelpURL']

        self.supplier_part_number = 5*[None]
        self.supplier_part_number[0] = row['Supplier Part Number 1']
        self.supplier_part_number[1] = row['Supplier Part Number 2']
        self.supplier_part_number[2] = row['Supplier Part Number 3']
        self.supplier_part_number[3] = row['Supplier Part Number 4']
        self.supplier_part_number[4] = row['Supplier Part Number 5']

        self.help_url = row['HelpURL']

        self.manufacturer = row['Manufacturer']
        self.manufacturer_part_number = row['Manufacturer Part Number']


class AltiumDatabase:
    def __init__(self):
        files = glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  os.pardir, os.pardir, os.pardir, '_export', '[a-zA-Z]*.csv'))

        self.database = set()
        self.files = {}

        for file in files:
            with open(file, 'r') as csvfile:
                filename = os.path.splitext(os.path.basename(file))[0]
                reader = csv.DictReader(csvfile)
                self.files[filename] = []
                for row in reader:
                    self.files[filename].append(row)
                    self.database.add(Part(row))
