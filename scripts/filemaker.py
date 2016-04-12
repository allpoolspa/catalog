#
import re
import json
import csv
import math
from copy import deepcopy
from amazon_variables import CATEGORY_INVENTORY_FILE, INVENTORY_LOADER
from aps_categories import (_CLEANCATS, TYPES_N_TAGS as TNT)
from scripts import *
from templates import *
from fba_inventory import FBA, ERRORS
from types_n_tags import TypeNTags
from fba_calculator import calculate_fees

class FileMaker(object):


    def __init__(self, files, outfile, template, ext="json", mappers=None):
        self._files = files
        self._outfile = outfile
        self._mappers = mappers
        self._template = template
        self._products = {}
        self._outfile_ext = ext

    def start(self):
        self.import_handler()

    def finish(self):
        self.export()

    def csv(self, infile):
        try:
            with open(infile, 'Ur') as f:
                lines = csv.DictReader(f)
                for line in lines:

                    yield line
        except:
            print(infile)

    def json(self, infile):
        try:
            with open(infile, 'Ur') as f:
                lines = json.load(f, encoding="ascii")
                for line in lines:
                    try:
                        yield lines[line]
                    except:
                        yield line
        except:
            print(infile)


    def export(self):
        if self.outfile_ext == "csv":
            self._csv_writer(ext="csv")
        elif self.outfile_ext == "json":
            self._json_writer()
        elif self.outfile_ext == "txt":
            self._csv_writer(ext="txt", delimiter="\t")
        elif self.outfile_ext == "all":
            self._csv_writer(ext="txt", delimiter="\t")
            self._csv_writer(ext="csv")
            self._json_writer()
        else:
            raise InputError(
                "Only .csv, .txt and .json files are supported at this time"
            )

    def _csv_writer(self, ext="csv", delimiter=","):
        with open("{0}.{1}".format(self.outfile, ext), 'w') as openfile:
            writer = csv.DictWriter(
                openfile,
                delimiter=delimiter,
                fieldnames=self.template.keys()
            )
            writer.writeheader()
            for product in self._products.values():
                writer.writerow(
                    {
                        k:unicode(v).encode("utf-8")
                        for k,v in product.items()
                    }
                )

    def _json_writer(self, ext="json"):
        with open("{0}.{1}".format(self.outfile, ext), 'w') as openfile:
            json.dump(
                self._products,
                openfile,
                sort_keys = True,
                indent = 4,
                ensure_ascii=True
            )

    def import_handler(self):
        for infile in self.files:
            if infile.endswith('csv'):
                return self.csv(infile)
            elif infile.endswith('json'):
                return self.json(infile)

    def current_product(self, product):
        sku = str(product['sku'])
        try:
            return self.products[sku]
        except:
            self.products[sku] = self.template
            return self.products[sku]


    @property
    def products(self):
        return self._products

    @products.setter
    def products(self, value):
        self._products = value

    @property
    def template(self):
        return deepcopy(self._template)

    @template.setter
    def template(self, value):
        self._template = value

    @property
    def mapper(self):
        return self._mapper

    @mapper.setter
    def mapper(self, value):
        self._mapper = value

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, value):
        self._files = value

    @property
    def outfile(self):
        return self._outfile

    @outfile.setter
    def outfile(self, value):
        self._outfile = value

    @property
    def outfile_ext(self):
        return self._outfile_ext

    @outfile_ext.setter
    def outfile_ext(self, value):
        self._outfile_ext = value


