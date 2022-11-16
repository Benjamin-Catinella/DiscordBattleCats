import json
import requests
from bs4 import BeautifulSoup
from lxml import html
import os
os.chdir("webscraper")
IMAGE_PATH = "images/"
URL = "https://battle-cats.fandom.com/wiki/Cat_Release_Order"

HEADERS = ({'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"})
XPATH = "/html/body/div[4]/div[3]/div[2]/main/div[3]/div[2]/div[1]/table[1]/tbody"
AXPATH = "//td[3]/a"
"/tr[1]/td[2]"
RARITYXPATH = "//td[1]/a"

RarityMap = {
    "EX" : "special",
    "N"  : "common",
    "RR" : "rare",
    "SR" : "super_rare",
    "UR" : "uber_rare",
    "LR" : "legendary_rare"
}

def get_image(cat_url, filename):
    if os.path.exists(f"images/{filename}") : 
        return
    XPATH_LIST = [
        "/html/body/div[4]/div[3]/div[2]/main/div[3]/div[2]/div[1]/table[1]/tbody/tr[3]/td/div/div[2]/div/div/a/img",
        "/html/body/div[4]/div[3]/div[2]/main/div[3]/div[2]/div[1]/table[3]/tbody/tr[3]/td/div/div[2]/div/div/a/img",
        "/html/body/div[4]/div[3]/div[2]/main/div[3]/div[2]/div[1]/table[2]/tbody/tr[3]/td/div/div[2]/div/div/a/img",
        "/html/body/div[4]/div[3]/div[2]/main/div[3]/div[2]/div[1]/table[4]/tbody/tr[3]/td/div/div[2]/div/div/a/img",
        "/html/body/div[4]/div[3]/div[2]/main/div[3]/div[2]/div[1]/table[5]/tbody/tr[3]/td/div/div[2]/div/div/a/img"
    ]
    # Requesting the web page
    htmlreq = requests.get(cat_url, headers=HEADERS)
    tree : html.HtmlElement = html.fromstring(htmlreq.content)

    # Applying XPATH
    for xpath in XPATH_LIST:
        try:
            tr_list : list[html.HtmlElement] = list(tree.xpath(xpath))
            img_url = tr_list[0].attrib["src"]
            img_data = requests.get(img_url).content

            break
        except Exception as e:
            pass
            
    else:
        print(f"Error while gathering data from {cat_url}")
        return
    
    with open(f"images/{filename}", 'wb') as handler:
        print(f"Writing data at {filename}")
        handler.write(img_data)


htmlreq = requests.get(URL, headers=HEADERS)
tree : html.HtmlElement = html.fromstring(htmlreq.content)
tr_list : list[html.HtmlElement] = list(tree.xpath(XPATH)[0])
# Get all <tr>
##htmlreq = open("test.html", "r").read()
##tree = html.fromstring(htmlreq)
##print(tree.xpath("/html/body/table/tbody/tr[2]/td[2]")[0].text_content())

cats = {}
# get <a> from each td inside the TRs
for i,tr in enumerate(tr_list): 
    if(i <=4): continue
    a : html.HtmlElement = tr[2][0]
    td : html.HtmlElement = tr[1]
    #<td data-sort-value="2">EX</td>
    try:
        rarity = RarityMap[td.text_content().replace("\n", "")]
    except:
        rarity = RarityMap["RR"]
    #<a href="/wiki/The_Cat_God_(Special_Cat)" title="The Cat God (Special Cat)">The Cat God</a>
    cat_name : str = a.text_content().replace("\n", "")

    image = cat_name.replace(" ", "_").replace("\n", "") +".webp"

    cats[cat_name] = {
        "name"   : cat_name,
        "image"  : image,
        "rarity" : rarity
    }
    href = "https://battle-cats.fandom.com" + a.attrib["href"]
    try: 
        get_image(href, image)
    except Exception as e:
        print(e)





# Save the cats as JSON
# with open("output.json", "w") as f:
#     f.write(json.dumps(cats,indent=4))
    