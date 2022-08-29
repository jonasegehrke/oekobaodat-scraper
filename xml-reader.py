from bs4 import BeautifulSoup
import os, io
import json

FOLDER_PATH = r'C:\\Users\\jonas\\capacit\\oekobaodat-scraper'
#FILE_NAME = 'fa9f6670-3170-4597-92ab-a2fdec7f1451.xml'
FILE_NAME = 'ff9336ea-fb7f-4299-8a40-5e9a28538c85.xml'
xml = os.path.join(FOLDER_PATH, FILE_NAME)

with open(xml) as fp:
    soup = BeautifulSoup(fp, 'xml')



result = {}
result["Title"] = soup.baseName.text

allDesc = soup.find_all('shortDescription')
for desc in allDesc:
    if "GWP" in desc.text:
        if desc['xml:lang'] == "en":
            parent = desc.find_parent("LCIAResult")
            values = parent.find_all('epd:amount')
            parent_descriptions = parent.find_all('shortDescription')
            for pd in parent_descriptions:
                if 'xmlns:epd' in pd: continue
                if pd['xml:lang'] == "en":
                    unit = pd.text
            if len(unit) > 0:
                result["GWP"] = {}
                result["GWP"]["Unit"] = unit
                for value in values:
                    result["GWP"][value['epd:module']] = value.text


print(result)

final = json.dumps(result, indent=2)
with open("result.json", "w") as outfile:
    outfile.write(final)