class ApsFileMaker(FileMaker):


    scp = "_scp"
    cc = "_cc"
    opt = "_optimus"
    man = "_man"

    def start(self):
        super(ApsFileMaker, self).start()
        self.finalize()

    def common_keys(self, curr_product, product):
        if not curr_product.get('part_number'):
            curr_product['part_number'] = product.get(
                'part_number',
                product.get('oem')
            )
        if not curr_product.get('manufacturer'):
            curr_product['manufacturer'] = product.get(
                'manufacturer',
                product.get('vendor')
            )
        if not curr_product.get('title') and product.get('title'):
            curr_product['title'] = product.get('title')
        if not curr_product.get('category'):
            curr_product['category'] = product.get(
                'category',
                product.get('department')
            )
        if not curr_product.get('description'):
            curr_product['description'] = product.get('description')
        if not curr_product.get('sku') and product.get('sku'):
            curr_product['sku'] = product.get('sku')
        if not curr_product.get('oem') and product.get('oem'):
            curr_product['oem'] = product.get('oem')
        if not curr_product.get('list_price') and product.get('list_price'):
            curr_product['list_price'] = self.cost(product.get('list_price'))
        if not curr_product.get('cost'):
            curr_product['cost'] = self.cost(
                product.get('price', product.get('cost'))
            )
        if not curr_product.get('upc'):
            curr_product['upc'] = product.get('upc')
        if product.get('dimensions'):
            l,w,h = self.get_dimensions(product.get('dimensions'))
            curr_product['length'] = l
            curr_product['width'] = w
            curr_product['height'] = h

    def scp_import(self, product):
        """Import products from scp."""
        if not self.sku(product): return;
        curr_product = self.current_product(product)

        self.common_keys(curr_product, product)
        price = self.cost(product.get('price'))
        curr_product['upc'] = product.get('upc')
        curr_product['available'] = product.get('availability')
        curr_product['obsolete'] = product.get('obsolete')
        curr_product['weight'] = product.get('weight')
        curr_product['uom'] = product.get('uom')
        acost = deepcopy(COSTS)
        acost['name'] = "scp"
        acost['cost'] = price
        curr_product['costs'].append(acost)
        asku = deepcopy(SKUS)
        asku['name'] = "scp"
        asku['sku'] = product.get('product_number')
        curr_product['skus'].append(asku)
        acat = deepcopy(CATEGORIES)
        acat['name'] = "scp"
        acat['category'] = product.get('department')
        curr_product['categories'].append(acat)
        acat = deepcopy(CATEGORIES)
        acat['name'] = "scp"
        acat['category'] = product.get('product_line')
        curr_product['categories'].append(acat)
        acat = deepcopy(CATEGORIES)
        acat['name'] = "scp"
        acat['category'] = product.get('category')
        curr_product['categories'].append(acat)

    def cc_import(self, product):
        """Import products from carecraft."""
        if not self.sku(product): return;
        curr_product = self.current_product(product)

        self.common_keys(curr_product, product)
        price = self.cost(product.get('price'))
        acost = deepcopy(COSTS)
        acost['name'] = "carecraft"
        acost['cost'] = price
        curr_product['costs'].append(acost)
        asku = deepcopy(SKUS)
        asku['name'] = "carecraft"
        asku['sku'] = product.get('part_number')
        curr_product['skus'].append(asku)
        curr_product['cost'] = price
        acat = deepcopy(CATEGORIES)
        acat['name'] = "carecraft"
        acat['category'] = product.get('category')
        curr_product['categories'].append(acat)

    def optimus_import(self, wholegood):
        """Import products from optimus."""
        for product in wholegood['parts']:
            original_sku = product.get('sku')
            if not self.sku(product): continue;
            curr_product = self.current_product(product)

            self.common_keys(curr_product, product)
            curr_product['parent'] = product.get('fits_model')
            curr_product['parent_id'] = wholegood.get('modelid')
            if not curr_product['image_url']:
                try:
                    curr_product['image_url'] = self.image_url(
                        product['abbreviation'].split('_')[0],
                        original_sku,
                        manufacturer=product.get('manufacturer')
                    )
                except:
                    curr_product['image_url'] = product.get('image_urls')
            price = self.cost(product.get('price'))
            if price:
                acost = deepcopy(COSTS)
                acost['name'] = "optimus"
                acost['cost'] = price
                curr_product['costs'].append(acost)
            asku = deepcopy(SKUS)
            asku['name'] = "optimus"
            asku['sku'] = product.get('optimus_sku')
            curr_product['skus'].append(asku)
            acat = deepcopy(CATEGORIES)
            acat['name'] = "optimus"
            acat['category'] = wholegood.get('category')
            curr_product['categories'].append(acat)
            acat = deepcopy(CATEGORIES)
            acat['name'] = "optimus"
            acat['category'] = "Part"
            curr_product['categories'].append(acat)
            try:
                images = deepcopy(IMAGES)
                images['description'] = "main"
                images['source'] = "optimus"
                images['url'] = self.image_url(
                    curr_product['sku'].split('_')[0],
                    curr_product['sku'],
                    manufacturer=product.get('manufacturer')
                )
                curr_product['images'].append(images)
            except:
                pass

    def manufacturer_import(self, product):
        """Import products from val-pakproducts.com"""
        if not self.sku(product): return
        curr_product = self.current_product(product)
        self.common_keys(curr_product, product)
        if product.get('category'):
            acat = deepcopy(CATEGORIES)
            acat['name'] = "manufacturer"
            acat['category'] = product.get('category')
            curr_product['categories'].append(acat)
        if product.get('type'):
            acat = deepcopy(CATEGORIES)
            acat['name'] = "manufacturer"
            acat['category'] = product.get('type')
            curr_product['categories'].append(acat)
        curr_product['original_manufacturer'] = product.get('original_manufacturer')
        curr_product['country'] = product.get('country')
        curr_product['manufacturer'] = product.get('manufacturer')
        curr_product['weight'] = product.get('weight')
        curr_product['length'] = product.get('length')
        curr_product['height'] = product.get('height')
        curr_product['width'] = product.get('width')
        curr_product['uom'] = product.get('uom')
        curr_product['oem'] = product.get('oem')
        curr_product['available'] = product.get('available')
        curr_product['discontinued'] = product.get('discontinued')
        try:
            imgs = product.get('image_urls')
            if not imgs: raise KeyError
            curr_product['image_url'] = imgs[0]
            for counter, img in enumerate(imgs):
                images = deepcopy(IMAGES)
                images['description'] = counter
                images['source'] = "manufacturer"
                images['url'] = img
                curr_product['images'].append(images)
        except:
            pass


    def import_handler(self):
        """Takes in a list of files and distributes them out to
        the read_handler() along with the appropriate import()
        """
        for f in self.files:
            if self.scp in f:
                self.read_handler(f, self.scp_import)
            elif self.cc in f:
                self.read_handler(f, self.cc_import)
            elif self.opt in f:
                self.read_handler(f, self.optimus_import)
            elif self.man in f:
                self.read_handler(f, self.manufacturer_import)
            else:
                print(
                    """Please specify the type of file by
                    adding one of the following:
                    \n{0}\n{1}\n{2}\n{3}\n
                    to the file name
                    """.format(self.scp, self.cc, self.opt, self.man)
                )

    def read_handler(self, infile, func):
        """ takes in a file and sends each line (product) to func
        :param infile: a string representation of a file and path
        :param func: a function to be called on each line/product
        """

        if infile.endswith('csv'):
            for product in self.csv(infile):
                func(product)
        elif infile.endswith('json'):
            for product in self.json(infile):
                func(product)
        else:
            print("incompatible file type: {}".format(ifnile))

    def finalize(self):
        for key in self.products.keys():
            # remove all unicode objects
            # and convert everything into strings
            product = self.products[key]

            #self.string_conversion(product)
            product['fulfillment'] = self.fba(product)
            asin = self.asin(product)
            product['asin'] = asin
            product['asins'].append(asin)
            self.type_handler(product)
            self.manufacturer(product)
            self.clean_title(product)
            self.product_handle(product)
            self.filter_foreign_products(product)
            product['obsolete'] = self.obsolete(product)
            product['discontinued'] = self.discontinued(
                product.get('title', False)
            )
            if (
                product['obsolete']
                or product['discontinued']
                or not(product['cost'])
            ):
                product['available'] = False
            else:
                product['quantity'] = 5
            self.get_type_n_tags(product)
            self.fba_fees(product)

    # Helper functions

    def fba_fees(self, product):
        try:
            length = float(product.get('length'))
            height = float(product.get('height'))
            width = float(product.get('width'))
            weight = float(product.get('weight'))
        except:
            return
        try:
            product['fba_fee'] = round(
                float(
                    calculate_fees(length, width, height, weight)
                ),
                2
            )
        except:
            product['fba_fee'] = None
        cost = product.get('cost')


    def get_type_n_tags(self, product):
        tnt = TypeNTags()
        tnt.find(product)
        product['category'] = tnt.thetype
        product['tags'] = tnt.tags



    def filter_foreign_products(self, product):
        if '-EU' in product['sku'] or  '-AU' in product['sku']:
            product['quantity'] = 0
            product['available'] = False

    def asin(self, product):
        sku = product.get('sku')
        part_number = product.get('part_number')
        try:
            clean_pn = part_number.replace('-','')
        except:
            clean_pn = ""
        return FBA.get(
            sku,
            FBA.get(
                part_number,
                FBA.get(clean_pn)
            )
        )

    def fba(self, product):
        sku = product.get('sku')
        part_number = product.get('part_number')
        try:
            clean_pn = part_number.replace('-','')
        except:
            clean_pn = ""
        if FBA.get(sku) or FBA.get(part_number) or FBA.get(clean_pn):
            return "AMAZON_NA"
        else:
            return ""

    def image_url(self, bucket, name, manufacturer=None):

        if "val-pak" in manufacturer.lower():
            return 'https://s3-us-west-1.amazonaws.com/valpakpics/{0}.jpg'.format(
                name
            )
        elif "raypak" in manufacturer.lower():
            part_number = name.split('_')[1]
            img = 'https://s3-us-west-1.amazonaws.com/oppics/full/{0}/{0}_{1}.jpg'.format(
                "Raypak",
                part_number
            )
            return img
        else:
            return 'https://s3-us-west-1.amazonaws.com/oppics/full/{0}/{1}.jpg'.format(
                bucket,
                name
            )

    def string_conversion(self, product):
        for k, v in product.items():
            try:
                nk = k.encode('ascii')
            except:
                print("Failed string conversion key: ",k)
            try:
                v = v.encode('ascii')
            except:
                if not(isinstance(v, int) or isinstance(v, type(None))):
                    print("Failed string conversion value: ", v)
            product[k] = v

    def obsolete(self, product):
        obsolete = product.get('obsolete')
        if obsolete is True: return True;
        if obsolete is False: return False;
        title = product['title'].lower()
        try:
            obsolete = product['obsolete'].lower()
        except:
            obsolete = ""
        if (
            ("obsolete" in title and not("not" in title)) or
            ("obsolete" in obsolete and not("not" in obsolete))
        ):
            return True
        return False

    def discontinued(self, title):
        ltitle = title.lower()
        if "no longer available" in ltitle:
            return True
        if "discontinued" in ltitle:
            return True
        return False

    def product_handle(self, product):
        manufacturer = product.get('manufacturer')
        part_number = product.get('part_number')
        product['product_handle'] = "{0} {1}".format(manufacturer, part_number)

    def clean_title(self, product):
        part_number = product.get('part_number', '')
        scp_sku = product.get('scp_sku','')
        title = product.get('title', '')
        title = title.replace(part_number, '')
        title = title.replace('  ', ' ')
        title = "{0} - {1}".format(part_number.upper(), title)
        if scp_sku in title:
            chars_to_remove = ['(',')']
            try:
                title = title.translate(
                    None, ''.join(chars_to_remove)
                )
            except:
                pass
        product['title'] = title

    def sku(self, product):
        """All Porducts need a sku, which is an all pool spa unique identifier.
        If product['sku'] doesn't exist, try and make it.
        :return bool: True if sku exists or we can make one, else False.
        """

        sku = product.get('sku')
        if sku:
            return True
        try:
            manufacturer = get_manufacturer(
                product.get(
                    'manufacturer',
                    product.get('vendor')
                )
            )

            part_number = product.get(
                'part_number',
                product.get('oem', product.get('upc'))
            )
            product['sku'] = make_sku(manufacturer,part_number)
            return True
        except:
            print("Failed to get sku".format(product))
        return False

    def get_dimensions(self, dimensions):
        try:
            ldimensions = dimensions.lower()
            return ldimensions.split('x')
        except:
            return [None, None, None]

    def product_type(self, checklist):
        """products are either parts or wholegoods.
        Take a best guess that it either has the word 'Part' in it or
        it is a wholegood.
        :param product: a string that may contain product type information
        :return: 'Part' or 'Wholegood' or just return argument given
        """
        for s in checklist:
            if not s:
                continue
            ls = s.lower()
            wholegood = [
                'equipment' in ls,
                'wholegood' in ls,
                'unit' in ls
            ]
            if "part" in ls or "replac" in ls:
                return "part"
            elif any(wholegood):
                return "wholegood"
            else:
                return "part"

    def pool_type(self, checklist):
        for s in checklist:
            if not s:
                continue
            if "comm" in s.lower():
                return "commercial"
        return "residential"

    def pool_or_spa(self, checklist):
        for s in checklist:
            if not s:
                continue
            if "spa" in s.lower():
                return "spa"
            else:
                return "pool"

    def type_handler(self, product):
        checklist = []
        for category in product['categories']:
            checklist.append(category['category'])
        checklist.append(product.get('type'))
        checklist.append(product.get('category'))
        checklist.append(product.get('subcategory'))
        checklist.append(product.get('scp_category'))
        checklist.append(product.get('optimus_category'))
        checklist.append(product.get('title'))
        product['product_type'] = self.product_type(checklist)
        product['pool_type'] = self.pool_type(checklist)
        product['pool_or_spa'] = self.pool_or_spa(checklist)

    def cost(self, cost):
        """Get a float representation of the cost."""
        try:
            return clean_cost(cost)
        except:
            pass
        return cost

    def manufacturer(self, product):
        """Get a normalized version of the manufacturer.
        Companies that provide the product information often have
        different versions of the manufacturer name.
        """
        product['manufacturer'] = get_manufacturer(product.get('manufacturer'))

