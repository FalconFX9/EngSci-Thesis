import re

def get_categories():
    with open(".\\EKUD-Reduced\\EKUD-Reduced.yaml", 'r') as file:
        lines = file.readlines()
    categories = {}
    for line in lines:
        match = re.match(r"\s*([0-9]+):(.*)", line)
        if match:
            print(match.group(1), match.group(2).strip())
            categories[match.group(2).strip()] = int(match.group(1).strip())

    return categories


def new_categories(categories):
    ncats = {}
    for cat in categories:
        if "knife" in cat.lower():
            if not "knife" in ncats:
                ncats["knife"] = [categories[cat]]
            else:
                ncats["knife"].append(categories[cat])
        
        elif "spoon" in cat.lower():
            if not "spoon" in ncats:
                ncats["spoon"] = [categories[cat]]
            else:
                ncats["spoon"].append(categories[cat])
        
        elif "fork" in cat.lower():
            if not "fork" in ncats:
                ncats["fork"] = [categories[cat]]
            else:
                ncats["fork"].append(categories[cat])

    return ncats


if __name__ == "__main__":
    categories = get_categories()
    print(categories)
    print(new_categories(categories))