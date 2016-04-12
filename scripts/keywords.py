import sys
import json

def get_titles(manufacturer):
    categories = {}
    with open("../aps/{}_aps.json".format(manufacturer)) as f:
        lines = json.load(f, encoding="ascii")
        for line in lines:
            product = lines[line]
            cat = product['category']
            words = [word for word in product['title'].split(' ')]
            if not categories.get(cat):
                categories[cat] = {}
            for word in words:
                if categories[cat].get(word):
                    categories[cat][word] += 1
                else:
                    categories[cat][word] = 1
    print categories
    print categories.keys()

get_titles(sys.argv[1])

