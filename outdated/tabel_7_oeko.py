import json



def get_names_tabel_7():
    f = open("resultTabel7.json")
    data = json.load(f)

    names = []
    for obj in data:

        name = obj["Title"]

        name = name.strip()
        name = name.lower()
        name = name.replace(" ", "")
        name = name.replace(",", "")
        
        names.append(name)
    return names


def get_names_oeko():
   with open("/Users/andreasholmandersen/Documents/Capacit/oekobaodat-scraper/oeko-scrape.json") as f:
    data = json.loads(f.read())
    
    names = []
    for obj in data:
        name = obj["shortName"]

        name = name.strip()
        name = name.lower()
        name = name.replace(" ", "")
        name = name.replace(",", "")
        
        names.append(name)

    return names



names_list_tabel_7 = get_names_tabel_7()

names_list_oeko = get_names_oeko()

def compare_list(list_one, list_two):
    misses = 1
    hits = 1
    for name_one in list_one:
        for name_two in list_two:
            if name_one == name_two:
                print(name_one, name_two)
                hits += 1
                
            else:
                misses += 1
    print("hits: ", hits)
    print("misses: ", misses)
                




    



compare_list(names_list_tabel_7, names_list_oeko)