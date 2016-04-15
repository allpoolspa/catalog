import re
from copy import deepcopy
from compiler.ast import flatten
from aps_categories import _CLEANCATS, TYPES_N_TAGS as TNT


class TypeNTags(object):

    def __init__(self):
        self._thetype = ""
        self._tags = set()

    def find(self, product):

        manufacturer = product.get('manufacturer')
        items = self._get_items(product)
        self.thetype = self.findtype(items, manufacturer)

        if self.thetype is "Miscellaneous":
            generic_tags = self.get_all_tags()
        else:
            generic_tags = TNT.get(self.thetype)
        self.tags = self.findtags(items, generic_tags, product)
        self._clean_tags()
        self.tags = list(tag.lower() for tag in self.tags)




    def findtags(self, items, generic_tags, product):
        tags = set()
        tags.add(self._pumps(product))
        tags.add(self._orings(product.get('title')))
        try:
            tags.add(product.get('manufacturer').lower())
        except:
            pass
        try:
            flat_generic_tags = flatten(generic_tags)
        except:
            print self.thetype
            print generic_tags
            raise KeyError
        for item in items:
            if not item: continue
            lowitem = item.lower()
            for tag in flat_generic_tags:
                if not tag: continue
                if tag == 'led':
                    pattern = re.compile('\W+\led[^\d\w]')
                    found1 = pattern.search(lowitem)
                    pattern = re.compile('\W+\led[^\d\w]')
                    found2 = pattern.search(lowitem)
                    if found1 or found2:
                        tags.add(tag)
                elif tag == 'de':
                    pattern = re.compile('\W+de[^\d\w]')
                    found1 = pattern.search(lowitem)
                    pattern = re.compile('\s+\de$')
                    found2 = pattern.search(lowitem)
                    pattern = re.compile('\W+\de$')
                    found3 = pattern.search(lowitem)
                    if found1 or found2 or found3:
                        print 'found2',item
                        tags.add(tag)
                elif tag == 'spa':
                    pattern = re.compile('\W+spa[^\d\w]')
                    found1 = pattern.search(lowitem)
                    pattern = re.compile('\s+\spa$')
                    found2 = pattern.search(lowitem)
                    pattern = re.compile('\W+\spa$')
                    found3 = pattern.search(lowitem)
                    if found1 or found2 or found3:
                        print 'found2',item
                        tags.add(tag)
                else:
                    low_tag = tag.lower()
                    if lowitem in low_tag or low_tag in lowitem:
                        tags.add(tag)
        return tags

    def findtype(self, items, manufacturer=None):
        atype = self.type_by_direct_match(items)
        if atype:
            return atype
        for item in items:
            if not item: continue
            try:
                item = item.encode('ascii')
            except:
                continue
            atype = self.type_by_relative_match(item)
            if atype:
                return atype
            atype = self.type_by_hashed_categories(item)
            if atype:
                return atype
            atype = self.type_by_synonyms(item)
            if atype:
                return atype
        atype = self.type_by_manufacturer(manufacturer)
        if atype:
            return atype
        return "Miscellaneous"


    def type_by_direct_match(self, items):
        for item in items:
            if not item: continue
            try:
                t = TNT[item]
                return item
            except:
                pass
            titem = item.title()
            if TNT.get(titem):
                return titem
        return None

    def type_by_relative_match(self, item):
        for k in TNT.keys():
            lk = k.lower()
            litem = item.lower()
            try:
                shortk = lk[:-1]
                check = [
                    lk in litem,
                    litem in lk,
                    litem in shortk,
                    shortk in litem
                ]
                if any(check):
                    if "Heat Pumps" == k and "heat pump" in litem:
                        return k
                    elif "Heat Pumps" == k and "pump" in litem:
                        return "Pumps"
                    elif "Pumps" == k and "heat pump" in litem:
                        return "Heat Pumps"
                    else:
                        return k
            except:
                print k, item
                pass

    def type_by_hashed_categories(self, item):
        try:
            pattern = re.compile('[\W_]+')
            citem = pattern.sub('', item).lower()
            possible_categories = ""
            if _CLEANCATS.get(citem):
                possible_categories = _CLEANCATS.get(citem)
                for cat in possible_categories.split(','):
                    try:
                        cat = cat.encode('ascii').lstrip()
                        if TNT.get(cat):
                            return cat
                    except:
                        pass
        except:
            return None

    def type_by_manufacturer(self, manufacturer):
        returns = {
            'US SEAL': "Pumps",
            'Unicel': "Filters",
            'Raypak': "Heaters",
            'Odyssey': "Covers",
            'Polaris': "Pool Cleaners",
            "GAME": "Floats & Toys",
            "Aladdin": "O-Rings & Gaskets",
            "S.R. Smith": "Deck Accessories",
            "Afras": "White Goods"
        }
        return returns.get(manufacturer)

    def get_all_tags(self):
        return set([i for v in TNT.values() for i in flatten(v)])

    def _get_items(self, product):
        items = set()
        for category in product['categories']:
            items.add(category['category'])
        items.add(product.get('category'))
        title = self._abbreviations(product.get('title'))
        items.add(title)
        items.add(product.get('type'))
        items.add(product.get('product_type'))
        items.add(product.get('pool_type'))
        items.add(product.get('pool_or_spa'))
        items.add(product.get('manufacturer'))
        return items


    def _pumps(self, product):
        manufacturer = 'US SEAL' == product.get('manufacturer')
        try:
            title = product['title'].lower()
            sku = product['sku'].lower()
        except:
            return
        pump_seals = ['seal' in title, 'ps' in sku]
        capacitors = ['mfd' in title, 'bc' in sku]
        pumps = ['variable' in title, '2 speed' in title]

        if any(pump_seals) and manufacturer:
            return 'pump seal'
        elif any(capacitors) and manufacturer:
            return 'capacitor'
        elif 'variable' in title:
            return 'variable'
        elif '2 speed' in title:
            return 'two speed'
        return ""

    def _orings(self, title):
        if 'orng' in title:
            return "o-ring"

    def _abbreviations(self, title):
        if not title: return
        abbrevations = {
             "vlv": "Valve",
             "pmp": "Pump",
             'orng': 'O-Ring',
             'skim': 'Skimmer',
             'bskt': 'Basket',
             'htr': 'Heater',
             'exch': 'Exchanger',
             'vrbl': 'Variable',
             'spd' : 'Speed'
        }
        ltitle = title.lower()
        for k,v in abbrevations.items():
            if k in ltitle:
                ltitle = ltitle.replace(k, v)
        return ltitle



    def type_by_synonyms(self, item):
        synonyms = {
            "Pumps" :[
                'HP', 'PMP', 'Whisperflo', "Intelliflo", 'Tristar',
                'Stealth', 'PHP', 'Northstar', 'impeller',
            ],
            "Lighting" :[
                'colorlogic',
                'light',
                'lite',
                '75W',
                '0W',
                'incandescent',
                'led',
                'halogen',
                'crystalogic',
                '12V',
            ],
            "Skimmers" :['skim'],
            "Filters" :['manifold', 'sand', 'cartridge', 'grid'],
            "Sanitization" :[
                'chlorine',
                'feeder',
                'aquarite',
                'salt',
                'ozone',
                'bromine',
                ' ph '
            ],
            'Air Blowers': ['Blower'],
            'Valves': ['VLV', 'Valve'],
            "Automation" :['omnilogic', 'transceiver', 'wifi', 'remote'],
            'Cleaners': [
            'Dolphin', 'Navigator', 'PoolVac', 'Aquabug', 'Polaris',
            'Aquanot', 'Wheel'

            ],
            'Heaters':[
                'Heat Exchanger', 'Headers', 'Cupper', 'Exhaust', 'Hood',
                'heat exch'
            ],
            "Maintenance": [
                'tool', 'wrench', 'caddy', 'saddle clamp', 'test plug'
            ],
            "White Goods" :[
                'pvc', 'fitting', 'bskt', 'junction', 'union', 'gauge', 'basket'
            ]
        }
        litem = item.lower()
        for k, values in synonyms.items():
            for v in values:
                lv = v.lower()
                check = [
                    lv in litem, lv in item, v in item, v in litem
                ]
                if any(check):
                    return k
        return None

    def _clean_tags(self):
        self.tags.discard(None)
        self.tags.discard("")
        self.tags.discard(False)
        equipments = [
            ('equipment' in tag
                or 'wholegood' in tag
                or 'whole good' in tag
                or 'unit' in tag
            )
            for tag in self.tags
        ]
        parts = [ ('part' in tag or 'kit' in tag) for tag in self.tags]
        if any(parts) and any(equipments):
            self.tags.discard('part')
        elif any('kit' in tag for tag in self.tags):
            self.tags.add('part')
        if any(equipments):
            self.tags.discard('unit')
            self.tags.discard('whole good')
            self.tags.discard('equipment')
            self.tags.add("wholegood")
        if any('spa' in tag for tag in self.tags):
            self.tags.discard('pool')
        if any('commercial' in tag for tag in self.tags):
            self.tags.discard('residential')

    @property
    def thetype(self):
        return self._thetype

    @thetype.setter
    def thetype(self, value):
        self._thetype = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

