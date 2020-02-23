import webbrowser
from AltiumDatabase.AltiumDatabase import AltiumDatabase
import pyperclip
import msvcrt

_altium_database_class = AltiumDatabase()
database = _altium_database_class.database

part_number = None
clipboard = pyperclip.paste()

for i in database:
    if i.part_number == clipboard:
        part_number = clipboard

if not part_number:
    print("Part number: ", end='')
    part_number = input()

result = []
for i in database:
    if i.part_number == part_number:
        result.append(i)

if len(result) == 0:
    print("Part number not found in database.")
    print("Press enter to search for it, any other key to cancel.")
    ch = msvcrt.getch()
    if ch not in {b'\r', b'\n'}:
        exit()
    
    manufacturer_part_number = part_number
    supplier_part_numbers = [None] * 5
else:
    supplier_part_numbers = result[0].supplier_part_number
    manufacturer_part_number = result[0].manufacturer_part_number
    pyperclip.copy(manufacturer_part_number)
    for x in supplier_part_numbers:
        print(x)

# TME
url = 'https://www.tme.eu/pl/katalog/#search=' + (supplier_part_numbers[0] or manufacturer_part_number)
webbrowser.open_new_tab(url)

# RSComponents
url = 'https://pl.rs-online.com/web/c?searchTerm=' + (supplier_part_numbers[1] or manufacturer_part_number)
webbrowser.open_new_tab(url)

# Farnell
url = 'https://pl.farnell.com/search?st=' + (supplier_part_numbers[2] or manufacturer_part_number)
webbrowser.open_new_tab(url)

# Mouser
url = 'https://eu.mouser.com/Search/Refine.aspx?Keyword=' + (supplier_part_numbers[3] or manufacturer_part_number)
webbrowser.open_new_tab(url)

# Digi-Key
url = 'https://www.digikey.com/products/en?keywords=' + (supplier_part_numbers[4] or manufacturer_part_number)
webbrowser.open_new_tab(url)

# octopart
url = "https://octopart.com/search?q=sdfxd"
