import requests
b=["svo","London","Cherepovets"]
for bb in b:
    aa="https://wttr.in/"+bb+"?m?3?n"
    a=requests.get(aa,headers={"Accept-Language":"ru"})
    print(a.text)












# https://vk.com/andreypiguzov
