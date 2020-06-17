import xml.etree.ElementTree as ET
import translator
from googletrans import Translator
import urllib.request
import os
import shutil
import datetime
import pandas as pd


def removeProducts(products):
    contents = pd.DataFrame(pd.read_csv('products.csv', delimiter=','))
    for product in products:
        contents = contents.drop(
            contents[contents.SKU == product['stok kodu']].index, axis=0)
        contents.to_csv(r'products.csv', index=False)
    print(len(products), " product(s) has been deleted.")


def salepricechange(products):
    contents = pd.DataFrame(pd.read_csv('products.csv', delimiter=','))
    for product in products:
        contents.loc[contents.SKU ==
                     product['stok kodu'], ['Sale price']] = product['yeni fiyat']
        contents.to_csv(r'products.csv', index=False)
    print(len(products), " product(s) sale prices has been changed.")


def regularpricechange(products):
    contents = pd.DataFrame(pd.read_csv('products.csv', delimiter=','))
    for product in products:
        print(product['stok kodu'])
        contents.loc[contents.SKU ==
                     product['stok kodu'], ['Regular price']] = product['yeni fiyat']
        contents.to_csv(r'products.csv', index=False)
    print(len(products), " product(s) regular prices has been changed.")


def stockchange(products):
    contents = pd.DataFrame(pd.read_csv('products.csv', delimiter=','))
    for product in products:
        contents.loc[contents.SKU ==
                     product['stok kodu'], ['Stock']] = product['yeni stok']
        contents.to_csv(r'products.csv', index=False)
    print(len(products), " product(s) stock info has been changed.")


def statuschange(products):
    contents = pd.DataFrame(pd.read_csv('products1.csv', delimiter=','))
    for product in products:
        contents.loc[contents.SKU ==
                     product['stok kodu'], ['Published']] = product['yeni status']
        contents.to_csv(r'products.csv', index=False)
    print(len(products), " product(s) published info has been changed.")


def addproducts2dataset(products):
    contents = pd.DataFrame(pd.read_csv('products.csv', delimiter=','))
    for product in products:
        contents = contents.append(product, ignore_index=True)
        contents.to_csv(r'products.csv', index=False)
        print(product["SKU"])
    print(len(products), " product(s) added. Please check NAME, DESCRIPTION, ATTIRIBUTE NAMES on database")


def myFunc(e):
    return e['stok kodu']


