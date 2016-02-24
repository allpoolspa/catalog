import math
import json
import csv, codecs, cStringIO
import re
from copy import deepcopy
from shopify_variables import (SHOPIFY_TEMPLATE, SHOPIFY_HEADERS)
from aps_categories import COLLECTIONS, MENUS, _CATEGORIES, TYPES_N_TAGS as TNT
from categories import _CATEGORIES

misc_counter = 0
counter = 0
multiplier = .6
infile = 'hayward_shopify.json'
op_infile = '../optimus/optimus_hay01.json'
outfile = 'merged_hayward_shopify.csv'

def shopify_converter(infile, outfile):
    with open('../shopify/shopify_json/{}'.format(infile), 'Ur') as f:
        data = json.load(f)
        manufacturer_products = {
            shopify_translate(value)['Variant SKU'] : shopify_translate(value)
            for key,value in data.items()
        }
    if op_infile:
        op_products = optimus_products()
    products = merger(manufacturer_products, op_products)
    with open("../shopify/{}".format(outfile), "w") as output:
        writer = csv.DictWriter(output, fieldnames=SHOPIFY_HEADERS)
        writer.writeheader()
        for k,product in products.items():
            writer.writerow({k:unicode(v).encode("utf-8") for k,v in product.items()})

def merger(mproducts, opproducts):
    for k, v in opproducts.items():
        opp = opproducts[k]
        try:
            mp = mproducts[k]
            for key in opp.keys():
                if key == 'Tags':
                    mp[key] += "," + opp[key]
                    mptags = mp[key].split(',')
                    opptags = opp[key].split(',')
                    for mptag in mptags:
                        strmptag = str(mptag)
                        if not strmptag in opptags:
                            opptags.append(strmptag)
                    mp[key] = ','.join(opptags)
                    if mp[key][0] == ',':
                        mp[key] = mp[key][1:]
                        continue
                    continue
                elif key == "Handle" and mp[key]:
                    continue
                elif key == 'Variant Barcode':
                    continue
                elif key == 'Variant Price' and mp[key]:
                    continue
                mp[key] = opp[key]
        except:
            mproducts[k] = opproducts[k]
    return mproducts


def optimus_products():
    op_products = {}
    with open('{}'.format(op_infile), 'Ur') as f:
        data = json.load(f)
        for datum in data:
            for part in datum['parts']:
                oem = part['oem']
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
                category, tags = type_n_tags(category, title)
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
                product['Tags'] = tags + ',' + manufacturer.lower()
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
                    pass
                op_products[product['Variant SKU']] = product
    return op_products

def get_manufacturer(manufacturer):
    ms = [
        'Oreq', 'Aquachek', 'GAME', 'Unicel', 'Val-Pak', 'U.S. SEAL',
        'Aladddin', 'Waterway', 'Zodiac', 'Pentair', 'Hayward'
    ]
    for m in ms:
        if m in manufacturer:
            return m
    return manufacturer

def type_n_tags(key, title=None):
    key = str(key.replace('| ', '').replace(' -', ','))
    possible_categories = _CATEGORIES[key]
    cats = possible_categories.split(',')
    for cat in cats:
        cat = cat.lstrip()
        try:
            tags = TNT[cat]
            tags = gettags(key, possible_categories, tags, title)
            return cat, tags
        except:
            pass
    print("No type or tags for: {}".format(key))
    return None, None

def gettags(key, categories, tags, title=None):
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

def shopify_translate(line):
    """ This simply translates a product from the SCP template to
    the Shopify template.
    """
    product = shopify_template()
    # Define and get variables
    manufacturer = line['manufacturer']
    category = line['category']
    # Make sure the upc is just numerical values.
    upc = clean_upc(line['upc'])
    # part_number is either the manufacturers part number or the upc.
    part_number = get_part_number(line)
    sku = create_sku(manufacturer, part_number)
    title = line['title']
    seo_title = manufacturer + " - " + title
    handle = manufacturer + " " + part_number
    description = make_description(
        title,
        line['long_description'],
        {'Instructions': line['instructions'], 'Warranty': line['warranty']}
    )
    # Product defintions
    product['Vendor'] = line['manufacturer']
    product['Title'] = title
    product['Published'] = True
    category, tags = type_n_tags(line['category'], title)
    if not (category and tags):
        alt_category, alt_tags = type_n_tags(line['subcategory'], title)
    if not category and alt_category:
        category = alt_category
    if not tags and alt_tags:
        tags = tags +','+alt_tags
    product['Handle'] = handle
    product['Type'] = category
    product['Tags'] = tags + ',' + manufacturer.lower()
    product['Variant Inventory Policy'] = "deny"
    product['Variant Fulfillment Service'] = "manual"
    # SEO definitions
    product['SEO Description'] = title + " " + description
    product['SEO Title'] = title
    # Variant definitions
    product['Variant SKU'] = sku
    product['Variant Inventory Tracker'] = "shopify"
    product['Variant Inventory Qty'] = 2
    product['Variant Price'] = make_price(line['price'])
    product['Variant Requires Shipping'] = True
    product['Variant Barcode'] = upc
    # Image definitions - Image Src is required if Alt is given
    #product['Image Src'] = make_image_location(sku)
    #product['Image Alt Text'] = sku
    # Google Shopping
    # product['Google Shopping / Age Group'] = "Adult"
    # product['Google Shopping / Gender'] = "Unisex"
    # product['Google Shopping / Condition'] = "new"
    # Optional fields
    try:
        product['Option1 Name'] = line['option_one_name']
        product['Option1 Value'] = line['option_one_value']
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

def shopify_template():
    return deepcopy(SHOPIFY_TEMPLATE)



def get_part_number(line):
    try:
        #val-pak specific: they have two part numbers for some products
        # one is the actual part number
        # and the other has an S to specify a single uom for ordering.
        part_number = clean_part_number(line['part_number'])
    except:
        print("Part Number wasn't found. Using upc instead")
        part_number = clean_upc(line['upc'])
    return part_number

def make_description(title, description, otherinfo=None):
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
                full_description += k + "\n"
                full_description += v
            except:
                continue
    return full_description


def make_image_location(name):
    return 'https://s3-us-west-1.amazonaws.com/shopifyimportimages/' \
        + name + ".jpg"

def make_price(cost):
    cost = float(cost.replace('$','').replace(',',''))
    if cost:
        global multiplier
        return round((cost + (cost * multiplier)), 2)
    return cost

def create_sku(manufacturer, part_number):
    return manufacturer[:3].upper() + "_" + part_number

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
    shopify_converter(infile, outfile)
