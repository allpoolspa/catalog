# Prints categories so that we can update the aps_categories file.

import json
from sets import Set

with open('../optimus/optimus_hay01.json', 'Ur') as inf:
    data = json.load(inf)
    cats = Set()
    subcats = Set()
    for datum in data:
        #cats.add(str(datum.get('category'))) # for optimus
        cats.add(str(data[datum].get('category'))) # scp
        subcats.add(str(data[datum].get('subcategory'))) # scp
for cat in cats:
    print '*' + cat
print
for cat in subcats:
    lcat = cat.lower()
    ncat = lcat[0].upper() + lcat[1:]
    print '*' + cat
