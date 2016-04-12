import json
import csv
from os import listdir
from os.path import isfile, join



class FbaCostAnalysisReport(object):

    FIELDNAMES = [
        'seller-sku',
        'sku',
        'asin',
        'condition-type',
        'Warehouse-Condition-code',
        'Quantity Available',
        'Quantity',
        'fulfillment-channel-sku',
        'cost',
        'total_cost'
    ]

    MISSING_SKUS = {
        "425-0030":"",
        "R201476":"",
        "0602-15":1.83,
        "RC97385D":47.05,
        "ZOD_R0559000":22.63,
        "HAY_RC97385D":47.05,
        "6628":"",
        "VAL_V20-338":0.05,
        "ZOD_C-55":0.65,
        "MAG_ 0121109015":.87,
        "WW_711-4030":.23,
        "CUS_25062-209":8.01,
        "ALA_O-363-0":.26,
        "R231200 PENTAIR":5.21,
        "PEN_AQ10030":"",
        "ALA_O-151-9":.30,
        "V60-110 DEX2400JN":6.07,
        "CUS_21063-154-000":4.70,
        "AXW431A-HAYWARD":3.87,
        "V22110AZ": 10.40,
        "425-0030B":3.13,
        "ala_800-8":1.15,
        "V20200":7.46,
        "ALA_GO-KIT32V-9":12.53,
        "ALA_GO-KIT77-9":12.93,
        "ALA_Go-Kit2":14.84,
        "ALA_GO-38V":"",
        "ala_750 no-niche skimmer":26.56,
        "VAL-V20-062":17.94,
        "ALA_925 8IN WEIR":4.35,
        "V20390PGN":9.78,
        "V38130":59.39,
    }

    def __init__(self, fba_file):
        self.fba_file = fba_file
        self.aps_files = self.get_aps_files()
        self.fba_products = {}

    def get_aps_files(self):
        return [f for f in listdir('../aps') if isfile(join('../aps', f))]

    def import_fba_inventory_file(self):
        print self.fba_file
        with open(self.fba_file, 'Ur') as f:
            lines = csv.DictReader(f)
            for line in lines:
                yield line

    def import_aps_file(self, infile):
        with open('../aps/{}'.format(infile), 'Ur') as f:
            print "checking {}".format(infile)
            lines = json.load(f, encoding="ascii")
            for line in lines:
                try:
                    yield lines[line]
                except:
                    yield line

    def run(self):
        fbas = self.import_fba_inventory_file()
        for fba in fbas:
            cost = self.MISSING_SKUS.get(fba['sku'])
            if cost:
                fba['cost'] = cost
                quantity = fba.get('Quantity', fba.get('Quantity Available'))
                fba['total_cost'] = cost * float(quantity)
            self.fba_products[fba['sku']] = fba
        for infile in self.aps_files:
            for aps_product in self.import_aps_file(infile):
                sku = aps_product.get('sku')
                part_number = aps_product.get('part_number')
                oem = aps_product.get('oem')
                asin = aps_product.get('asin')
                manufacturer = aps_product.get('manufacturer')
                fba1  = self.fba_products.get(
                    sku
                )
                cost = aps_product.get('cost')
                fba2 = self.fba_products.get(
                    part_number
                )
                if fba1 and not fba1.get('cost'):
                    self.add_cost_analysis(manufacturer, fba1, cost)
                if fba2 and not fba2.get('cost'):
                    self.add_cost_analysis(manufacturer, fba2, cost)

        self.export()




    def add_cost_analysis(self, manufacturer, product, cost):
        if product['sku'] == 'SP1422D' and manufacturer == "Pentair":
            print product
            return
        try:
            product['cost'] = cost
        except:
            pass
        try:
            quantity = product.get('Quantity', product.get('Quantity Available'))
            product['total_cost'] = cost * float(quantity)
        except:
            pass


    def export(self):
        outfile = "../../Reports/AmazonReports/FBAReports/FBACostAnalysis/cost_analysis.csv"
        with open("{0}".format(outfile), 'w') as openfile:
            writer = csv.DictWriter(
                openfile,
                fieldnames=self.FIELDNAMES
            )
            writer.writeheader()
            for product in self.fba_products.values():
                writer.writerow(
                    {
                        k:unicode(v).encode("utf-8")
                        for k,v in product.items()
                    }
                )


if __name__ == "__main__":
    fba_file = "../../Reports/AmazonReports/FBAInventory/fba_inventory_04072016.csv"
    fba_ca = FbaCostAnalysisReport(fba_file)
    fba_ca.run()

