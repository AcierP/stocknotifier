import requests
import threading
import dhooks
import time
import random
from itertools import cycle

with open('proxies.txt','r+', encoding='utf-8') as f:
	ProxyPool = cycle(f.read().splitlines())

productstosend = []
alreadychecked = []

newegglinks = [
    "https://www.newegg.com/p/pl?d=rtx+3080&N=100007709%20601357247",
    "https://www.newegg.com/zotac-geforce-rtx-3080-zt-t30800j-10p/p/N82E16814500504?Description=rtx%203080&cm_re=rtx_3080-_-14-500-504-_-Product",
    "https://www.newegg.com/gigabyte-geforce-rtx-3080-gv-n3080aorus-m-10gd/p/N82E16814932336?Description=rtx%203080&cm_re=rtx_3080-_-14-932-336-_-Product",
    "https://www.newegg.com/evga-geforce-rtx-3080-10g-p5-3897-kr/p/N82E16814487518?Description=rtx%203080&cm_re=rtx_3080-_-14-487-518-_-Product&quicklink=true",
    "https://www.newegg.com/asus-geforce-rtx-3080-tuf-rtx3080-o10g-gaming/p/N82E16814126452?Description=rtx%203080&cm_re=rtx_3080-_-14-126-452-_-Product",
    "https://www.newegg.com/zotac-geforce-rtx-3080-zt-a30800d-10p/p/N82E16814500502?Description=rtx%203080&cm_re=rtx_3080-_-14-500-502-_-Product",
    "https://www.newegg.com/gigabyte-geforce-rtx-3080-gv-n3080gaming-oc-10gd/p/N82E16814932329?Description=rtx%203080&cm_re=rtx_3080-_-14-932-329-_-Product",
    "https://www.newegg.com/msi-geforce-rtx-3080-rtx-3080-gaming-x-trio-10g/p/N82E16814137597?Description=rtx%203080&cm_re=rtx_3080-_-14-137-597-_-Product",
    "https://www.newegg.com/asus-geforce-rtx-3080-rog-strix-rtx3080-o10g-gaming/p/N82E16814126457?Description=rtx%203080&cm_re=rtx_3080-_-14-126-457-_-Product",
    "https://www.newegg.com/gigabyte-geforce-rtx-3080-gv-n3080vision-oc-10gd/p/N82E16814932337?Description=rtx%203080&cm_re=rtx_3080-_-14-932-337-_-Product",
    "https://www.newegg.com/msi-geforce-rtx-3080-rtx-3080-ventus-3x-10g-oc/p/N82E16814137598?Description=rtx%203080&cm_re=rtx_3080-_-14-137-598-_-Product",
    "https://www.newegg.com/pny-geforce-rtx-3080-vcg308010tfxppb/p/N82E16814133809?Description=rtx%203080&cm_re=rtx_3080-_-14-133-809-_-Product",
    "https://www.newegg.com/msi-geforce-rtx-3070-rtx-3070-gaming-x-trio/p/N82E16814137603?Description=3070&cm_re=3070-_-14-137-603-_-Product",
    "https://www.newegg.com/gigabyte-geforce-rtx-3070-gv-n3070aorus-m-8gd/p/N82E16814932359?Description=3070&cm_re=3070-_-14-932-359-_-Product",
    "https://www.newegg.com/gigabyte-geforce-rtx-3070-gv-n3070gaming-oc-8gd/p/N82E16814932342?Description=3070&cm_re=3070-_-14-932-342-_-Product",
    "https://www.newegg.com/msi-geforce-rtx-3070-rtx-3070-ventus-2x-oc/p/N82E16814137602?Description=3070&cm_re=3070-_-14-137-602-_-Product",
    "https://www.newegg.com/Product/ComboDealDetails?ItemList=Combo.4204117",
    "https://www.newegg.com/Product/ComboDealDetails?ItemList=Combo.4190539",
    "https://www.newegg.com/Product/ComboDealDetails?ItemList=Combo.4204103",   
    "https://www.newegg.com/Product/ComboDealDetails?ItemList=Combo.4190541",
    "https://www.newegg.com/Product/ComboDealDetails?ItemList=Combo.4190581",
    "https://www.newegg.com/evga-geforce-rtx-3090-24g-p5-3987-kr/p/N82E16814487526?Description=rtx%203090&cm_re=rtx_3090-_-14-487-526-_-Product&quicklink=true",
    "https://www.newegg.com/Product/ComboDealDetails?ItemList=Combo.4205009",
    "https://www.newegg.com/Product/ComboDealDetails?ItemList=Combo.4205017",
    "https://www.newegg.com/Product/ComboDealDetails?ItemList=Combo.4205005"
]

hook = dhooks.Webhook('https://discord.com/api/webhooks/775830552641011722/WF4q3n26Cti7OqWyPRkJJYzfmTj-EdhflZcH3olC9E19vApHNFOjNh1xJy6kDt8FcUkx')

def checkNewEgg(proxy):
    while True:
        req = requests.Session()
        tocheck = random.choice(newegglinks)
        r = req.get(tocheck, proxies=proxy)
        if "Add to cart" in r.text:
            if tocheck not in alreadychecked:
                alreadychecked.append(tocheck)
                productstosend.append(tocheck)
def sendhook():
    while True:
        for item in productstosend:
            hook.send(f"@everyone")
            
            embed = dhooks.Embed(
                description=f'A product was just restocked!\n\n{item}',
                color=0x5CDBF0,
                timestamp='now'
            )
            embed.set_footer(text='Product Notifier https://discord.gg/acier')

            hook.send(embed=embed)
            productstosend.remove(item)
            alreadychecked.remove(item)

threading.Thread(target=sendhook, args=[]).start()
for _ in range(10):
    proxy = {
        "https": "https://" + next(ProxyPool)
    }
    threading.Thread(target=checkNewEgg, args=[proxy]).start()