import csv
with open("deneme.csv", "r") as f:
    reader = csv.reader(f)
    for header in reader:
        break
myDict = {"SKU": "345", "Name": "hebebheh"}
# add row to CSV file
with open("deneme.csv", "a", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writerow(myDict)
