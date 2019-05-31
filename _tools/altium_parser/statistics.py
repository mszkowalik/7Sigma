import os, csv

import parse

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, '_tools', 'stats.csv')
with open(file, 'w') as csvfile:
    fieldnames = ['Schematic elements', 'Footprint elements', 'Database elements',
                  'Schematics unused', 'Footprints unused', 'Schematic errors', 'Footprint errors']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    sch_names = parse.schematics.keys()
    pcb_names = parse.footprints.keys()
    database_sch_names = {i.schlib for i in parse.database}
    database_pcb_names = {i.pcblib for i in parse.database}

    writer.writeheader()
    writer.writerow({'Schematic elements': len(sch_names),
                     'Footprint elements': len(pcb_names),
                     'Database elements': len(parse.database),
                     'Schematics unused': len(sch_names-database_sch_names),
                     'Footprints unused': len(pcb_names-database_pcb_names),
                     'Schematic errors': len(database_sch_names-sch_names),
                     'Footprint errors': len(database_pcb_names-pcb_names)})
