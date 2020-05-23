import xml.etree.ElementTree as ET
import translator
from googletrans import Translator
import urllib.request
import os
import shutil
import datetime

#dosya adı için bugünün stringini oluştur
##today= str(datetime.datetime.now().day) + str(datetime.datetime.now().month) + str(datetime.datetime.now().year)

#bugünkü xmli indir
##url = 'http://www.modacelikler.com/index.php?do=catalog/output&pCode=2134241870'
##urllib.request.urlretrieve(url, 'index.xml')

#dünkü xmli aç
tree = ET.parse('index_old.xml')
root = tree.getroot()
#bugünkü xmli aç
treeNew = ET.parse('index.xml')
rootNew = treeNew.getroot()

def myFunc(e):
  return e['stok kodu']

products = []

for child in root:
    try:
        products.append( {"stok kodu" : child[0].text,
                    "ürün adı" : child[1].text,
                    "stok" : int(child[17].text),
                    "status" : child[2].text,
                    "fiyat" : float(child[10].text),
                    "vergi" : int(child[15].text),
                    "indirim" : child[27].text,
                    "indirimli fiyat" : float(child[26].text),
                    "product type" : child[28][0].tag })
    except IndexError:
        products.append( {"stok kodu" : child[0].text,
                    "ürün adı" : child[1].text,
                    "stok" : int(child[17].text),
                    "status" : child[2].text,
                    "fiyat" : float(child[10].text),
                    "vergi" : int(child[15].text),
                    "indirim" : child[27].text,
                    "indirimli fiyat" : float(child[26].text),
                    "product type" : "simple" })         
products.sort(key=myFunc)

print(*products, sep='\n')

productsNew = []
for childNew in rootNew:
    try:
        productsNew.append( {"stok kodu" : childNew[0].text,
                        "ürün adı" : childNew[1].text,
                        "stok" : int(childNew[17].text),
                        "status" : childNew[2].text,
                        "fiyat" : float(childNew[10].text),
                        "vergi" : int(childNew[15].text),
                        "indirim" : childNew[27].text,
                        "indirimli fiyat" : float(childNew[26].text),
                        "product type" : childNew[28][0].tag }) 
    except IndexError:
        productsNew.append( {"stok kodu" : childNew[0].text,
                        "ürün adı" : childNew[1].text,
                        "stok" : int(childNew[17].text),
                        "status" : childNew[2].text,
                        "fiyat" : float(childNew[10].text),
                        "vergi" : int(childNew[15].text),
                        "indirim" : childNew[27].text,
                        "indirimli fiyat" : float(childNew[26].text),
                        "product type" : "simple" }) 
productsNew.sort(key=myFunc)
#print(*productsNew, sep='\n')
i=0
cikarilacaklarList = []
indirimegirenlerList = []
indirimibitenlerList = []
fiyatidegisenlerList = []
stoguazalanlarList = []
stoguartanlarList = []

for product in products:
    kont=False
    kont1=False
    kont2= False
    kont3 =False
    i += 1
    for productNew in productsNew:
        if product["stok kodu"] == productNew["stok kodu"]:
            kont=True
            if product["indirimli fiyat"] == productNew["indirimli fiyat"]:
                kont1=True
            if kont1==False:
                if product["indirimli fiyat"] > productNew["indirimli fiyat"] or product["indirimli fiyat"] == 0.0:
                    indirimegirenlerList.append({"stok kodu" : product["stok kodu"],
                                                "eski fiyat" : product["indirimli fiyat"],
                                                "yeni fiyat" : productNew["indirimli fiyat"]})
                else:
                    indirimibitenlerList.append({"stok kodu" : product["stok kodu"],
                                                "eski fiyat" : product["indirimli fiyat"],
                                                "yeni fiyat" : productNew["indirimli fiyat"]}) 
            if product["fiyat"] == productNew["fiyat"]:
                kont2=True         
            if kont2==False:
                fiyatidegisenlerList.append({"stok kodu" : product["stok kodu"],
                                             "Eski fiyat": product["fiyat"],
                                             "Yeni fiyat": productNew["fiyat"]})
            if product["stok"] == productNew["stok"]:
                kont3=True         
            if kont3==False:
                if product["stok"] > productNew["stok"]:
                    stoguazalanlarList.append({"stok kodu" : product["stok kodu"],
                                                "eski stok" : product["stok"],
                                                "yeni stok" : productNew["stok"]})
                else:
                    stoguartanlarList.append({"stok kodu" : product["stok kodu"],
                                                "eski stok" : product["stok"],
                                                "yeni stok" : productNew["stok"]}) 
            break
    if kont==False:
        cikarilacaklarList.append({"stok kodu" : product["stok kodu"]})

i=0
ekleneceklerList = []
for productNew in productsNew:
    kont=False
    i += 1
    for product in products:
        if product["stok kodu"] == productNew["stok kodu"]:
            kont=True
#            print("ok " + str(i))
            break
    if kont==False:
        ekleneceklerList.append({"stok kodu" : productNew["stok kodu"]})
print('\033[1m' + "Çıkarılacak ürünler:" + '\033[0m')
print(*cikarilacaklarList, sep='\n')
print('\033[1m' + "Eklenecek ürünler:" + '\033[0m')
print(*ekleneceklerList, sep='\n')
print('\033[1m' + "indirime girenler:"+ '\033[0m')
print(*indirimegirenlerList, sep='\n')
print('\033[1m' + "indirimi bitenler:"+ '\033[0m')
print(*indirimibitenlerList, sep='\n')
print('\033[1m' + "fiyatı değişenler:"+ '\033[0m')
print(*fiyatidegisenlerList, sep='\n')
print('\033[1m' + "stogu azalanlar:"+ '\033[0m')
print(*stoguazalanlarList, sep='\n')
print('\033[1m' + "stogu artanlar:"+ '\033[0m')
print(*stoguartanlarList, sep='\n')
#dünkü xmli archive taşı
##shutil.move('index_old.xml', 'xml_archive/stock_' + today + '.xml')
#bugünkü xmli işlenmiş xml dosyası yap
##os.rename('index.xml', 'index_old.xml')