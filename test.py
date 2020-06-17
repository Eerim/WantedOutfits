import pandas as pd


def removeProducts(products):
    contents = pd.DataFrame(pd.read_csv('products1.csv', delimiter=','))
    for product in products:
        contents = contents.drop(
            contents[contents.SKU == product['stok kodu']].index, axis=0)
        contents.to_csv(r'products1.csv', index=False)
    print(len(products), " product(s) has been deleted.")


def salepricechange(products):
    contents = pd.DataFrame(pd.read_csv('products1.csv', delimiter=','))
    for product in products:
        contents.loc[contents.SKU ==
                     product['stok kodu'], ['Sale price']] = product['yeni fiyat']
        contents.to_csv(r'products1.csv', index=False)
    print(len(products), " product(s) sale prices has been changed.")


def regularpricechange(products):
    contents = pd.DataFrame(pd.read_csv('products1.csv', delimiter=','))
    for product in products:
        print(product['stok kodu'])
        contents.loc[contents.SKU ==
                     product['stok kodu'], ['Regular price']] = product['yeni fiyat']
        contents.to_csv(r'products1.csv', index=False)
    print(len(products), " product(s) regular prices has been changed.")


def stockchange(products):
    contents = pd.DataFrame(pd.read_csv('products1.csv', delimiter=','))
    for product in products:
        contents.loc[contents.SKU ==
                     product['stok kodu'], ['Stock']] = product['yeni stok']
        contents.to_csv(r'products1.csv', index=False)
    print(len(products), " product(s) stock info has been changed.")


def statuschange(products):
    contents = pd.DataFrame(pd.read_csv('products1.csv', delimiter=','))
    for product in products:
        contents.loc[contents.SKU ==
                     product['stok kodu'], ['Published']] = product['yeni status']
        contents.to_csv(r'products1.csv', index=False)
    print(len(products), " product(s) published info has been changed.")


def addproducts2dataset(products):
    contents = pd.DataFrame(pd.read_csv('products1.csv', delimiter=','))
    for product in products:
        contents = contents.append(product, ignore_index=True)
        contents.to_csv(r'products1.csv', index=False)
        print(product["SKU"])
    print(len(products), " product(s) added.")


ekleneceklerList = [{"SKU": "MD7778",
                     "Type": "simple",
                     "Name": "henelübe",
                     "Published": "1",
                     "Description": "",
                     "Stock": "25",
                     "Sale Price": "",
                     "Regular Price": "35.50",
                     "Images": "",
                     "Attribute 1 name": "",
                     "Attribute 1 value(s)": "",
                     "Attribute 2 name": "",
                     "Attribute 2 value(s)": "",
                     "Categories": "All products, All products > Clothing",
                     "Is featured?": "0",
                     "Visibility in catalogue": "visible",
                     "Tax status": "taxable",
                     "Tax class": "",
                     "In stock?": "1",
                     "Backorders allowed?": "0",
                     "Sold individually?": "0",
                     "Allow customer reviews?": "1",
                     "Parent": "",
                     "Position": "0",
                     "Attribute 1 visible": "",
                     "Attribute 2 visible": ""
                     },
                    {"SKU": "MD7779",
                     "Type": "simple",
                     "Name": "henelübe",
                     "Published": "1",
                     "Description": "",
                     "Stock": "25",
                     "Sale Price": "",
                     "Regular Price": "35.50",
                     "Images": "",
                     "Attribute 1 name": "",
                     "Attribute 1 value(s)": "",
                     "Attribute 2 name": "",
                     "Attribute 2 value(s)": "",
                     "Categories": "All products, All products > Clothing",
                     "Is featured?": "0",
                     "Visibility in catalogue": "visible",
                     "Tax status": "taxable",
                     "Tax class": "",
                     "In stock?": "1",
                     "Backorders allowed?": "0",
                     "Sold individually?": "0",
                     "Allow customer reviews?": "1",
                     "Parent": "",
                     "Position": "0",
                     "Attribute 1 visible": "",
                     "Attribute 2 visible": ""
                     }]


addproducts2dataset(ekleneceklerList)
