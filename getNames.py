import json

with open("final-result.json") as json_file:
    materials = json.load(json_file)
    print(materials[0])
    names = set()
    for material in materials:
        for stage in material["stages"]:
            for key in stage["measures"]:
                names.add(key)


    print(names)

    for name in names:
        