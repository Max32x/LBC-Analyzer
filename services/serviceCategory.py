import os
import json

def id_cat(category):

    json_categories = os.path.join("data", "categories.json")
    with open(json_categories, 'r') as f:
        categories_json = json.load(f)

    if category:
        id_category = categories_json[category]
    else : 
        id_category=""

    return id_category