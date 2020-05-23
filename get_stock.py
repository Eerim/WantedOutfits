import csv
import sys
from htmldom import htmldom
pages1 = []

with open('web_pages_from_modacelikler.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
            pages1.append(row[0])
            line_count += 1
    print(f'Processed {line_count} pages.')
for product_page in pages1:
    print(product_page)
    try:
        dom = htmldom.HtmlDom(product_page).createDom()
        a = dom.find( "option" )
        for option in a:
            print(option.text())
    except:
        print("file not found Gülçin!!")