def addProducts(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    products = []
    options = []
    products = []
    att1_name = ""
    att1_val = []
    att2_name = ""
    att2_val = []
    # print(*products, sep='\n')
    for variants in root.findall('item'):
        skuMain = variants.find('stockCode').text
        isVariant = False
        for variant in variants.findall('variants'):
            for subbranks in variant.findall("variant"):
                isVariant = True
                sku = subbranks.find('vStockCode').text
                stok = subbranks.find('vStockAmount').text
                price = subbranks.find('vPrice1').text
                for opts in subbranks.findall("options"):
                    for opttions in opts.findall("option"):
                        options.append(
                            (opttions.find("variantName").text, opttions.find("variantValue").text))
                    if len(options) == 1:
                        products.append({"stok kodu": sku,
                                         "ürün adı": variants[1].text,
                                         "stok": int(stok),
                                         "status": variants[2].text,
                                         "fiyat": round(float(price)+float(price)*int(variants[15].text)/100, 2),
                                         "vergi": variants[15].text,
                                         "indirim": "",
                                         "indirimli fiyat": "",
                                         "product type": "variation",
                                         "parent": variants[0].text,
                                         "att1 name": options[0][0],
                                         "att1 val": options[0][1],
                                         "tax class": "parent",
                                         "pic1": "",
                                         "pic2": "",
                                         "pic3": "",
                                         "pic4": "",
                                         "ana kategori": variants[6].text,
                                         "alt kategori": variants[7].text,
                                         "açıklama": variants[25].text,
                                         "att2 name": "",
                                         "att2 val": "",
                                         "parent": variants[0].text})
                        att1_name = options[0][0]
                        att1_val.append(options[0][1])
                    else:
                        products.append({"stok kodu": sku,
                                         "ürün adı": variants[1].text,
                                         "stok": int(stok),
                                         "status": variants[2].text,
                                         "fiyat": round(float(price)+float(price)*int(variants[15].text)/100, 2),
                                         "vergi": "",
                                         "indirim": variants[27].text,
                                         "indirimli fiyat": "",
                                         "product type": "variation",
                                         "parent": variants[0].text,
                                         "att1 name": options[0][0],
                                         "att1 val": options[0][1],
                                         "att2 name": options[1][0],
                                         "att2 val": options[1][1],
                                         "tax class": "parent",
                                         "pic1": "",
                                         "pic2": "",
                                         "pic3": "",
                                         "pic4": "",
                                         "ana kategori": variants[6].text,
                                         "alt kategori": variants[7].text,
                                         "açıklama": variants[25].text,
                                         "parent": variants[0].text})
                        att1_name = options[0][0]
                        if len(att1_val) != 0:
                            if att1_val.count(options[0][1]) == 0:
                                att1_val.append(options[0][1])
                        else:
                            att1_val.append(options[0][1])
                        att2_name = options[1][0]
                        if len(att2_val) != 0:
                            if att2_val.count(options[1][1]) == 0:
                                att2_val.append(options[1][1])
                        else:
                            att2_val.append(options[1][1])
                    options = []
            else:
                if isVariant == True:
                    products.append({"stok kodu": skuMain,
                                     "ürün adı": variants[1].text,
                                     "stok": variants[17].text,
                                     "status": variants[2].text,
                                     "fiyat": float(variants[10].text),
                                     "vergi": float(variants[15].text),
                                     "indirim": variants[27].text,
                                     "indirimli fiyat": float(variants[26].text),
                                     "product type": "variable",
                                     "att1 name": att1_name,
                                     "att1 val": att1_val,
                                     "att2 name": att2_name,
                                     "att2 val": att2_val,
                                     "pic1": variants[20].text if variants[20].text == None else variants[20].text if variants[20].text.find('?') == -1 else variants[20].text[:variants[20].text.find('?')],
                                     "pic2": variants[21].text if variants[21].text == None else variants[21].text if variants[21].text.find('?') == -1 else variants[21].text[:variants[21].text.find('?')],
                                     "pic3": variants[22].text if variants[22].text == None else variants[22].text if variants[22].text.find('?') == -1 else variants[22].text[:variants[22].text.find('?')],
                                     "pic4": variants[23].text if variants[23].text == None else variants[23].text if variants[23].text.find('?') == -1 else variants[23].text[:variants[23].text.find('?')],
                                     "ana kategori": variants[6].text,
                                     "alt kategori": variants[7].text,
                                     "açıklama": variants[25].text,
                                     "tax class": "",
                                     "parent": ""})
                    att1_val.clear()
                    att2_val.clear()
                    att1_name = ""
                    att2_name = ""
        if isVariant == False:
            products.append({"stok kodu": variants[0].text,
                             "ürün adı": variants[1].text,
                             "stok": variants[17].text,
                             "status": variants[2].text,
                             "fiyat": float(variants[10].text),
                             "vergi": float(variants[15].text),
                             "indirim": variants[27].text,
                             "indirimli fiyat": float(variants[26].text),
                             "product type": "simple",
                             "pic1": variants[20].text if variants[20].text == None else variants[20].text if variants[20].text.find('?') == -1 else variants[20].text[:variants[20].text.find('?')],
                             "pic2": variants[21].text if variants[21].text == None else variants[21].text if variants[21].text.find('?') == -1 else variants[21].text[:variants[21].text.find('?')],
                             "pic3": variants[22].text if variants[22].text == None else variants[22].text if variants[22].text.find('?') == -1 else variants[22].text[:variants[22].text.find('?')],
                             "pic4": variants[23].text if variants[23].text == None else variants[23].text if variants[23].text.find('?') == -1 else variants[23].text[:variants[23].text.find('?')],
                             "ana kategori": variants[6].text,
                             "alt kategori": variants[7].text,
                             "açıklama": variants[25].text,
                             "parent": "",
                             "att1 name": "",
                             "att1 val": "",
                             "att2 name": "",
                             "att2 val": "",
                             "tax class": ""})
    return products


# dosya adı için bugünün stringini oluştur
# today= str(datetime.datetime.now().day) + str(datetime.datetime.now().month) + str(datetime.datetime.now().year)

# bugünkü xmli indir
# url = 'http://www.modacelikler.com/index.php?do=catalog/output&pCode=2134241870'
# urllib.request.urlretrieve(url, 'index.xml')

productsOld = addProducts('index_old.xml')
productsNew = addProducts('index.xml')
productsOld.sort(key=myFunc)
productsNew.sort(key=myFunc)
i = 0
cikarilacaklarList = []
indirimegirenlerList = []
indirimibitenlerList = []
fiyatidegisenlerList = []
stoguazalanlarList = []
stoguartanlarList = []
statusdegisenlerlist = []
for product in productsOld:
    kont = False
    kont1 = False
    kont2 = False
    kont3 = False
    kont4 = False
    i += 1
    for productNew in productsNew:
        if product["stok kodu"] == productNew["stok kodu"]:
            kont = True
            if product['product type'] != 'variable':
                if product["indirimli fiyat"] == productNew["indirimli fiyat"]:
                    kont1 = True
                if kont1 == False:
                    if product["indirimli fiyat"] > productNew["indirimli fiyat"] or product["indirimli fiyat"] == 0.0:
                        indirimegirenlerList.append({"stok kodu": product["stok kodu"],
                                                     "eski fiyat": product["indirimli fiyat"],
                                                     "yeni fiyat": round(float(productNew["indirimli fiyat"])+float(productNew["indirimli fiyat"])*float(productNew["vergi"]/100), 2)})
                    else:
                        indirimibitenlerList.append({"stok kodu": product["stok kodu"],
                                                     "eski fiyat": product["indirimli fiyat"],
                                                     "yeni fiyat": round(float(productNew["indirimli fiyat"])+float(productNew["indirimli fiyat"])*float(productNew["vergi"])/100, 2)})
                if product["fiyat"] == productNew["fiyat"]:
                    kont2 = True
                if kont2 == False:
                    fiyatidegisenlerList.append({"stok kodu": product["stok kodu"],
                                                 "Eski fiyat": product["fiyat"],
                                                 "Yeni fiyat": productNew["fiyat"]})
            if product["stok"] == productNew["stok"]:
                kont3 = True
            if kont3 == False:
                if product["stok"] > productNew["stok"]:
                    stoguazalanlarList.append({"stok kodu": product["stok kodu"],
                                               "eski stok": product["stok"],
                                               "yeni stok": productNew["stok"]})
                else:
                    stoguartanlarList.append({"stok kodu": product["stok kodu"],
                                              "eski stok": product["stok"],
                                              "yeni stok": productNew["stok"]})
            if product["status"] == productNew["status"]:
                kont4 = True
            if kont4 == False:
                statusdegisenlerlist.append({"stok kodu": product["stok kodu"],
                                             "eski status": product["status"],
                                             "yeni status": productNew["status"]})
            break
    if kont == False:
        cikarilacaklarList.append({"stok kodu": product["stok kodu"]})

i = 0
ekleneceklerList = []
for productNew in productsNew:
    kont = False
    i += 1
    for product in productsOld:
        translator = Translator()
        if product["stok kodu"] == productNew["stok kodu"]:
            kont = True
            break
    if kont == False:
        print(productNew["stok kodu"], " ", productNew["ürün adı"])
        try:
            ekleneceklerList.append({"SKU": productNew["stok kodu"],
                                     "Type": productNew["product type"],
                                     "Name": translator.translate(productNew["ürün adı"]).text,
                                     "Published": productNew["status"],
                                     "Description": "",
                                     "Stock": productNew["stok"],
                                     "Sale Price": productNew["indirimli fiyat"],
                                     "Regular Price": productNew["fiyat"],
                                     "Images": "" if productNew["product type"] == "variation" else
                                     productNew["pic1"]+","+productNew["pic2"] +
                                     ","+productNew["pic3"] +
                                     ","+productNew["pic4"]
                                     if productNew["pic4"] != None else productNew["pic1"]+","+productNew["pic2"] + ","+productNew["pic3"]
                                     if productNew["pic3"] != None else productNew["pic1"]+","+productNew["pic2"]
                                     if productNew["pic2"] != None else productNew["pic1"],
                                     "Attribute 1 name": translator.translate(productNew["att1 name"]).text
                                     if productNew["att1 name"] != None else productNew["att1 name"],
                                     "Attribute 1 value(s)": translator.translate(productNew["att1 val"]).text
                                     if productNew["att1 val"] != None and productNew["att1 val"] != [] else productNew["att1 val"],
                                     "Attribute 2 name": translator.translate(productNew["att2 name"]).text
                                     if productNew["att2 name"] != None else productNew["att2 name"],
                                     "Attribute 2 value(s)": translator.translate(productNew["att2 val"]).text
                                     if productNew["att2 val"] != None and productNew["att2 val"] != [] else productNew["att2 val"],
                                     "Categories": "All products, All products > Clothing"
                                     if productNew["ana kategori"] == "Takımlar" else "All products, All products > Clothing, All products > Clothing > Dresses "
                                     if productNew["alt kategori"] == "Elbise" else "All products, All products > Clothing, All products > Clothing > Tops > Shirts &amp; Blouses, All products > Clothing > Tops"
                                     if productNew["alt kategori"] == "Gömlek" or productNew["alt kategori"] == "Bluz" or productNew["alt kategori"] == "Kazak" else "All products, All products > Clothing, All products > Clothing > Coats"
                                     if productNew["alt kategori"] == "Palto / Kaban" else "All products, All products > Clothing > Tops > Cardigans, All products > Clothing, All products > Clothing > Tops"
                                     if productNew["alt kategori"] == "Hırka" else "All products, All products > Clothing, All products > Clothing > Tops > T-shirts, All products > Clothing > Tops"
                                     if productNew["alt kategori"] == "Tişört" else "All products, All products > Clothing, All products > Clothing > Tops > Jackets, All products > Clothing > Tops"
                                     if productNew["alt kategori"] == "Ceket" else "All products, All products > Clothing, All products > Clothing > Tops > Jumpers, All products > Clothing > Tops"
                                     if productNew["alt kategori"] == "Sweat" else "All products, All products > Clothing, All products > Clothing > Trousers"
                                     if productNew["alt kategori"] == "Pantolon" else "All products, All products > Clothing, All products > Clothing > Skirts"
                                     if productNew["alt kategori"] == "Etek" else "All products, All products > Clothing, All products > Clothing > Leggings"
                                     if productNew["alt kategori"] == "Tayt" else"All products, All products > Clothing, All products > Clothing > Jeans"
                                     if productNew["alt kategori"] == "Jean Pantolon" else "All products, All products > Clothing",
                                     "Is featured?": "0",
                                     "Visibility in catalogue": "visible",
                                     "Tax status": "taxable",
                                     "Tax class": "parent"
                                     if productNew["product type"] == "varitaion" else "",
                                     "In stock?": "1"
                                     if int(productNew["stok"]) > 0 else "0",
                                     "Backorders allowed?": "0",
                                     "Sold individually?": "0",
                                     "Allow customer reviews?": "1",
                                     "Parent": productNew["parent"],
                                     "Position": "0",
                                     "Attribute 1 visible": "1"
                                     if productNew["product type"] == "variable" else "",
                                     "Attribute 2 visible": "1"
                                     if productNew["product type"] == "variable" and len(productNew["att2 name"]) != 0 else ""
                                     })
        except:
            ekleneceklerList.append({"SKU": productNew["stok kodu"],
                                     "Type": productNew["product type"],
                                     "Name": productNew["ürün adı"],
                                     "Published": productNew["status"],
                                     "Description": "",
                                     "Stock": productNew["stok"],
                                     "Sale Price": productNew["indirimli fiyat"]
                                     if productNew["indirimli fiyat"] != 0 and productNew["product type"] != "variable" else "",
                                     "Regular Price": productNew["fiyat"]
                                     if productNew["product type"] != "variable" else "",
                                     "Images": "" if productNew["product type"] == "variation" else
                                     productNew["pic1"]+","+productNew["pic2"] +
                                     ","+productNew["pic3"] +
                                     ","+productNew["pic4"]
                                     if productNew["pic4"] != None else productNew["pic1"]+","+productNew["pic2"] + ","+productNew["pic3"]
                                     if productNew["pic3"] != None else productNew["pic1"]+","+productNew["pic2"]
                                     if productNew["pic2"] != None else productNew["pic1"],
                                     "Attribute 1 name": productNew["att1 name"],
                                     "Attribute 1 value(s)": productNew["att1 val"],
                                     "Attribute 2 name": productNew["att2 name"],
                                     "Attribute 2 value(s)": productNew["att2 val"],
                                     "Categories": "All products, All products > Clothing"
                                     if productNew["ana kategori"] == "Takımlar" else "All products, All products > Clothing, All products > Clothing > Dresses "
                                     if productNew["alt kategori"] == "Elbise" else "All products, All products > Clothing, All products > Clothing > Tops > Shirts &amp; Blouses, All products > Clothing > Tops"
                                     if productNew["alt kategori"] == "Gömlek" or productNew["alt kategori"] == "Bluz" or productNew["alt kategori"] == "Kazak" else "All products, All products > Clothing, All products > Clothing > Coats"
                                     if productNew["alt kategori"] == "Palto / Kaban" else "All products, All products > Clothing > Tops > Cardigans, All products > Clothing, All products > Clothing > Tops"
                                     if productNew["alt kategori"] == "Hırka" else "All products, All products > Clothing, All products > Clothing > Tops > T-shirts, All products > Clothing > Tops"
                                     if productNew["alt kategori"] == "Tişört" else "All products, All products > Clothing, All products > Clothing > Tops > Jackets, All products > Clothing > Tops"
                                     if productNew["alt kategori"] == "Ceket" else "All products, All products > Clothing, All products > Clothing > Tops > Jumpers, All products > Clothing > Tops"
                                     if productNew["alt kategori"] == "Sweat" else "All products, All products > Clothing, All products > Clothing > Trousers"
                                     if productNew["alt kategori"] == "Pantolon" else "All products, All products > Clothing, All products > Clothing > Skirts"
                                     if productNew["alt kategori"] == "Etek" else "All products, All products > Clothing, All products > Clothing > Leggings"
                                     if productNew["alt kategori"] == "Tayt" else"All products, All products > Clothing, All products > Clothing > Jeans"
                                     if productNew["alt kategori"] == "Jean Pantolon" else "All products, All products > Clothing",
                                     "Is featured?": "0",
                                     "Visibility in catalogue": "visible",
                                     "Tax status": "taxable",
                                     "Tax class": "parent"
                                     if productNew["product type"] == "varitaion" else "",
                                     "In stock?": "1"
                                     if int(productNew["stok"]) > 0 else "0",
                                     "Backorders allowed?": "0",
                                     "Sold individually?": "0",
                                     "Allow customer reviews?": "1",
                                     "Parent": productNew["parent"],
                                     "Position": "0",
                                     "Attribute 1 visible": "1"
                                     if productNew["product type"] == "variable" else "",
                                     "Attribute 2 visible": "1"
                                     if productNew["product type"] == "variable" and len(productNew["att2 name"]) != 0 else ""
                                     })
removeProducts(cikarilacaklarList)
addproducts2dataset(ekleneceklerList)
salepricechange(indirimegirenlerList + indirimibitenlerList)
regularpricechange(fiyatidegisenlerList)
stockchange(stoguartanlarList + stoguazalanlarList)
statuschange(statusdegisenlerlist)
# dünkü xmli archive taşı
# shutil.move('index_old.xml', 'xml_archive/stock_' + today + '.xml')
# bugünkü xmli işlenmiş xml dosyası yap
# os.rename('index.xml', 'index_old.xml')
