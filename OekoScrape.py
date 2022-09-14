from bs4 import BeautifulSoup
import os, io
import json
import requests
from deep_translator import GoogleTranslator

url = "https://oekobaudat.de/OEKOBAU.DAT/resource/datastocks/cd2bda71-760b-4fcc-8a0b-3877c10000a8/processes?format=json&search=true&startIndex=0&pageSize=2000&sortOrder=true&sortBy=name&lang=en&langFallback=false&subType=GENERIC_DATASET&dataSource=b497a91f-e14b-4b69-8f28-f50eb1576766&dataSourceMode=NOT&compliance=b00f9ec0-7874-11e3-981f-0800200c9a66"

payload={}
headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.9,da-DK;q=0.8,da;q=0.7',
  'Connection': 'keep-alive',
  'Origin': 'https://www.oekobaudat.de',
  'Referer': 'https://www.oekobaudat.de/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

a1 = requests.request("GET", url, headers=headers, data=payload)
a1 = a1.json()

url = "https://oekobaudat.de/OEKOBAU.DAT/resource/datastocks/cd2bda71-760b-4fcc-8a0b-3877c10000a8/processes?format=json&search=true&startIndex=0&pageSize=2000&sortOrder=true&sortBy=name&lang=en&langFallback=false&subType=GENERIC_DATASET&dataSource=b497a91f-e14b-4b69-8f28-f50eb1576766&dataSourceMode=NOT&compliance=c0016b33-8cf7-415c-ac6e-deba0d21440d"

payload={}
headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.9,da-DK;q=0.8,da;q=0.7',
  'Connection': 'keep-alive',
  'Origin': 'https://www.oekobaudat.de',
  'Referer': 'https://www.oekobaudat.de/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

a2 = requests.request("GET", url, headers=headers, data=payload)
a2 = a2.json()

response = a1["data"] + a2["data"]



"""
notes:
compliance: c0016b33-8cf7-415c-ac6e-deba0d21440d === +A2
compliance: b00f9ec0-7874-11e3-981f-0800200c9a66 === +A1
"""

"""
TODO
owners - thinkstep & sephera = should be the same
get units
search up against lca
"""

