import requests
import urllib.request
import time
import csv
import sys
import translator
from termcolor import colored
from bs4 import BeautifulSoup
from googletrans import Translator
pages1 = []
with open('web_pages_from_mineralist.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
            pages1.append(row[0])
            line_count += 1
    print(f'Processed {line_count} pages.')
with open('results.csv', mode='w', newline="") as results_file:
        results_writer = csv.writer(results_file, delimiter=",")
        results_writer.writerow(["ID", "Type", "SKU","Name","Published","Is featured?","Visibility in catalogue","Short description","Description", "Date sale price starts","Date sale price ends","Tax status","Tax class","In stock?", "Stock", "Low stock amount","Backorders allowed?","Sold individually?","Weight (kg)", "Length (cm)", "Width (cm)", "Height (cm)", "Allow customer reviews?", "Purchase note", "Sale price", "Regular price", "Categories", "Tags", "Shipping class", "Images", "Download limit", "Download expiry days", "Parent", "Grouped products", "Upsells", "Cross-sells", "External URL", "Button text","Pozition" ])
        prod_id=103000
        for product_page in pages1:
                print(product_page)
                url=product_page
                response = requests.get(url)
                soup =BeautifulSoup(response.text, "html.parser")
                product_name=soup.h1
                sale_price=soup.find("span", attrs={"class":"product-price"})
                regular_price=soup.find("span", attrs={"class":"product-price-not-discounted"})
                tag3=soup.find("div", id="productDetailTab")
                images=[]
                for link in soup.findAll("img"):
                        if link.get('src').endswith("-O.jpg") :
                                images.append(str(link.get('src')))
                definition=""
                for string in tag3.strings:
                        if repr(string) != "'\n'" :
                                cropped=repr(string).replace('\'','')
                                cropped=cropped.replace('\\n','')
                                cropped=cropped.replace('\\u200b','')
                                cropped=cropped.replace('\\xa0','')
                                if cropped.startswith('.'):
                                        cropped=cropped.lstrip('. ')
                                if cropped != "" :
                                        definition += cropped + "."
                translator = Translator()
                definition=definition.replace("..",".")
                definition=definition.replace(".",". ")
                title_en = translator.translate(product_name.string).text
                definition_en = translator.translate(definition).text
                definition_en = definition_en.replace("Audio", "On image")
                sale_price_flt=float(sale_price.next_element.replace(",","."))/7.54+25
                regular_price_flt=float(regular_price.next_element.replace(",","."))/7.54+25
        #        title_en = translate.translate(data=[tag.string],tolang='en',fromlang='tr')
        #        definiton_en = translate.translate(data=[definition],tolang='en',fromlang='tr')                
                if product_page.find("kupe") != -1:
                        cat="All products, All products > Accessories, All products > Accessories > Earrings"
                elif product_page.find("bileklik") != -1 or product_page.find("hollow") != -1 or product_page.find("hallow") != -1 or product_page.find("kunye") != -1 or product_page.find("bilekligi") != -1 or product_page.find("suyolu") != -1 or product_page.find("kelepce") != -1 :
                        cat="All products, All products > Accessories, All products > Accessories > Bracelets"
                elif product_page.find("set") != -1:
                        cat="All products, All products > Accessories, All products > Accessories > Sets"
                elif product_page.find("kolye") != -1 or product_page.find("kolyesi") != -1 or product_page.find("zincir") != -1 or product_page.find("gerdanlik") != -1 :
                        cat="All products, All products > Accessories, All products > Accessories > Necklaces"                        
                elif product_page.find("kolye-ucu") != -1:
                        cat="All products, All products > Accessories, All products > Accessories > Pendants"
                elif product_page.find("yuzuk") != -1 or product_page.find("yuzugu") != -1 or product_page.find("tamtur") != -1 or product_page.find("tektas") != -1 or product_page.find("bestas") != -1 :
                        cat="All products, All products > Accessories, All products > Accessories > Rings"                        
                if len(images) == 1 :
                        results_writer.writerow([prod_id, "simple", "", title_en, "1", "0", "visible", "", definition_en, "", "", "taxable", "", "1", "", "", "0", "0", "","", "", "","1","", round(sale_price_flt,2), round(regular_price_flt,2), cat, "","", images[0], "", "", "", "", "", "", "", "","0"])
                else:
                        results_writer.writerow([prod_id, "simple", "", title_en, "1", "0", "visible", "", definition_en, "", "", "taxable", "", "1", "", "", "0", "0", "","", "", "","1","", round(sale_price_flt,2), round(regular_price_flt,2), cat, "","", images[0] + ", " + images[1], "", "", "", "", "", "", "", "","0"])
                prod_id += 1
#       print("ürün adı:" +tag.string +"\nÜrün indirimli fiyatı: " + tag1.next_element + "\nNormal satış fiyatı:" + tag2.next_element + "\nÜrün açıklaması:\n" + definition +"\n ürün resim linkleri:\n")
#       print(images)
#       translator = Translator()
#       results=translator.translate(tag.string)
#       print(results.text)
#        print(translator.translate(definition).text)

                
#        print(colored("GÜLÇİN işlem tamamdır. (ç)alma işi tamamdır. (ç)almak bizim işimiz. (ç)eviri de tamam. IdaxDigital!!!", "red"))
