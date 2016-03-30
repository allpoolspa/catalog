import math
import json
import csv, codecs, cStringIO
import re
from copy import deepcopy
from scripts import make_price, get_manufacturer
from shopify_variables import (SHOPIFY_TEMPLATE, SHOPIFY_HEADERS)
from aps_categories import COLLECTIONS, MENUS, _CATEGORIES, TYPES_N_TAGS as TNT

misc_counter = 0
counter = 0
multiplier = .5
filename = 'srsmith'
infile = '../shopify/shopify_json/{}_shopify.json'.format(filename)
op_infile = '../optimus/{}_optimus.json'.format(filename)
outfile = '../shopify/shopify_ready_csv/merged_{}2_shopify.csv'.format(filename)
notfound = []

def shopify_translater(infile, outfile):
    global notfound
    with open('{}'.format(infile), 'Ur') as f:
        data = json.load(f)
        manufacturer_products = {
            shopify_translate(value)['Variant SKU'] : shopify_translate(value)
            for key,value in data.items()
        }
    if op_infile:
        op_products = optimus_translate()
    else:
        op_products = {}
    products = merger(manufacturer_products, op_products)
    with open("{}".format(outfile), "w") as output:
        writer = csv.DictWriter(output, fieldnames=SHOPIFY_HEADERS)
        writer.writeheader()
        for k,product in products.items():
            writer.writerow({k:unicode(v).encode("utf-8") for k,v in product.items()})
    for i in notfound:
        print '"'+i+'":"",'

def merger(mproducts, opproducts):
    noimages = 0
    for k, v in opproducts.items():
        opp = opproducts[k]
        try:
            mp = mproducts[k]
            for key in opp.keys():
                if key == 'Tags':
                    mp[key] += "," + opp[key]
                    mp[key] = _clean_tags(mp[key])
                    continue
                elif key == "Handle" and mp[key]:
                    continue
                elif key == 'Variant Barcode':
                    continue
                elif key == 'Variant Price':
                    continue
                elif key == 'Image Src':
                    notempty = [opp[key] is not "", opp[key]]
                    if 'no-image' in mp['Tags'] and all(notempty):
                        opp['Tags'] = opp['Tags'].replace(',no-image', '')
                        mp['Tags'] = mp['Tags'].replace(',no-image', '')
                        mp['Tags'] += ',has-image'
                        opp['Tags'] += ',has-image'
                        mp['Tags'] = _clean_tags(mp['Tags'])
                mp[key] = opp[key]
        except:
            mproducts[k] = opproducts[k]
            img = mproducts[k]['Image Src']
            if img == "" or not img:
                noimages += 1
                mproducts[k]['Tags'] += ",no-image"
            else:
                mproducts[k]['Tags'] += ",has-image"
    print noimages
    return mproducts

def optimus_translate():
    op_products = {}
    with open('{}'.format(op_infile), 'Ur') as f:
        data = json.load(f)
        for datum in data:
            for part in datum['parts']:
                oem = part.get('oem')
                part_number = part.get('part_number')
                if not oem:
                    #print('No part number for: {}'.format(part))
                    continue
                product = shopify_template()
                sku = part['sku']
                title = part['title']
                if not title:
                    title = oem + " - For - " + datum['title']
                category = datum['category']
                main_title = str(datum['title'])
                category, tags = _type_n_tags(category, title)
                manufacturer = get_manufacturer(part['manufacturer'])
                description = part.get('description', oem)
                handle = manufacturer + " " + oem
                product['Vendor'] = manufacturer
                try:
                    product['Title'] = title + " - " + oem
                except:
                    print part
                product['Published'] = True
                product['Handle'] = handle
                product['Type'] = category
                tags += ',{},part'.format(manufacturer.lower())

                if oem:
                    product['Option1 Name'] = "Part Number"
                    product['Option1 Value'] = oem
                #product['Option2 Name'] = "Fits Model"
                #product['Option2 Value'] = datum['title']
                # SEO definitions
                product['SEO Description'] = title + " - " + description
                product['SEO Title'] = title
                # Variant definitions
                product['Variant SKU'] = sku
                product['Variant Price'] = 0
                product['Variant Inventory Policy'] = "deny"
                product['Variant Fulfillment Service'] = "manual"
                product['Variant Inventory Tracker'] = "shopify"
                product['Variant Inventory Qty'] = 0
                product['Variant Requires Shipping'] = True
                try:
                    product['Image Src'] = part['image_urls'][0]
                    product['Image Alt Text'] = sku
                except:
                    product['Tags'] += ',no-image'
                product['Tags'] = _clean_tags(tags)
                op_products[product['Variant SKU']] = product
    return op_products


