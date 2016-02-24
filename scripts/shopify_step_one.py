# Makes a json file from a csv.
# Also, we can merge a json and csv file into a new json file.
# This is not the prettiest script but it gets the job done.
# Be aware that this expects and accepts certain keys.
# You may have to change the title of the keys in your file
# before using this script.
# TODO: list except and accept keys.

# MAKES JSON FILES THAT CAN RUN THROUGH THE shopify_converter.py
import json
import csv


p = {}
unsure = {}
files = ['db_files/hayward.json'] #add a .json catalog file here
fcsv = '' #add a .csv catalog file here
outf = 'hayward_shopify.json' #add an output file here

for afile in files:
    if afile and afile.endswith('.json'):
        with open('../'+ afile, 'Ur') as ifile:
            products = json.load(ifile, encoding="cp1252")
            counter = 0
            for product in products:
                if isinstance(products, list):
                    item = product
                else:
                    item = products[product]
                fprice = item['price']
                if 'dimensions' in item and item['dimensions']:
                    h, l, w = item['dimensions'].split('x')
                elif 'dimensions' in item and not item['dimensions']:
                    h,l,w = None, None, None
                else:
                    h = item.get('height')
                    l = item.get('length')
                    w = item.get('width')
                weight = item.get('ship_weight', item.get('weight'))
                category = item.get('product_line')
                subcategory = item.get('department')
                category = item.get('product_line')
                upc = item.get('upc')
                if item['part_number'] not in p:
                    if fprice:
                        available = True
                    else:
                        available = False
                    p[item['part_number']] = {
                        'part_number' : item['part_number'],
                        'upc' : upc,
                        'manufacturer' : item['manufacturer'],
                        'title' : item['title'],
                        'price' : fprice,
                        'available' : available,
                        'weight' : weight,
                        'height' : h,
                        'width' : w,
                        'length' : l,
                        'type' : None,
                        'category' : category,
                        'subcategory' : subcategory,
                        'short_description' : None,
                        'long_description' : None,
                        'instructions' : None,
                        'warranty' : None,
                    }
    if afile and afile.endswith('.csv'):
        with open(afile, 'Ur') as ifile:
            products = csv.DictReader(ifile)
            counter = 0
            for product in products:
                if 'upc' in product:
                    upc = product['upc']
                else:
                    upc = None
                part_number = product['part_number']
                if 'type' in product:
                    product_type = product['type']
                if 'category' in product:
                    category = product['category']
                else:
                    category = None
                if 'subcategory' in product:
                    subcategory = product['subcategory']
                else:
                    subcategory = None
                if 'short_description' in product:
                    short_description = product['short_description']
                else:
                    short_description = None
                if 'long_description' in product:
                    long_description = product['long_description']
                else:
                    long_description = None
                if 'warranty' in product:
                    warranty = product['warranty']
                else:
                    warranty = None
                if 'instructions' in product:
                    instructions = product['instructions']
                else:
                    instructions = None
                if 'weight' in product:
                    weight = product['weight']
                else:
                    weight = None
                if 'length' in product:
                    length = product['length']
                else:
                    length = None
                if 'height' in product:
                    height = product['height']
                else:
                    height = None
                if 'width' in product:
                    width = product['width']
                else:
                    width = None
                if 'title' in product:
                    title  = product['title']
                else:
                    title = None
                if 'manufacturer' in product:
                    manufacturer = product['manufacturer']
                else:
                    manufacturer = None

                try:
                    if isinstance(product['price'], float):
                        fprice = fprice = product['price']
                    else:
                        price = product['price'].replace(',', '').replace('$', '')
                        fprice = float(price)
                except:
                    #print('Price Unavailable: {0}'.format(part_number))
                    fprice = None


                if part_number in p:
                    ppn = p[part_number]
                    if not ppn['length']:
                        ppn['length'] = length
                    if not ppn['width']:
                        ppn['width'] = width
                    if not ppn['weight']:
                        ppn['weight'] = weight
                    if not ppn['height']:
                        ppn['height'] = height
                    if not ppn['title']:
                        ppn['title'] = title
                    if not ppn['type']:
                        ppn['type'] = product_type
                    if not ppn['category']:
                        ppn['category'] = category
                    if not ppn['subcategory']:
                        ppn['subcategory'] = subcategory
                    if not ppn['instructions']:
                        ppn['instructions'] = instructions
                    if not ppn['warranty']:
                        ppn['warranty'] = warranty
                    if not ppn['short_description']:
                        ppn['short_description'] = short_description
                    if not ppn['long_description']:
                        ppn['long_description'] = long_description
                    if fprice and not ppn['price']:
                        ppn['price'] = fprice
                        ppn['available'] = True
                    else:
                        fprice = ppn['price']
                    if not ppn['upc'] == upc:
                        unsure[upc] = {
                            'upc_scp' : upc,
                            'upc_man' : ppn['upc'],
                            'part_number': part_number,
                            'title': title
                        }
                    ppn['upc'] = upc
                    counter += 1
                else:
                    if fprice:
                        available = True
                    else:
                        #print 'Price Unavailable', fprice
                        available = False
                    p[part_number] = {
                        'part_number' : part_number,
                        'upc' : upc,
                        'manufacturer' : manufacturer,
                        'title' : title,
                        'price' : fprice,
                        'available' : available,
                        'weight' : weight,
                        'height' : height,
                        'width' : width,
                        'length' : length,
                        'type' : product_type,
                        'category' : category,
                        'subcategory' : subcategory,
                        'short_description' : short_description,
                        'long_description' : long_description,
                        'instructions' : instructions,
                        'warranty' : warranty
                    }
                    counter += 1
            print counter


with open('../shopify/shopify_json/'+outf, 'w') as merged:
    json.dump(
        p, merged,
        sort_keys = True, indent = 4, ensure_ascii=True
    )