class ShopifyFileMaker(FileMaker):


    def start(self):
        for product in self.import_handler():
            self.aps_import(product)

    def aps_import(self, product):
        curr_product = self.current_product(product)
        oem = product.get('oem')
        part_number = product.get('part_number')
        sku = product.get('sku')
        title = product.get('title')
        manufacturer = product.get('manufacturer')
        description = product.get('description')
        handle = product.get(
            'product_handle', shopify_handle(manufacturer, oem)
        )
        category = product.get('category')
        tags = product.get('tags')
        cost = product.get('cost')
        curr_product['Vendor'] = manufacturer
        curr_product['Title'] = title
        curr_product['Published'] = True
        curr_product['Handle'] = handle
        curr_product['Type'] = category
        #curr_product['Option2 Name'] = "Fits Model"
        #curr_product['Option2 Value'] = datum['title']
        # SEO definitions
        curr_product['SEO Description'] = "{0} {1}".format(title, description)
        curr_product['SEO Title'] = title
        # Variant definitions
        curr_product['Variant SKU'] = sku
        curr_product['Variant Barcode'] = product.get('upc')
        curr_product['Variant Weight Unit'] = product.get('weight')
        curr_product['Variant Price'] = make_price(product.get('cost'))
        img = product.get('image_url')
        if img:
            curr_product['Image Src'] = img
            curr_product['Image Alt Text'] = part_number
            tags.append('has-image')

        else:
            tags.append('no-image')

        if cost:
            curr_product['Variant Inventory Qty'] = 5
        else:
            curr_product['Variant Inventory Qty'] = 0
        if part_number:
            curr_product['Option1 Name'] = "Part Number"
            curr_product['Option1 Value'] = part_number
        curr_product['Variant Inventory Policy'] = "deny"
        curr_product['Variant Fulfillment Service'] = "manual"
        curr_product['Variant Inventory Tracker'] = "shopify"
        curr_product['Variant Requires Shipping'] = True
        curr_product['Tags'] = ','.join(tags)