def shopify_translate(line):
    """ This simply translates a product from the SCP template to
    the Shopify template.
    """
    product = shopify_template()
    # Define and get variables
    manufacturer = get_manufacturer(line.get('manufacturer'))
    category = str(line.get('category'))
    # Make sure the upc is just numerical values.
    upc = clean_upc(str(line.get('upc')))
    # part_number is either the manufacturers part number or the upc.
    part_number = str(line.get('part_number')) #get_part_number(line)
    sku = create_sku(manufacturer, part_number)
    title = str(line.get('title'))
    seo_title = manufacturer + " - " + title
    handle = manufacturer + " " + part_number
    description = make_description(
        title,
        line.get('long_description')
    )
    # Product defintions
    product['Vendor'] = manufacturer
    if part_number not in title:
        product['Title'] = title + ' - ' + part_number
    else:
        product['Title'] = title
    product['Published'] = True
    category, tags = _type_n_tags(category, title)
    if not (category and tags):
        alt_category, alt_tags = _type_n_tags(line.get('subcategory'), title)
    if not category and alt_category:
        category = alt_category
    if not tags and alt_tags:
        tags = tags +','+alt_tags
    product['Handle'] = handle
    product['Type'] = category
    tags +=  ",{0},no-image,".format(manufacturer.lower())
    product['Tags'] = _clean_tags(tags)
    product['Variant Inventory Policy'] = "deny"
    product['Variant Fulfillment Service'] = "manual"
    # SEO definitions
    print(description, title)
    product['SEO Description'] = description
    product['SEO Title'] = product['Title']
    # Variant definitions
    product['Variant SKU'] = sku
    product['Variant Inventory Tracker'] = "shopify"
    product['Variant Price'] = make_price(line['price'])
    if product['Variant Price']:
        product['Variant Inventory Qty'] = 5
    else:
        product['Variant Inventory Qty'] = 0
    product['Variant Requires Shipping'] = True
    product['Variant Barcode'] = upc
    # Image definitions - Image Src is required if Alt is given
    #product['Image Src'] = make_image_location('valpakpics', sku)
    #product['Image Alt Text'] = sku
    # Google Shopping
    # product['Google Shopping / Age Group'] = "Adult"
    # product['Google Shopping / Gender'] = "Unisex"
    # product['Google Shopping / Condition'] = "new"
    # Optional fields
    try:
        product['Option1 Name'] = "Part Number"
        product['Option1 Value'] = part_number
    except:
        product['Option1 Name'] = "Title"
        product['Option1 Value'] = "Default Title"
    try:
        product['Option2 Name'] = line['option_two_name']
        product['Option2 Value'] = line['option_two_value']
    except:
        # no option two (optional)
        pass
    return product

def _clean_tags(tags):
    equipment = [
        'equipment' in tags,
        'wholegood' in tags,
        'unit' in tags
    ]
    if 'part' in tags and any(equipment):
        tags = tags.replace('part', '')
    taglist = tags.split(',')
    cleanlist = []
    for tag in taglist:
        strtag = str(tag).lower()
        if strtag and not(strtag in cleanlist):
            cleanlist.append(strtag)
    cleanstr = ','.join(cleanlist)
    return cleanstr

