str=[]
str.append({"ewr":"qwe","asd":"bb"})
str.append({"ewr":"qqq"})
i=0

for sku_s in str: 
    if sku_s["ewr"] == "qqq":
        str[i]=dict(sku_s, **{'zxc': "vasdalue"})
        try:
            curr = sku_s["asd"] +","
        except KeyError:
            curr=""
        str[i]=dict(sku_s, **{'zxc': "vasdalue", 'asd': curr + "value"})
    i+=1

print(str[0],str[1])