class AmazonFileMaker(FileMaker):

    def __init__(self, files, outfile, template, ext="json", mappers=None):
        super(AmazonFileMaker, self).__init__(
            files,
            outfile,
            template,
            ext,
            mappers
        )
        self._action = 'a'
        self._quantity = 0
        self._id_type = 3 #UPC, 1 is ASIN
        self._condition = 11
        self._leadtime = 30
        self._fba = False
        self._fulfillment = "DEFAULT" #AMAZON_NA


    def start(self):
        for product in self.import_handler():
            self.aps_import(product)

    def fba_price_adjustment(self, price):
        try:
            return max(math.ceil((price + (price*.4))), 5.99)
        except:
            print("Unable to adjust price".format(price))
        return price

    def fba(self, sku):
        if FBA.get(sku):
            return True
        return False

    @property
    def action(self):
        return self._action

    @property
    def quantity(self):
        return self._quantity

    @property
    def id_type(self):
        return self._id_type

    @property
    def condition(self):
        return self._condition

    @property
    def leadtime(self):
        return self._leadtime

    @property
    def fba(self):
        return self._fba

    @property
    def fulfillment(self):
        return self._fulfillment


    @action.setter
    def action(self, value):
        self._action = value

    @quantity.setter
    def quantity(self, value):
        self._quantity = value

    @id_type.setter
    def id_type(self, value):
        self._id_type = value

    @condition.setter
    def condition(self, value):
        self._condition = value

    @leadtime.setter
    def leadtime(self, value):
        self._leadtime = value

    @fba.setter
    def fba(self, value):
        self._fba = value

    @fulfillment.setter
    def fulfillment(self, value):
        self._fulfillment = value