def get_meta_data(xml, stages):
    with open(xml,"r", errors='ignore') as fp:
        soup = BeautifulSoup(fp, 'xml')
    proceed = False

    for baseName in soup.find_all('baseName'):
        if baseName["xml:lang"] == "en":
            proceed = True
    if proceed == False:
        return

    subType = soup.find("epd:subType") 
    if subType == None: return
    result = {}
    if subType.text == "generic dataset":
        result["epdInfo"] = {}
        result["declaredUnit"] = {}
        result["link"] = []
        result["additionalSources"] = []
        result["ownerId"] = "8bbaefca-6833-4a6d-93ab-3e8b27a060a7"
        result["custom"] = False
        result["scraped"] = True
        result["generic"] = True
        result["expectedLifespan"] = None

        for baseName in soup.find_all('baseName'):
            if baseName["xml:lang"] == "en":
                #result["shortName"] = GoogleTranslator(source='auto', target='da').translate(baseName.text) #for danish
                result["shortName"] = baseName.text


        product_description = soup.find("common:generalComment")
        if product_description.get("xml:lang") == "en":
            #result["description"] = GoogleTranslator(source='auto', target='da').translate(product_description.text) #for danish
            result["description"] = product_description.text

        uuid = soup.find("dataSetInformation").find("common:UUID").text
        if uuid == "41c5627a-4a1d-4e12-ac62-c1d4f1560fb9":
            return None #remove an old faulty dataset https://oekobaudat.de/OEKOBAU.DAT/datasetdetail/process.xhtml?uuid=41c5627a-4a1d-4e12-ac62-c1d4f1560fb9
        result["link"] = ["https://oekobaudat.de/OEKOBAU.DAT/datasetdetail/process.xhtml?uuid=" + uuid]

        if stages == None: return
        result["stages"] = stages

        if soup.find("time") == None:
            all_valid_until = None
            all_reference_year = None
        else:
            all_valid_until = soup.find("time").find("common:dataSetValidUntil").text
            all_reference_year = soup.find("time").find("common:referenceYear").text
            
        #TODO get these



        # doing
        dataSetId = soup.find("referenceToReferenceFlow").text
        all_exchanges = soup.find_all('exchange')
        for exchange in all_exchanges:
            internalId = exchange.get('dataSetInternalID')
            if internalId == dataSetId:
                result["declaredUnit"]["declaredValue"] = exchange.find("meanAmount").text
                refObjectId = exchange.find("referenceToFlowDataSet").get("refObjectId")
                FOLDER_PATH = r'C:\\Users\\jonas\\vscode\\capacit\\oekobaodat-scraper\\flows'
                FILE_NAME = "{}.xml".format(refObjectId)
                unit_xml = os.path.join(FOLDER_PATH, FILE_NAME)
                with open(unit_xml,"r", errors='ignore') as fp:
                    unitSoup = BeautifulSoup(fp, 'xml')
                    if unitSoup.find("Data"):
                        mass = unitSoup.find("Data").text
                        massUnit = unitSoup.find("Units").get("name")
                        if "/" in massUnit:
                            declaredUnit = massUnit.split("/")[1]
                        else:
                            declaredUnit = massUnit

                        declared_unit_enums = [
                                { "text": "G", "value": 0 },
                                { "text": "KG", "value": 1 },
                                { "text": "TON", "value": 2 },
                                { "text": "M", "value": 3 },
                                { "text": "M^2", "value": 4 },
                                { "text": "M^3", "value": 5 },
                                { "text": "STK", "value": 6 },
                                { "text": "MJ", "value": 7 },
                                { "text": "KGKM", "value": 8 },
                                { "text": "A", "value": 9 },
                                
                            ]
                        mass_unit_enums = [
                                { "text": "KG/M", "value": 0 },
                                { "text": "KG/M^2", "value": 1 },
                                { "text": "KG/M^3", "value": 2 },
                                { "text": "KG/STK", "value": 3 },
                                { "text": "T/M", "value": 4 },
                                { "text": "T/M^2", "value": 5 },
                                { "text": "T/M^3", "value": 6 },
                                { "text": "T/STK", "value": 7 },
                            ]

                        result["declaredUnit"]["mass"] = mass
                        result["declaredUnit"]["declaredUnit"] = next(enum for enum in declared_unit_enums if enum["text"] == declaredUnit.upper())["value"]
                        result["declaredUnit"]["massUnit"] = next(enum for enum in mass_unit_enums if enum["text"] == massUnit.upper())["value"]
                    else:
                        result["declaredUnit"]["mass"] = "1" 
                        result["declaredUnit"]["massUnit"] = None #TODO discuss massunit when its not a mass and not defined
                        if "ENERGY" in unitSoup.find("flowProperty").find("common:shortDescription").text.upper():
                            result["declaredUnit"]["declaredUnit"] = 7
                        elif "LENGTH" in unitSoup.find("flowProperty").find("common:shortDescription").text.upper():
                            result["declaredUnit"]["declaredUnit"] = 3
                        elif "MASS" in unitSoup.find("flowProperty").find("common:shortDescription").text.upper():
                            result["declaredUnit"]["declaredUnit"] = 1
                        elif "AREA" in unitSoup.find("flowProperty").find("common:shortDescription").text.upper():
                            result["declaredUnit"]["declaredUnit"] = 4
                        elif "TIME" in unitSoup.find("flowProperty").find("common:shortDescription").text.upper():
                            result["declaredUnit"]["declaredUnit"] = 9
                        elif "KGKM" in unitSoup.find("flowProperty").find("common:shortDescription").text.upper():
                            result["declaredUnit"]["declaredUnit"] = 8
                        elif "VOLUME" in unitSoup.find("flowProperty").find("common:shortDescription").text.upper():
                            result["declaredUnit"]["declaredUnit"] = 5
                        else:
                            print(unitSoup.find("flowProperty").find("common:shortDescription").text)
                            print("UNKNOWN:" , uuid)


            


        result["epdInfo"]["issuedAt"] = all_reference_year
        result["epdInfo"]["validTo"] = all_valid_until
        result["epdInfo"]["epdProductIndustryType"] = None #usikkerhedsfaktor 1,3
        

        resource = next(element for element in response if element["uuid"] == uuid)
        translated = GoogleTranslator(source='auto', target='da').translate(resource["classific"]).replace(" ", "")
        result["tags"] = translated.split("/")

        compliance = soup.find("common:referenceToComplianceSystem").get("refObjectId")
        if compliance == "b00f9ec0-7874-11e3-981f-0800200c9a66":
            result["epdInfo"]["epdSpecificationForm"] = 0
        elif compliance == "c0016b33-8cf7-415c-ac6e-deba0d21440d":
            result["epdInfo"]["epdSpecificationForm"] = 1
    else:
        return None
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
        stage_result['stageStatus'] = 2
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
    FOLDER_PATH = r'C:\\Users\\jonas\\vscode\\capacit\\oekobaodat-scraper\\xml'
    FILE_NAME = file
    xml = os.path.join(FOLDER_PATH, FILE_NAME)
    stages = get_LCIA(xml)
    result = get_meta_data(xml, stages)
    results.append(result)
    if result != None:
        return results
    return None

def runAll():
    results = []
    FOLDER_PATH = r'C:\\Users\\jonas\\vscode\\capacit\\oekobaodat-scraper\\xml'
    all_xml = os.listdir(FOLDER_PATH)
    for FILE_NAME in all_xml:
        stages = {}
        xml = os.path.join(FOLDER_PATH, FILE_NAME)
        stages = get_LCIA(xml)
        result = get_meta_data(xml, stages)
        if result != None:
            results.append(result)
    return results

#result = runSingle("1504d42a-c5bb-4799-bd59-5b7fe07ddda7.xml")
#fc442d0a-fbc4-4304-ace8-24304756e2df

result = runAll()


final = json.dumps(result, indent=2)
with open("final-result.json", "w") as outfile:
    outfile.write(final) 



