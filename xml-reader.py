from bs4 import BeautifulSoup
import os, io
import json





def get_data(xml):
    with open(xml) as fp:
        soup = BeautifulSoup(fp, 'xml')

    result = {}
    proceed = False
    for baseName in soup.find_all('baseName'):
        if baseName["xml:lang"] == "en":
            result["Title"] = baseName.text
            proceed = True

    if proceed == False:
        return
    
    
    

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
    return result


results = []

FOLDER_PATH = r'C:\\Users\\jonas\\capacit\\oekobaodat-scraper\\xml'

all_xml = os.listdir(FOLDER_PATH)
for FILE_NAME in all_xml:
    xml = os.path.join(FOLDER_PATH, FILE_NAME)
    result = get_data(xml)
    if result != None:
        results.append(result)


final = json.dumps(results, indent=2)
with open("result.json", "w") as outfile:
    outfile.write(final)

