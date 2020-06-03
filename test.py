import pandas as pd


def removeProducs(products):
    contents = pd.DataFrame(pd.read_csv('products.csv', delimiter=','))
    for product in products:
        contents = contents.drop(
            contents[contents.SKU == product['stok kodu']].index, axis=0)
        # contents = contents.drop[contents[contents['SKU']
        #                                  == product['stok kodu']].index]
        print(contents)


def slaepricechange(products):
    contents = pd.DataFrame(pd.read_csv('products.csv', delimiter=','))
    for product in products:
        print(product['stok kodu'])
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


products = [{"stok kodu": "MD2042", 'eski stok': 3, 'yeni stok': 5}]
stockchange(products)
