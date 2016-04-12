""" This program takes a 
        category file with the following keys:
            CategoryId,Webstore Categories
        manufacturer files with the following keys:
            oem, title, manufacturer, department, product_line
                ***The product_line is the field used to make the category.

"""
import csv
import json
import datetime

from difflib import SequenceMatcher as SM
from collections import OrderedDict as OD
from tfidf_words import TFIDF

class CategoryMatcher:

    def __init__(self, args):
        self.bonus_ctr = 0
        self.called = 0
        self.website_categories = {}
        self.man_categories = {}
        self.connector_dict = {}
        self.category_info = {}
        self.truncated_manufacturers = ['Unicel', 'Raypak', 'Hayward', 'Pentair', 
                        'Zodiac', 'Aladdin', 'US Seal', 'Waterway']
        self.category_files = ['CategoryFiles/ReadyFor_category_matcher/aps_filter_categories_05142015.csv', 
                            'CategoryFiles/ReadyFor_category_matcher/aps_filter_categories_05142015.csv']

        self.filelist = ['Unicel/unicel_scp.json', 'Raypak/raypak_scp.json', 'Zodiac/zodiac_scp.json',
                            'Waterway/waterways_scp.json', 'Hayward/hayward_scp.json', 
                            'USSeal/usseal_scp.json', 'Aladdin/aladdin_scp.json', 'Val-Pak/valpak_manufacturer.csv']
        self.filelist_SKIP = ['Pentair/pentair_manufacturer.csv']

        if args.outputfile_type == None or args.outputfile_type == 'csv':
            self.outputfile = 'both_categories.csv'
        else:
            self.outputfile = 'categories.json'

    def start(self):
        self.read_categories_from_website()
        print 'Read from website...'
        self.read_file_handler()
        print 'Read from files...'
        self.make_connector_dict()
        print 'Made connector table...'
        self.connect_dicts()
        print 'Connected tables...'
        self.statistics()
        self.write_handler()
        self.write_connector_table()
        self.write_man_categories()

    def read_categories_from_website(self):
        for afile in self.category_files:
            with open(afile, 'Ur') as open_file:
                rdr = csv.DictReader(open_file)
                for row in rdr:
                    category = row['Webstore Categories']
                    cid = row['CategoryId']
                    if not category in self.website_categories:
                        self.website_categories[category] = []
                    self.website_categories[category].append(cid)


    def read_file_handler(self):
        for afile in self.filelist:
            if afile.endswith('json'):
                self.json_reader(afile)
            elif afile.endswith('csv'):
                self.csv_reader(afile)
            else:
                print afile, 'is not a csv or json file.'


    def json_reader(self, afile):
        with open(afile, 'Ur') as openfile:
            json_object = json.load(openfile)
            for product in json_object:
                self._make_man_category_dict(product)
                self._make_category_info_dict(product)

    def csv_reader(self, afile):
        with open(afile, 'Ur') as openfile:
            reader = csv.DictReader(openfile)
            for product in reader:
                if product['oem'] == None or product['oem'] == '':
                    continue
                self._make_man_category_dict(product)
                self._make_category_info_dict(product)
        

    def read_categories_from_database(self, category_files):
        #send to get_department.py
        pass

    def _make_man_category_dict(self, product):
        product_line = product['product_line']
        manufacturer = product['manufacturer']
        oem = product['oem']
        truncated_manufacturer = self._manufacturer_map(manufacturer)
        category =  truncated_manufacturer + '>' + product_line

        #Adjusts for Aladdin part numbers that have 'ALA_' prepended to the oem.
        if 'aladdin' in manufacturer.lower():
            oem = 'ALA_' + oem
        if category in self.man_categories.keys():
            self.man_categories[category].append(oem)
        else:
            self.man_categories[category] = []
            self.man_categories[category].append(oem)

    def _make_category_info_dict(self, product):
        oem = product['oem']
        manufacturer = product['manufacturer']

        #Adjusts for Aladdin part numbers that have 'ALA_' prepended to the oem.
        if 'aladdin' in manufacturer.lower():
            oem = 'ALA_' + oem
        self.category_info[oem] = {'man_category': '',
                                    'title': product['title'],
                                    'manufacturer': manufacturer,
                                    'oem': oem,
                                    'platinum_keyword': [],
                                    'amz_category': ''
        }

    def make_connector_dict(self):
        for man_category in self.man_categories.keys():
            highest_score = 0
            best_match = ''
            manufacturer = ''
            manufacturer_string = 'Hayward, Pentair, Zodiac'
            for m in self.truncated_manufacturers:
                if m in man_category:
                    manufacturer = m
                    break
            for category in self.website_categories.keys():

                if manufacturer in category:
                    #Some manufacturers are aftermarket manufacturers and will have
                    #categories with the original manufacturer in it.
                    #Filter these out.
                    #if manufacturer in manufacturer_string and 'brands' in category.lower():
                        #continue
                    temp_score = self._get_score(man_category, category)
                    if highest_score < temp_score:
                        highest_score = temp_score
                        best_match = category

            if 'cleaner' in man_category.lower():
                print man_category, best_match, highest_score
            self.connector_dict[man_category] = best_match

    def _get_score(self, man_category, amz_category):
        self.called += 1
        temp_amz_cat = amz_category.lower()
        temp_man = man_category.lower()
        #filter the word brands out of scoring.
        if 'brands' in temp_amz_cat:
            temp_amz_cat.replace('brands>', '')
        amz_list = self.wordizer(temp_amz_cat)
        man_list = self.wordizer(temp_man)
        synonyms = {'lubes':['lubricants'], 'junction':['maintenance'],
                     'service':['maintenance'],'screws':['maintenance'],
                     'alarms':['safety'],'chlorinators':['chem', 'feeders'],
                     'waterfall':['water', 'feature'], 'laminar':['lights','water','feature'],
                     'designer':['water', 'feature'], 'fountains':['water', 'feature']}
        for word, syns in synonyms.items():
            if word in man_list:
                man_list += syns
        if 'hayward' in man_list and 'heaters' in man_list and not 'venting' in man_list:
            man_list += ['units']
        score = 0.0
        for amz_cat in amz_list:
            amz_word = amz_cat.lower()
            if not amz_word:
                continue
            for man_cat in man_list:
                man_word = man_cat.lower()
                if self.in_checker(amz_word, man_word):
                    if amz_word in TFIDF.keys():
                        score += TFIDF[amz_word]
                    elif man_word in TFIDF.keys():
                        score += TFIDF[man_word]
        #score += SM(None, temp_man, temp_amz_cat).ratio()
        return score

    def in_checker(self, word1, word2):
        #return word1 in word2 or word2 in word1 or word1[:-1] in word2[:-1] or word2[:-1] in word1
        return word1 == word2 or word1[:-1] == word2 or word2[:-1] == word1

    def _manufacturer_map(self, manufacturer):
        truncated_manufacturer = manufacturer
        for m in self.truncated_manufacturers:
            if m.lower() in manufacturer.lower():
                truncated_manufacturer = m
                break
        return truncated_manufacturer

    def connect_dicts(self):
        for man_cat, oem_list in self.man_categories.items():
            amz_cat = self.connector_dict[man_cat]
            for oem in oem_list:
                self.category_info[oem]['man_category'] = man_cat
                self.category_info[oem]['amz_category'] = amz_cat
                if not amz_cat:
                    continue
                for key_word in self.website_categories[amz_cat]:
                    self.category_info[oem]['platinum_keyword'].append("cat_" + key_word)


    def statistics(self):
        amz_cat_ctr = {}
        manufacturer_ctr = {}
        for oem in self.category_info:
            item = self.category_info[oem]
            if item['amz_category'] not in amz_cat_ctr:
                amz_cat_ctr[item['amz_category']] = 1
            else:
                amz_cat_ctr[item['amz_category']] = amz_cat_ctr[item['amz_category']] + 1
            if item['manufacturer'] not in manufacturer_ctr:
                manufacturer_ctr[item['manufacturer']] = 1
            else:
                manufacturer_ctr[item['manufacturer']] = manufacturer_ctr[item['manufacturer']] + 1
        amz = OD(sorted(amz_cat_ctr.items()))
        for man, count in manufacturer_ctr.items():
            print man, ' : ', count
        print '***************************************************'
        print '***************************************************'
        for cat, count in amz.items():
            print cat, ' : ', count
        print '***************************************************'
        print '***************************************************'
        print self.bonus_ctr, '=', self.called

    def wordizer(self, category):
        return category.replace('>', ' ').replace('(', '').replace(')', '').replace('/', ' ').replace('|', ' ').replace(' - ', ' ').replace('&', '').replace('  ', ' ').split(' ')

    #Writers: handle csv and json
    def write_handler(self):
        if self.outputfile.endswith('json'):
            print 'Writing to json file...'
            self.write_json()
        else:
            print 'Writing to csv file'
            self.write_csv()

    def write_man_categories(self):
        with open(self.timeStamped('manufacturer_categories.json'), 'w') as f:
            json.dump(
                self.man_categories.keys(), f, 
                sort_keys = True, indent = 4, ensure_ascii=False
            )

    def write_connector_table(self):
        with open(self.timeStamped('connector_table.csv'), 'w') as f:
            json.dump(
                self.connector_dict, f, 
                sort_keys = True, indent = 4, ensure_ascii=False
            )

    def write_json(self):
        pass

    def write_csv(self):
        ofile = self.timeStamped(self.outputfile)
        with open('CategoryFiles/ReadyForAmzTemplate/'+ofile, 'w') as f:
            writr = csv.DictWriter(f, fieldnames=['man_category', 'title', 
                                    'manufacturer', 'oem', 'platinum_keyword', 'amz_category']
            )
            writr.writeheader()
            print 'Writing to:', ofile
            for k,v in self.category_info.items():
                writr.writerow(v)
        
    def timeStamped(self, fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
        return datetime.datetime.now().strftime(fmt).format(fname=fname)

if __name__ == '__main__':
    from commands import categoryparser
    args = categoryparser()
    CM = CategoryMatcher(args)
    CM.start()