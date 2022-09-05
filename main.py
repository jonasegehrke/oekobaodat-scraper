import json
import os
from types import NoneType

from bs4 import BeautifulSoup


def get_data(xml):
    with open(xml,"r", errors='ignore') as fp:
        soup = BeautifulSoup(fp, 'xml')
  
  
  
   ## TODO move to new function that takes care of "INFO"

def get_meta_data(xml, stages):
    with open(xml,"r", errors='ignore') as fp:
        soup = BeautifulSoup(fp, 'xml')

        result = {}
        result["epdInfo"] = {}
        result["declaredUnit"] = {}
        result["link"] = []

        result["custom"] = False
        result["scraped"] = True

        result["generic"] = True
        result["expectedLifespan"] = None

        for baseName in soup.find_all('baseName'):
            if baseName["xml:lang"] == "en":
                result["shortName"] = baseName.text
                
        
        result["longName"] = None
        product_description = soup.find("common:generalComment")
        if product_description.get("xml:lang") == "en":
            result["description"] = product_description.text

        uuid = soup.find("dataSetInformation").find("common:UUID").text
        result["link"] = "https://oekobaudat.de/OEKOBAU.DAT/datasetdetail/process.xhtml?uuid=" + uuid

        if stages == None: return
        result["stages"] = stages


        
        if soup.find("time") == None:
            all_valid_until = None
            all_reference_year = None
        else:
            all_valid_until = soup.find("time").find("common:dataSetValidUntil").text
            all_reference_year = soup.find("time").find("common:referenceYear").text
        
        result["declaredUnit"]["declaredUnit"] = None
        result["declaredUnit"]["declaredValue"] = None
        result["declaredUnit"]["mass"] = None
        result["declaredUnit"]["massUnit"] = None

        result["epdInfo"]["issuedAt"] = all_reference_year
        result["epdInfo"]["validTo"] = all_valid_until
        result["epdInfo"]["dateRangeStart"] = None
        result["epdInfo"]["dateRangeEnd"] = None
        result["epdInfo"]["epdSpecificationForm"] = None
        result["epdInfo"]["epdProductIndustryType"] = None
        
        
        tags = soup.find("technologyDescriptionAndIncludedProcesses")
        if tags == None: return
        if tags.get("xml:lang") == "en":
            result["tags"] = tags.text
        else:
            result["tags"] = None
        

    return result

def runAll():
    results = []
    FOLDER_PATH = r'/Users/andreasholmandersen/Documents/Capacit/oekobaodat-scraper/xml'
    all_xml = os.listdir(FOLDER_PATH)
    for FILE_NAME in all_xml:
        xml = os.path.join(FOLDER_PATH, FILE_NAME)
        #values 
        #info
        result = get_meta_data(xml, {})
        if result != None:
            results.append(result)
    return results


def runSingle(file):
    results = []
    FOLDER_PATH = r'/Users/andreasholmandersen/Documents/Capacit/oekobaodat-scraper/xml'
    FILE_NAME = file
    xml = os.path.join(FOLDER_PATH, FILE_NAME)
    result = get_meta_data(xml, {})
    results.append(result)
    return results


# result = runSingle("0d968a32-96fb-4ba4-9497-3c343cd8ecde.xml")

result = runAll()

final = json.dumps(result, indent=2)
with open("test2.json", "w") as outfile:
    outfile.write(final) 