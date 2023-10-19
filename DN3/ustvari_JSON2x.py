import json

zacetniData = {
    "persons": [
        {"name": "Alice", "age": 30, "married": True, "employed": True},
        {"name": "Bob", "age": 40, "married": False, "employed": True},
        {"name": "Charlie", "age": 25, "married": True, "employed": False},
        {"name": "David", "age": 32, "married": False, "employed": True},
        {"name": "Eve", "age": 29, "married": True, "employed": False},
        {"name": "Fay", "age": 37, "married": False, "employed": True},
        {"name": "Grace", "age": 45, "married": True, "employed": True},
        {"name": "Heidi", "age": 31, "married": False, "employed": False},
        {"name": "Ivy", "age": 21, "married": True, "employed": True},
        {"name": "Judy", "age": 26, "married": False, "employed": False}
    ]
}

updateData = {
    "persons": [
        {"name": "Alice", "age": 31, "employed": False},
        {"name": "Bob", "married": True},
        {"name": "Charlie", "age": 26},
        {"name": "David", "employed": False},
        {"name": "Eve", "married": False},
        {"name": "Fay", "age": 38, "employed": False},
        {"name": "Grace", "age": 46},
        {"name": "Heidi", "married": True, "employed": True},
        {"name": "Ivy", "age": 22},
        {"name": "Judy", "employed": True}
    ]
}

# Shrani - zamenjaj PATH do folderja kjer bos shranil obe JSON datoteki. Ne pozabi dodati ime datoteke na koncu path-a!
# npr ./DATA/zacetniData.json
with open('PATH', 'w') as f:
    json.dump(zacetniData, f, indent=2)

with open('PATH', 'w') as f:
    json.dump(updateData, f, indent=2)