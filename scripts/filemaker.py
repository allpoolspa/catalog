#
import re
import json
import csv
from copy import deepcopy
from templates import APS_TEMPLATE, SHOPIFY_TEMPLATE
from amazon_variables import CATEGORY_INVENTORY_FILE, INVENTORY_LOADER
from aps_categories import (_CLEANCATS, TYPES_N_TAGS as TNT)
from scripts import (
    clean_cost,
    make_price,
    make_sku,
    get_manufacturer,
    shopify_handle
)

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
            return

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
            return

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
            curr_product['list_price'] = product.get('list_price')
        if not curr_product.get('cost'):
            curr_product['cost'] = product.get('price')
        if not curr_product.get('upc'):
            curr_product['upc'] = product.get('upc')

    def scp_import(self, product):
        """Import products from scp."""
        if not self.sku(product): return;
        curr_product = self.current_product(product)

        self.common_keys(curr_product, product)
        curr_product['upc'] = product.get('upc')
        curr_product['available'] = product.get('availability')
        curr_product['obsolete'] = product.get('obsolete')
        curr_product['type'] = product.get('product_line')
        curr_product['weight'] = product.get('weight')
        curr_product['uom'] = product.get('uom')
        l,w,h = self.scp_dimensions(product.get('dimensions'))
        curr_product['length'] = l
        curr_product['width'] = w
        curr_product['height'] = h
        curr_product['scp_cost'] = product.get('price')
        curr_product['scp_sku'] = product.get('product_number')
        curr_product['scp_category'] = product.get('department')

    def cc_import(self, product):
        """Import products from carecraft."""
        if not self.sku(product): return;
        curr_product = self.current_product(product)

        self.common_keys(curr_product, product)
        curr_product['cost'] = product.get('price')
        curr_product['carecraft_cost'] = product.get('price')

    def optimus_import(self, wholegood):
        """Import products from optimus."""
        for product in wholegood['parts']:
            if not self.sku(product): continue;
            curr_product = self.current_product(product)
            self.common_keys(curr_product, product)
            curr_product['parent'] = product.get('fits_model')
            curr_product['parent_id'] = wholegood.get('modelid')
            try:
                curr_product['image_url'] = product.get('image_urls')[0]
            except:
                curr_product['image_url'] = product.get('image_urls')
            curr_product['type'] = "Part"
            curr_product['optimus_cost'] = product.get('price')
            curr_product['optimus_sku'] = product.get('optimus_sku')
            curr_product['optimus_category'] = wholegood.get('category')

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
                    """.format(scp, cc, opt, manufacturer)
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

            product['cost'] = self.cost(product.get('cost'))
            product['list_price'] = self.cost(product.get('list_price'))
            product['scp_cost'] = self.cost(product.get('scp_cost'))
            product['optimus_cost'] = self.cost(product.get('optimus_cost'))
            self.type_handler(product)
            self.manufacturer(product)
            self.clean_title(product)
            self.product_handle(product)
            product['obsolete'] = self.obsolete(product)
            product['discontinued'] = self.discontinued(
                product.get('title', False)
            )



    # Helper functions

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
        if "discontinued" in title.lower():
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
        if part_number not in title:
            title +='- {}'.format(part_number)
        if scp_sku in title:
            title = title.replace('  ', ' ')
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
        try:
            manufacturer = get_manufacturer(
                product.get(
                    'manufacturer',
                    product.get('vendor')
                )
            )
            part_number = product.get(
                'part_number',
                product.get(
                    'oem',
                    product.get('upc')
                )
            )
            product['sku'] = make_sku(manufacturer,part_number)
            return True
        except:
            print("Failed to get sku".format(product))
        return False

    def scp_dimensions(self, dimensions):
        try:
            return dimensions.split('x')
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
            if "part" in ls or "replac" in ls:
                return "part"
            else:
                return "wholegood"

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
        category, tags = self._type_n_tags(product)
        cost = product.get('cost')
        curr_product['Vendor'] = manufacturer
        curr_product['Title'] = title
        curr_product['Published'] = True
        curr_product['Handle'] = handle
        curr_product['Type'] = category
        curr_product['Tags'] = tags
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
            abbr = sku[:3]
            curr_product['Image Src'] = self.image_url(abbr, sku)
            curr_product['Image Alt Text'] = part_number
            tags += ',has-image'

        else:
            tags += ',no-image'

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
        curr_product['Tags'] = self._clean_tags(tags)


    def image_url(self,bucket, name):
        return 'https://s3-us-west-1.amazonaws.com/oppics/full/{0}/{1}.jpg'.format(
            bucket,
            name
        )

    def _type_n_tags(self, product):
        category = product.get('category')
        subcategory = product.get('subcategory')
        op_category = product.get('op_category')
        scp_category = product.get('scp_category')
        title = product.get('title')
        atype = product.get('type')
        product_type = product.get('product_type')
        pool_type = product.get('pool_type')
        pool_or_spa = product.get('pool_or_spa')

        items = [category, subcategory, op_category, scp_category, atype]
        try:
            for item in items:
                try:
                    item = item.encode('ascii')
                except:
                    continue
                titem = item.title()
                pattern = re.compile('[\W_]+')
                citem = pattern.sub('', item).lower()
                possible_categories = ""
                if TNT.get(titem):
                    possible_categories = titem
                    break
                elif _CLEANCATS.get(citem):
                    possible_categories = _CLEANCATS.get(citem)
                    break
            cats = possible_categories.split(',')
            for cat in cats:
                cat = str(cat.encode('ascii'))
                cat = cat.lstrip()
                try:
                    tags = TNT.get(cat)
                    tags = self._gettags(category, possible_categories, tags, title)
                    tags += ",{0},{1},{2}".format(
                        pool_type,
                        product_type,
                        pool_or_spa
                    )
                    return cat, tags
                except:
                    pass
                    # need a log here
        except:
            print("No type or tags for: {0}, {1}, {2}, {3}, {4}".format(
                    category,
                    op_category,
                    scp_category,
                    subcategory,
                    atype
                )
            )
        return "Accessories", "no-cat,"

    def _gettags(self, key, categories, tags, title=""):
        product_tags = ""
        try:
            lkey = key.lower()
        except:
            lkey = ""
        try:
            lcategories = categories.lower()
        except:
            lcategories = ""
        try:
            ltitle = title.lower()
        except:
            ltitle = ""

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

    def _clean_tags(self, tags):
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
        self._id_type = 3
        self._condition = 11
        self._leadtime = 30
        self._fba = False


    def start(self):
        for product in self.import_handler():
            self.aps_import(product)

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

class AmazonInventoryLoader(AmazonFileMaker):


    def aps_import(self, product):
        upc = product.get('upc')
        if not upc: return
        curr_product = self.current_product(product)
        oem = product.get('oem')
        part_number = product.get('part_number')
        sku = product.get('sku')
        title = product.get('title')
        manufacturer = product.get('manufacturer')
        description = product.get('description')
        cost = product.get('cost')
        price = make_price(cost, .4)
        minprice = make_price(cost, multiplier=.25)
        maxprice = make_price(cost, multiplier=.90)
        curr_product['sku'] = sku
        curr_product['product-id'] = upc
        curr_product['product-id-type'] = self.id_type
        curr_product['price'] = price
        curr_product['minimum-seller-allowed-price'] = minprice
        curr_product['maximum-seller-allowed-price'] = maxprice
        curr_product['item-condition'] = self.condition
        curr_product['quantity'] = self.quantity
        curr_product['add-delete'] = self.action
        curr_product['item-note'] = product.get('item-note', '')
        curr_product['fulfillment-center-id'] = product.get(
            'fulfillment-center-id',''
        )
        curr_product['leadtime-to-ship'] = self.leadtime

class AmazonCategoryLoader(AmazonFileMaker):


    def aps_import(self, product):
        upc = product.get('upc')
        if not upc: return
        curr_product = self.current_product(product)
        oem = product.get('oem')
        part_number = product.get('part_number')
        sku = product.get('sku')
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
        curr_product['item_length_unit_of_measure'] = product.get('IN')
        curr_product['item_weight'] = product.get('weight')
        curr_product['item_weight_unit_of_measure'] = product.get('LB')




if "__main__" == __name__:
    import sys
    action = sys.argv[1]
    ext = sys.argv[2]
    manufacturer = sys.argv[3]
    if not ext:
        ext = "json"
    if action == "aps":
        files = [
            "../cc/{}_cc.json".format(manufacturer),
            "../scp/2016/{}_scp.json".format(manufacturer),
            "../optimus/{}_optimus.json".format(manufacturer)
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