def _type_n_tags(key, title=None):
    global notfound
    try:
        key = str(key.replace('| ', '').replace(' -', ','))
        possible_categories = _CATEGORIES.get(key)

        cats = possible_categories.split(',')
        for cat in cats:
            cat = cat.lstrip()
            try:
                tags = TNT.get(cat)
                tags = _gettags(key, possible_categories, tags, title)
                return cat, tags
            except:
                pass
    except:
        pass
    if key:
        if key not in notfound:
            notfound.append(key)
        print("No type or tags for: {}".format(key))
    return "Accessories", "part,no-cat,"

def _bestguess_type(title):
    keywords = {
        "Pumps": ["Pump", "HP", "Pump", "Trap", 'Lid'],
        "O-Rings & Gaskets": [
            'oring', 'O-Ring', 'Oring',
            'O-ring', 'Oring', 'ORing',
            'gasket', 'Gasket'
        ]
    }
    type_score = {}
    for k, values in keywords.items():
        type_score[k] = 0
        for value in values:
            if value in title:
                if k == "Pumps":
                    type_score[k] += 5
                else:
                    type_score[k] += 10
    bestguess_type = max(type_score, key=type_score.get)
    if type_score[bestguess_type] == 0:
        return None
    return bestguess_type




def _gettags(key, categories, tags, title=None):
    product_tags = ""
    lkey = key.lower()
    lcategories = categories.lower()
    ltitle = title.lower()
    for tag in tags:
        if isinstance(tag, str):
            ltag = tag.lower()
            if ltag in lkey:
                product_tags += "," + ltag
            if ltag in lcategories:
                product_tags += "," + ltag
            if ltag in ltitle:
                product_tags += "," + ltag
        else:
            for atag in tag:
                ltag = atag.lower()
                if ltag in lkey:
                    product_tags += "," + ltag
                if ltag in lcategories:
                    product_tags += "," + ltag
                if ltag in ltitle:
                    product_tags += "," + ltag

    return product_tags if product_tags else key


def shopify_template():
    return deepcopy(SHOPIFY_TEMPLATE)

def get_part_number(part):
    try:
        #val-pak specific: they have two part numbers for some products
        # one is the actual part number
        # and the other has an S to specify a single uom for ordering.
        part_number = clean_part_number(part['part_number'])
    except:
        print("Part Number wasn't found. Using upc instead")
        part_number = clean_upc(part['upc'])
    return part_number

def make_description(title, description, otherinfo=None):
    description = str(description)
    if title and description:
        full_description = title + ".\n"  + description
    elif title:
        # everything should have a title
        full_description = title
    else:
        return

    if otherinfo:
        for k,v in otherinfo.items():
            try:
                full_description += "\n"
                full_description += str(k) + "\n"
                full_description += str(v)
            except:
                continue
    return full_description


def make_image_location(bucket, name):
    return 'https://s3-us-west-1.amazonaws.com/{0}/{1}.jpg'.format(
        bucket, name
    )

def make_price1(cost):
    try:
        cost = float(cost.replace('$','').replace(',',''))
        global multiplier
        cost = round((cost + (cost * multiplier) + 1.00), 2)
    except:
        print("Didn't make price")
        pass
    return cost

def create_sku(manufacturer, part_number):
    cmanufacturer = manufacturer.replace(
        '.',''
    ).replace(
        '-', ''
    ).replace(
        ' ', ''
    )
    return cmanufacturer[:3].upper() + "_" + part_number

def clean_part_number(part_number):
    """ This is used to clean part numbers."""
    clean_part_number = part_number
    if ',' in part_number:
        value0, value1 = part_number.replace(" ", "").split(',')
        if not value0.endswith('S'):
            clean_part_number = value0
        else:
            clean_part_number = value1
    return clean_part_number

def clean_upc(upc):
    if upc:
        return re.sub("[^0-9]", "", upc)
    return upc


def count():
    global counter
    counter = counter + 1



if __name__ == "__main__":
    shopify_translater(infile, outfile)
