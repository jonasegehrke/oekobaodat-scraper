from bs4 import BeautifulSoup
import os, io
import json
import re



def get_data(xml):
    with open(xml,"r", errors='ignore') as fp:
        soup = BeautifulSoup(fp, 'xml')
        

    result = {}
    proceed = False
    currentKey = ""
    unit = ""
    for baseName in soup.find_all('baseName'):
        if baseName["xml:lang"] == "en":
            result["Title"] = baseName.text
            proceed = True

    if proceed == False:
        return

    all_lcia = soup.find_all('LCIAResult')
    for lcia in all_lcia:
        keys = lcia.find("referenceToLCIAMethodDataSet").find_all("common:shortDescription")
        units = lcia.find("epd:referenceToUnitGroupDataSet").find_all("common:shortDescription")
        for key in keys:
            if '(' in key.text and ')' in key.text and key.get("xml:lang") == "en":
                start = key.text.rfind('(') + 1
                end = key.text.rfind(')')
                currentKey = key.text[start:end]
            elif key.get("xml:lang") == "en":
                print(key)
        for u in units:
            if u.get("xml:lang") == "en":
                unit = u.text
        if len(currentKey) > 0 and len(unit) > 0:
            values = lcia.find_all('epd:amount')
            result[currentKey] = {}
            result[currentKey]["Unit"] = unit
                
            for value in values: 
                result[currentKey][value['epd:module']] = value.text
            currentKey = ""
            unit = ""
    
    all_exhanges = soup.find_all('exchange')
    for exchange in all_exhanges:
        if exchange.find('epd:amount'):
            keys = exchange.find("referenceToFlowDataSet").find_all('common:shortDescription')
            units = exchange.find("epd:referenceToUnitGroupDataSet").find_all('common:shortDescription')
            for key in keys:
                if '(' in key.text and ')' in key.text and key.get("xml:lang") == "en":
                    start = key.text.rfind('(') + 1
                    end = key.text.rfind(')')
                    currentKey = key.text[start:end]
                elif key.get("xml:lang") == "en":
                    print(key)
            for u in units:
                if u.get("xml:lang") == "en":
                    unit = u.text
            if len(currentKey) > 0 and len(unit) > 0:
                values = exchange.find_all('epd:amount')
                result[currentKey] = {}
                result[currentKey]["Unit"] = unit
                for value in values:
                    result[currentKey][value['epd:module']] = value.text
                currentKey = ""
                unit = ""
    return result
        


def runSingle(file):
    results = []
    FOLDER_PATH = r'C:\\Users\\jonas\\Capacit\\abc-carbon\\oekobaodat-scraper\\xml'
    FILE_NAME = file
    xml = os.path.join(FOLDER_PATH, FILE_NAME)
    result = get_data(xml)
    results.append(result)
    return results

def runAll():
    results = []
    FOLDER_PATH = r'C:\\Users\\jonas\\Capacit\\abc-carbon\\oekobaodat-scraper\\xml'
    all_xml = os.listdir(FOLDER_PATH)
    for FILE_NAME in all_xml:
        xml = os.path.join(FOLDER_PATH, FILE_NAME)
        result = get_data(xml)
        if result != None:
            results.append(result)
    return results

#result = runSingle("fc442d0a-fbc4-4304-ace8-24304756e2df.xml")


result = runAll()

print(len(result))

final = json.dumps(result, indent=2)
with open("result.json", "w") as outfile:
    outfile.write(final) 



