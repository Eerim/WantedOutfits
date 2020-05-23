import xml.etree.ElementTree as ET
tree = ET.parse('index_old.xml')
root = tree.getroot()
def myFunc(e):
  return e['stok kodu']

products = []

#for child in root:
#    try:
#        products.append( {"stok kodu" : child[0][0].tag })
#    except IndexError:
#        products.append( {"stok kodu" : "simple" })
#products.sort(key=myFunc)
options = []
ekleneceklerList= []
#print(*products, sep='\n')
for variants in root.findall('item'):
    isVariant=False
    for variant in variants.findall('variants'):
        for subbranks in variant.findall("variant"):
            isVariant=True
            sku = subbranks.find('vStockCode').text
            stok = subbranks.find('vStockAmount').text
            price = subbranks.find('vPrice1').text
            for opts in subbranks.findall("options"):
                for opttions in opts.findall("option"):
                    options.append((opttions.find("variantName").text,opttions.find("variantValue").text))
                if len(options) == 1:
                    productsNew.append({"stok kodu" : sku,
                        "ürün adı" : variants[1].text,
                        "stok" : int(stok),
                        "status" : variants[2].text,
                        "fiyat" : round(float(price)+float(price)*int(variants[15].text)/100,2),
                        "vergi" : "",
                        "indirim" : "",
                        "indirimli fiyat" : "",
                        "product type" : "variation",
                        "parent" : sku[:sku.find("_")],
                        "att1 name" : options[0][0],
                        "att1 val" : options[0][1]})
                else:
                    productsNew.append( {"stok kodu" : sku,
                        "ürün adı" : variants[1].text,
                        "stok" : int(stok),
                        "status" : variants[2].text,
                        "fiyat" : float(price),
                        "vergi" : "",
                        "indirim" : "",
                        "indirimli fiyat" : "",
                        "product type" : "variation",
                        "parent" : sku[:sku.find("_")],
                        "att1 name" : options[0][0],
                        "att1 val" : options[0][1],
                        "att2 name" : options[1][0],
                        "att2 val" : options[1][1]})                            
                options = []
    if isVariant == False:
        ekleneceklerList.append({"stok kodu" : variants[0].text,
                        "ürün adı" : variants[1].text,
                        "stok" : variants[17].text,
                        "status" : variants[2].text,
                        "fiyat" : float(price),
                        "vergi" : "",
                        "indirim" : "",
                        "indirimli fiyat" : "",
                        "product type" : "variation",
                        "parent" : sku[:sku.find("_")],
                        "att1 name" : options[0][0],
                        "att1 val" : options[0][1],
                        "att2 name" : options[1][0],
                        "att2 val" : options[1][1]})
print(*ekleneceklerList, sep="\n")

        
       