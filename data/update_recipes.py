import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def main():
    # keep track of how many recipes we've skipped
    skipped = 0 
    # Load id_map.json into a variable
    with open('./id_map.json', 'r', encoding='utf-8') as f:
        id_map = json.load(f)
    # Load the recipe data into a variable as well
    with open('./crafting_recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)
        print(type(recipes))
    # Iterate through the recipes and add the unique ID to each recipe
    for recipe in recipes.items():
        # match the recipe's name to the ID in id_map
        # print(type(recipe))
        try:
            recipe_id = id_map[recipe[0]]
            # add each recipe to Redis using the Unique ID as the key
            # r.hmset(recipe_id, recipe)
            print(f"Added {recipe_id} to Redis.")
        except KeyError:
            print(f"Skipping {recipe[0]} because it has no ID.")
            skipped += 1
            continue
    print(f"Finished adding recipes to Redis. Skipped {skipped} recipes.")

if __name__ == '__main__':
    main()