class AmazonInventoryLoader(AmazonFileMaker):


    def aps_import(self, product):
        upc = product.get('upc')
        if not upc: return
        sku = product.get('sku')
        curr_product = self.current_product(product)
        oem = product.get('oem')
        part_number = product.get('part_number')
        fulfillment = product.get('fulfillment', '')
        title = product.get('title')
        manufacturer = product.get('manufacturer')
        description = product.get('description')
        cost = product.get('cost')
        price = make_price(cost, .4)
        asin = product.get('asin')
        minprice = make_price(cost, multiplier=.25)
        maxprice = make_price(price, multiplier=20)
        curr_product['sku'] = sku
        curr_product['product-id-type'] = self.id_type
        curr_product['product-id'] = upc
        curr_product['price'] = price
        curr_product['minimum-seller-allowed-price'] = minprice
        curr_product['maximum-seller-allowed-price'] = maxprice
        curr_product['item-condition'] = self.condition
        curr_product['quantity'] = self.quantity
        curr_product['add-delete'] = self.action
        curr_product['fulfillment-center-id'] = fulfillment
        curr_product['leadtime-to-ship'] = self.leadtime
        if fulfillment == "AMAZON_NA":
            price = self.fba_price_adjustment(price)
            curr_product['product-id-type'] = 1
            curr_product['product-id'] = asin
            curr_product['quantity'] = ""
            curr_product['leadtime-to-ship'] = ""
        curr_product['price'] = price



