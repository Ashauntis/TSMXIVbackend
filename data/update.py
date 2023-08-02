import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

# This program will take a JSON file containing the ID to name mappings and add it to the Redis database.
# It will also create a JSON file containing the English name to ID mappings for easier referencing. 
def main():
    id_map = {}
    
    # Read the JSON file
    with open('./id_to_names.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for key, value in data.items():
        # Ensure there's data in the entry
        if value['en'].strip() == "":
            print(f"Skipping {key} because it has no data.")
            continue
        # Add the ID and names to Redis
        r.hmset(key, value)
        print(f"Added {key} to Redis.")
        
        # Add the English name and corresponding ID to id_map
        id_map[value['en']] = key
    
    # Save id_map to id_map.json
    with open('id_map.json', 'w', encoding='utf-8') as f:
        json.dump(id_map, f, ensure_ascii=False, indent=4)
    
    print("id_map.json created/updated successfully.")

if __name__ == '__main__':
    main()
