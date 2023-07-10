import requests
import json
from bs4 import BeautifulSoup


# Open and read a file into a dictionary object
def read_json_file(filename):
    #check to see if the file exists
    try:
        o = open(filename)
        o.close()
    except FileNotFoundError:
        #create the file
        with open(filename, 'w') as file:
            file.write('{}')
    with open(filename) as file:
        data = json.load(file)
        return data

def scrape_table(html):
    default_headings = ['recipe', 'recipe_level', 'type', 'num_crafted',
                    'difficulty', 'durability', 'max_qual', 'materials', 'crystals']

    soup = BeautifulSoup(html, 'html.parser')
    crafting_tables = soup.find_all('table', class_='crafting')
    print(f'Found {len(crafting_tables)/2} crafting tables')

    crafter = soup.find('h1', class_='firstHeading').get_text()


    for table in crafting_tables:
        # print('Starting new table')
        rows = table.find_all('tr')
        # create a unique object for each recipe
        for row in rows:
            cells = row.find_all('td')

            if len(cells) == 0:
                # print("Skipping empty row")
                continue

            item = {}
            i = 0
            for cell in cells:
                if i >= len(default_headings):
                    print("Detected extra cells, skipping")
                    print(f"Extra cell: {cell.get_text()}")
                    break
                item[default_headings[i]] = cell.get_text()
                i += 1

            # if type is other, skip it
            if item['type'] == 'Other':
                continue

            # parse materials into a dictionary
            if ", " in item['materials']:
                item['materials'] = parse_materials(item['materials'])
            else:
                quantity, material_name = item['materials'].replace("\n", "").split(" ", 1)
                item['materials'] = {material_name: int(quantity)}

            if ", " in item['crystals']:
                item['crystals'] = parse_materials(item['crystals'])
            else:
                quantity, crystal_name = item['crystals'].replace("\n", "").split(" ", 1)
                item['crystals'] = {crystal_name: int(quantity)}

            # if item has anything in it, update the data with it's values
            if len(item) > 0:
                if (crafter in data):
                    data[crafter][item['recipe']] = item
                    # print(f'Updated {crafter} {item["recipe"]}')
                else:
                    data[crafter] = {item['recipe']: item}
                    # print(f'Added {crafter} {item["recipe"]}')

def parse_materials(materials_str):
    materials_dict = {}
    materials_list = materials_str.replace("\n", "").split(", ")

    for material in materials_list:
        quantity, material_name = material.split(" ", 1)
        materials_dict[material_name] = int(quantity)

    return materials_dict

urls_to_scrape = [
    'https://ffxiv.consolegameswiki.com/wiki/Alchemist_Recipes',
    'https://ffxiv.consolegameswiki.com/wiki/Armorer_Recipes',
    'https://ffxiv.consolegameswiki.com/wiki/Blacksmith_Recipes',
    'https://ffxiv.consolegameswiki.com/wiki/Carpenter_Recipes',
    'https://ffxiv.consolegameswiki.com/wiki/Culinarian_Recipes',
    'https://ffxiv.consolegameswiki.com/wiki/Goldsmith_Recipes',
    'https://ffxiv.consolegameswiki.com/wiki/Leatherworker_Recipes',
    'https://ffxiv.consolegameswiki.com/wiki/Weaver_Recipes',
    ]

test_url = ['https://ffxiv.consolegameswiki.com/wiki/Alchemist_Recipes']

# Declare a variable to hold the new data and read any existing data into it
data = read_json_file("./crafting_recipes.json")
# run the scraper for each URL
for URL in urls_to_scrape:
    page = requests.get(URL)
    if page.status_code != 200:
        print(f'Error: {page.status_code}')
        exit()
    # Declare a variable to hold the data and read into it
    scrape_table(page.text)
    # overwrite all data in the file with the new data
    with open("./crafting_recipes.json", 'w') as file:
        json.dump(data, file, indent=4)
