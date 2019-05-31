import os
import webbrowser

os.environ['OCTOPART_API_KEY'] = '183afa14'
import octopart

import webbrowser
from altium_parser.AltiumDatabase.AltiumDatabase import AltiumDatabase
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

mpn = result[0].manufacturer_part_number
supplier_part_numbers = result[0].supplier_part_number



results = octopart.match([mpn])

assert len(results) == 1
print(results[0].parts)
# assert len(results[0].parts) == 1

offers = results[0].parts[0].offers

print(offers)

names = [
    'TME',
    'RS Components',
    'Farnell',
    'Mouser',
    'Digi-Key'
]
suppliers = [list(filter(lambda x: x.seller == name, offers)) for name in names]

urls = ['https://www.tme.eu/pl/katalog/#search=',
        'https://pl.rs-online.com/web/c?searchTerm=',
        'https://pl.farnell.com/search?st=',
        'https://eu.mouser.com/Search/Refine.aspx?Keyword=',
        'https://www.digikey.com/products/en?keywords=']

all_ok = True
def print_sku(offers, asked, url, name):
    print(name, end=': ')
    print(asked, end=' ')
    skus = [i.sku if i.seller != 'RS Components' else i.sku.replace('-', '') for i in offers ]
    print(skus)
    global all_ok
    if asked.strip():
        if asked not in skus:
            webbrowser.open_new_tab(url + asked)
            all_ok = False
            print("----- FAIL ------")
    else:
        if len(skus) != 0:
            webbrowser.open_new_tab(url + skus[0])
            all_ok = False
            print("----- FAIL ------")
        else:
            webbrowser.open_new_tab(url + mpn)
            print("----- CHECK IF NONE ------")

# fix for RS components
supplier_part_numbers[1] = supplier_part_numbers[1].replace('-', '')

for i in zip(suppliers, supplier_part_numbers, urls, names):
    print_sku(i[0], i[1], i[2], i[3])
    print()

if all_ok:
    print("OK!")
else:
    print("---------------------------------------------")
    print("---------------------------------------------")
    print("--------------   FAIL   ---------------------")
    print("---------------------------------------------")
    print("---------------------------------------------")

order = [3, 4, 2, 1, 0]
order_supp = [supplier_part_numbers[i] for i in order]
order_urls = [urls[i] for i in order]
for i in zip(order_supp, order_urls):
    if i[0]:
        webbrowser.open_new_tab(i[1] + i[0])
        break

webbrowser.open_new_tab(result[0].help_url)