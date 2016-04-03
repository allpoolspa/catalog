import json
from sets import Set

def printcats():
    # Prints categories so that we can update the aps_categories file.
    opdir = '../optimus'
    shopdir = '../shopify/shopify_json'
    thefile = 'aladdin_shopify.json'
    with open('{0}/{1}'.format(shopdir,thefile), 'Ur') as inf:
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
        print '*' + cat

def clean_cost(cost):
    try:
        return float(cost.replace('$','').replace(',',''))
    except:
        return cost


def make_price(cost, multiplier=None):
    if not cost: return;
    if not multiplier:
        multiplier = .5
    try:
        cost = float(cost.replace('$','').replace(',',''))
    except:
        pass
    try:
        fprice = (cost + (cost * multiplier) + 2.00)
        price = round(fprice, 2)
        return price
    except:
        pass
        #need a log here print("Didn't make price: {}".format(cost))
    return None

def make_sku(manufacturer, part_number):
    cmanufacturer = manufacturer.replace(
        '.',''
    ).replace(
        '-', ''
    ).replace(
        ' ', ''
    ).replace(
        '&', ''
    )
    return cmanufacturer[:3].upper() + "_" + part_number

def shopify_handle(manufacturer, oem):
    return "{0} {1}".format(manufacturer, oem)

def get_manufacturer(manufacturer):
    manufacturers = {
        'Oreq':'Oreq' ,
        'Aquachek': 'Aquachek',
        'GAME': 'GAME',
        'Unicel': 'Unicel',
        'Val-Pak': 'Val-Pak',
        'US SEAL':'US SEAL' ,
        'Aladdin': 'Aladdin',
        'Waterway': 'Waterway',
        'Zodiac': 'Zodiac',
        'Pentair': 'Pentair',
        'Hayward': 'Hayward',
        'S.R. Smith':'S.R. Smith' ,
        'A.O. Smith': 'A.O. Smith',
        'Afras Industries': 'Afras Industries',
        'Oreq': 'Oreq',
        'Odyssey': 'Odyssey',
        'Raypak':'Raypak' ,
        'Polaris': 'Zodiac',
        'Jandy': 'Zodiac',
        'A&B Brush': 'A&B Brush',
        'Pac-Fab': 'Pac-Fab',
        'Purex':'Purex',
        'American Products': 'Pentair',
        'Anthony': 'Pentair',
        'HACH': 'HACH',
        'Caretaker': 'Zodiac',
        'Regal': 'A.O. Smith',
        "Great American": "GAME",
    }
    try:
        manufacturer = manufacturer.encode('ascii')
    except:
        print("Manufacturer {} failed to convert".format(manufacturer))
        return manufacturer
    for m, n in manufacturers.items():
        remove = ['.', '-', ' ', '&']
        m = str(m.encode('ascii'))
        clean_m = m.translate(
            None, ''.join(remove)
        ).lower()
        clean_manufacturer = manufacturer.translate(
            None, ''.join(remove)
        ).lower()
        if clean_m in clean_manufacturer:
            return n
    return manufacturer

def list_manufacturers(file):
    import json
    print file
    with open(file, 'Ur') as f:
        products = json.load(f)
        mans = set(products[k]['manufacturer'] for k in products)
        print mans


def get_image_url(sku):
    path = 'https://s3-us-west-1.amazonaws.com/oppics/full/'
    folder = sku.split('_')[0]
    url = '{0}{1}/{2}.jpg'.format(path, folder, sku)
    return url
