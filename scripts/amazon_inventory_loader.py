# Takes a manufacturer's inventory and
# makes an amazon inventory upload sheet.
import csv
import itertools
import json
from math import ceil
from copy import deepcopy
from amazon_variables import CATEGORY_INVENTORY_FILE as amazon_dict
from scripts import make_price, get_manufacturer, make_sku, get_image_url


class amazonProductLoader:


    def __init__(self, infile, outfile):
        self._manufacturer_file = infile
        self._amazon_file = outfile
        self._product_list = []
        self._offering_condition = 'New'
        self._quantity = 0
        self._leadtime = 30
        self._fulfillment_latency = 30
        self._isfba = False
        self._product_type = 'OutdoorLiving'
        self._status = 'Update'
        self._product_id_type = 'UPC'
        self._weight_uom = "LB"
        self._measurement_uom = "IN"

    def readcsv(self):
        with open(self._manufacturer_file, 'Ur') as inputfile:
            products = csv.DictReader(inputfile)
            product_list = self._product_list
            for product in products:
                amz_dict = self.translate(product)
                product_list.append(amz_dict)

    def readjson(self):
        with open(self._manufacturer_file, 'Ur') as inputfile:
            products = json.load(inputfile)
            for k, product in products.items():
                amz_dict = self.prune(self.translate(product))
                self._product_list.append(amz_dict)

    def write_amazon_file(self):
        with open(self._amazon_file, 'w') as outputfile:
            output_wrtr = csv.DictWriter(
                outputfile,
                fieldnames=amazon_dict
            )
            output_wrtr.writeheader()
            for product in self._product_list:
                output_wrtr.writerow(product)

    def prune(self, adict):
        new_dict = { key:adict.get(key) for key in amazon_dict.keys()}
        return new_dict



    def translate(self, product):
        for k,v in product.items():
            product[k] = str(v)
        print product
        amazonproduct = {}
        manufacturer = get_manufacturer(product.get('manufacturer'))
        part_number = product.get('part_number')
        sku = product.get('sku', make_sku(manufacturer, part_number))
        upc = product.get('upc')
        if not upc:
            return {}
        title = product.get('title')
        try:
            price = make_price(product.get('price'))
        except:
            return {}
        image_url = get_image_url(sku)
        amazonproduct['standard_price'] = price
        amazonproduct['item_sku'] = sku
        amazonproduct['sku'] = sku
        amazonproduct['part_number'] = part_number
        amazonproduct['external_product_id'] = upc
        amazonproduct['external_product_id_type'] = self._product_id_type
        amazonproduct['product_id'] = upc
        amazonproduct['product_id_type'] = self._product_id_type
        amazonproduct['manufacturer'] = manufacturer
        amazonproduct['brand_name'] = manufacturer
        amazonproduct['item_name'] = title
        amazonproduct['model'] = part_number
        # dimensions. If all dimensions, then add unit of measures
        amazonproduct['item_display_weight'] = product.get('weight')
        amazonproduct['item_display_height'] = product.get('height')
        amazonproduct['item_display_width'] = product.get('width')
        amazonproduct['item_display_length'] = product.get('length')
        amazonproduct['item_weight_unit_of_measure'] = self._weight_uom
        amazonproduct['item_height_unit_of_measure'] = self._measurement_uom
        amazonproduct['item_width_unit_of_measure'] = self._measurement_uom
        amazonproduct['item_length_unit_of_measure'] = self._measurement_uom
        amazonproduct['product_description'] = product.get(
            'long_descriptions',
            product.get('title')
        )
        amazonproduct['generic_keywords'] = product.get(
            'tags',
            product.get('category')
        )
        amazonproduct['specific_uses_keywords1'] = product.get('category')
        amazonproduct['specific_uses_keywords2'] = product.get('subcategory')
        amazonproduct['specific_uses_keywords3'] = product.get('short_description')

        amazonproduct['item_package_quantity'] = 1
        amazonproduct['main_image_url'] = image_url
        amazonproduct['warranty_description'] = product.get('warranty')
        amazonproduct['is_discontinued_by_manufacturer'] = self.discontinued(title)
        amazonproduct['condition_type'] = self._offering_condition
        amazonproduct['feed_product_type'] = self._product_type
        amazonproduct['update_delete'] = self._status
        amazonproduct['fulfillment_latency'] = self._fulfillment_latency
        amazonproduct['leadtime-to-ship'] = self._leadtime
        amazonproduct['quantity'] = self._quantity
        self.check_dimensions(amazonproduct)
        return amazonproduct

    def check_dimensions(self, product):
        if not product['item_display_weight']:
            product['item_weight_unit_of_measure'] = ""
        hwl = [
            product['item_display_height'],
            product['item_display_width'],
            product['item_display_length']
        ]

        if not all(hwl):
            product['item_display_height'] = ''
            product['item_display_width'] = ''
            product['item_display_length'] = ''


    def discontinued(self, title):
        return 'discontinued' in title.lower()


    def make_copy_amz_title_dict(self):
        return deepcopy(amazon_dict)

    def filter_foreign_products(self, sku):
        for product in self._product_list:
            if '-EU' in product['sku'] or  '-AU' in product['sku']:
                product['quantity'] = 0


if __name__ == '__main__':
    #from commands import makeparser
    #args = makeparser()
    names = [
        'pentair',
        'aladdin',
        'srsmith',
        'aosmith',
    ]
    for name in names:
        infile = '../shopify/shopify_json/{}_shopify.json'.format(name)
        outfile = '../amazon/{}_amazon.csv'.format(name)
        amzloader = amazonProductLoader(infile, outfile)
        amzloader.readjson()
        #amzloader.filter_foreign_products()
        amzloader.write_amazon_file()



