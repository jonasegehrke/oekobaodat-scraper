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
        



def get_LCIA(xml):
    with open(xml,"r", errors='ignore') as fp:
        soup = BeautifulSoup(fp, 'xml')

    stages = []
    proceed = False
    all_stage_enum = ["A1-A3","A1","A2","A3","A4","A5","B1","B2","B3","B4","B5","B6","B7","C1","C2","C3","C4","D"]

    for baseName in soup.find_all('baseName'):
        if baseName["xml:lang"] == "en":
            proceed = True

    if proceed == False:
        return
    
    all_lcia = soup.find_all('LCIAResult')
    all_exchanges = soup.find_all('exchange')
    

    all_datapoints = all_lcia + all_exchanges

    for index, stage_enum in enumerate(all_stage_enum):
        stage_result = {}
        stage_result['stageType'] = index
        for datapoint in all_datapoints:
            if(datapoint.name == "LCIAResult"):
                key_elements = datapoint.find("referenceToLCIAMethodDataSet").find_all("common:shortDescription")
            if(datapoint.name == "exchange"):
                key_elements = datapoint.find("referenceToFlowDataSet").find_all("common:shortDescription")
            currentKey = ''
            for key_element in key_elements:
                if '(' in key_element.text and ')' in key_element.text and key_element.get("xml:lang") == "en":
                    start = key_element.text.rfind('(') + 1
                    end = key_element.text.rfind(')')
                    currentKey = key_element.text[start:end]
            if len(currentKey) <= 0:
                continue
            all_amounts = datapoint.find_all('epd:amount')
            if "measures" not in stage_result:
                stage_result["measures"] = {}
            for amount in all_amounts:
                if stage_enum == amount['epd:module']:
                    stage_result["measures"][currentKey] = amount.text
                    break
                else:
                    stage_result["measures"][currentKey] = None
            currentKey = ''
        stages.append(stage_result)    
    return stages
    




def runSingle(file):
    results = []
    FOLDER_PATH = r'C:\\Users\\jonas\\Capacit\\abc-carbon\\oekobaodat-scraper\\xml'
    FILE_NAME = file
    xml = os.path.join(FOLDER_PATH, FILE_NAME)
    result = get_LCIA(xml)
    results.append(result)
    return results

def runAll():
    results = []
    FOLDER_PATH = r'C:\\Users\\jonas\\Capacit\\abc-carbon\\oekobaodat-scraper\\xml'
    all_xml = os.listdir(FOLDER_PATH)
    for FILE_NAME in all_xml:
        xml = os.path.join(FOLDER_PATH, FILE_NAME)
        result = get_LCIA(xml)
        if result != None:
            results.append(result)
    return results

result = runSingle("9099dfdd-22a6-4dee-9b60-0e90701e9d99.xml")

#result = runAll()


final = json.dumps(result, indent=2)
with open("test-result.json", "w") as outfile:
    outfile.write(final) 



