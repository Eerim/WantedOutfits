import pandas as pd


def removeProducs(products):
    contents = pd.DataFrame(pd.read_csv('products.csv', delimiter=','))
    for product in products:
        contents = contents.drop(
            contents[contents.SKU == product['stok kodu']].index, axis=0)
        print(contents)


def salepricechange(products):
    contents = pd.DataFrame(pd.read_csv('products.csv', delimiter=','))
    for product in products:
        contents.loc[contents.SKU ==
                     product['stok kodu'], ['Sale price']] = product['yeni fiyat']
        print(contents.loc[contents.SKU ==
                           product['stok kodu'], ['Sale price']])


def regularpricechange(products):
    contents = pd.DataFrame(pd.read_csv('products.csv', delimiter=','))
    for product in products:
        print(product['stok kodu'])
        contents.loc[contents.SKU ==
                     product['stok kodu'], ['Regular price']] = product['yeni fiyat']
        print(contents.loc[contents.SKU ==
                           product['stok kodu'], ['Regular price']])


def stockchange(products):
    contents = pd.DataFrame(pd.read_csv('products.csv', delimiter=','))
    for product in products:
        print(product['stok kodu'])
        contents.loc[contents.SKU ==
                     product['stok kodu'], ['Stock']] = product['yeni stok']
        print(contents.loc[contents.SKU ==
                           product['stok kodu'], ['Stock']])


def statuschange(products):
    contents = pd.DataFrame(pd.read_csv('products.csv', delimiter=','))
    for product in products:
        print(product['stok kodu'])
        contents.loc[contents.SKU ==
                     product['stok kodu'], ['Published']] = product['yeni status']
        print(contents.loc[contents.SKU ==
                           product['stok kodu'], ['Published']])
        print(contents)


def addproducts(products):
    contents = pd.DataFrame(pd.read_csv('products.csv', delimiter=','))
    print(contents)
    for product in products:
        contents = contents.append(product, ignore_index=True)
        print(contents)


products = [{"stok kodu": "MD7777"}, {"stok kodu": "MD7778"}]
addproducts(products)
