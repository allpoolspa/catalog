import csv
import json



def filter_fba():
    headers = ['sku', 'asin', 'price', 'quantity', 'add-delete']

    allfile = 'inventory_report_03082016.csv'
    upcfile = 'apscom_merchant_inventory_report_03082016.csv'
    fbafile = 'hand_picked_fba_inventory.csv'
    outfile = 'testing.csv'
    deleted = 0
    productlist = {}
    with open("../../AmazonReports/InventoryReports/{}".format(allfile), 'Ur') as infile:
        products = csv.DictReader(infile)
        for product in products:
            sku = product.get('seller-sku', product.get('sku'))
            sku = sku.replace('"', "")
            productlist[sku] = {}
            productlist[sku]['sku'] = sku
            productlist[sku]['price'] = product.get('price')
            productlist[sku]['add-delete'] = 'a'

    with open("../../AmazonReports/InventoryReports/{}".format(upcfile), 'Ur') as infile:
        products = csv.DictReader(infile)
        for product in products:
            sku = product.get('seller-sku', product.get('sku'))
            try:
                sku = sku.replace('"', "")
            except:
                pass
            upc = product.get('upc')
            try:
                upc = upc.replace('"', "")
                productlist[sku]['upc'] = upc
            except:
                pass


    with open("../../AmazonReports/FBAInventory/{}".format(fbafile), 'Ur') as infile:
        products = csv.DictReader(infile)
        for product in products:
            sku = product.get('seller-sku', product.get('sku'))
            #quantity = product.get('Quantity Available')
            try:
                price = productlist[sku].get('price')
                ad = productlist[sku].get('add-delete')
                upc = productlist[sku].get('upc', "")
                asin = product.get('asin')
                asin = asin.replace("?", "")
                #del productlist[sku]
                if upc:
                    print "{0}\t{1}\t{2}\t{3}\t\t\t{4}\t{5}".format(
                        sku, upc, 1, price, 11 , ad
                    )
                #deleted += 1
            except:
                pass

    print deleted

    def writer():
        with open("../../AmazonReports/InventoryReports/{}".format(outfile), "w") as output:
            writer = csv.DictWriter(output, fieldnames=headers)
            writer.writeheader()
            for product in productlist.values():
                writer.writerow(product)


filter_fba()
