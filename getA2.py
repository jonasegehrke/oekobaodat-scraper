import requests

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

i = 0
for element in response["data"]:
    if 'owner' in element:
        i = i+1
        print(element["owner"])
    else:
        print(element)

print(i)

#skip if not fount:
#validUntil
#refYear