class AmazonCategoryLoader(AmazonFileMaker):


    def aps_import(self, product):
        upc = product.get('upc')
        sku = product.get('sku')
        if self.filter_fba(sku): return
        if not upc: return
        curr_product = self.current_product(product)
        oem = product.get('oem')
        part_number = product.get('part_number')
        title = product.get('title')
        manufacturer = product.get('manufacturer')
        description = product.get('description')
        cost = product.get('cost')
        price = make_price(cost, .4)
        minprice = make_price(cost, multiplier=.25)
        maxprice = make_price(cost, multiplier=.90)
        curr_product['item_sku'] = sku
        curr_product['external_product_id'] = upc
        curr_product['external_product_id_type'] = self.id_type
        curr_product['standard_price'] = price
        curr_product['list_price'] = product.get('list_price')
        curr_product['condition_type'] = self.condition
        curr_product['quantity'] = self.quantity
        curr_product['update_delete'] = self.action
        curr_product['item-note'] = product.get('item-note', '')
        curr_product['fulfillment-center-id'] = product.get(
            'fulfillment-center-id',''
        )
        curr_product['fulfillment_latency'] = self.leadtime
        curr_product['product_descrition'] = description
        curr_product['brand_name'] = manufacturer
        curr_product['manufacturer'] = manufacturer
        curr_product['part_number'] = part_number
        curr_product['model'] = part_number
        # get category from amazon
        curr_product['feed_product_type'] = ""
        curr_product['item_type'] = ""
        curr_product['item_width'] = product.get('width')
        curr_product['item_height'] = product.get('height')
        curr_product['item_length'] = product.get('length')
        curr_product['item_length_unit_of_measure'] = 'IN'
        curr_product['item_weight'] = product.get('weight')
        curr_product['item_weight_unit_of_measure'] = 'LB'
        self.check_dimensions(curr_product)

    def check_dimensions(self, product):
        if not product['item_weight']:
            product['item_weight_unit_of_measure'] = ""
        hwl = [
            product['item_height'],
            product['item_width'],
            product['item_length']
        ]

        if not all(hwl):
            product['item_height'] = ''
            product['item_width'] = ''
            product['item_length'] = ''


if "__main__" == __name__:
    import sys
    action = sys.argv[1]
    ext = sys.argv[2]
    manufacturer = sys.argv[3]
    if not ext:
        ext = "json"
    if action == "aps":
        files = [
            "../cc/2016/{}_cc.json".format(manufacturer),
            "../scp/2016/{}_scp.json".format(manufacturer),
            "../optimus/2016/{}_optimus.json".format(manufacturer),
            "../manufacturer/{}_man_2.csv".format(manufacturer),
            "../manufacturer/{}_man.json".format(manufacturer)
        ]
        outfile = "../aps/{}_aps".format(manufacturer)
        fm = ApsFileMaker(files, outfile, APS_TEMPLATE, ext=ext)
        fm.start()
        fm.finish()
    elif action == "shopify":
        files = [
            "../aps/{}_aps.json".format(manufacturer),
        ]
        outfile = "../shopify/shopify_ready/{}_shopify".format(manufacturer)
        fm = ShopifyFileMaker(files, outfile, SHOPIFY_TEMPLATE, ext=ext)
        fm.start()
        fm.finish()
    elif action == "amazon":
        files = [
            "../aps/{}_aps.json".format(manufacturer),
        ]
        outfile = "../amazon/2016/1/{}_amazon".format(manufacturer)
        fm = AmazonInventoryLoader(files, outfile, INVENTORY_LOADER, ext=ext)
        fm.start()
        fm.finish()
    else:
        pass



