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
