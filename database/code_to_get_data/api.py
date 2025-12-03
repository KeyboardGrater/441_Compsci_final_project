import requests
import json 
import time

# --- Database Schema Key ---
# We define a list to store all the collected Pokémon data
pokemon_data_list = []

def call_pokemon_api(pokemon_id):
    """
    Makes a GET request to the core PokéAPI endpoint for a specific Pokémon ID.
    (https://pokeapi.co/api/v2/pokemon/{id})
    """
    base_url = "https://pokeapi.co/api/v2/pokemon/"
    url = f"{base_url}{pokemon_id}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            # Note: Removed the print for cleaner output during the main loop
            return None

    except requests.exceptions.RequestException:
        # Note: Removed the print for cleaner output during the main loop
        return None

# --- NEW FUNCTION FOR EGG GROUPS ---
def call_pokemon_species_api(pokemon_id):
    """
    Makes a GET request to the Pokémon Species endpoint to get Egg Group data.
    (https://pokeapi.co/api/v2/pokemon-species/{id})
    """
    # This is the correct endpoint for species-specific data like Egg Groups and flavor text
    base_url = "https://pokeapi.co/api/v2/pokemon-species/" 
    url = f"{base_url}{pokemon_id}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    except requests.exceptions.RequestException:
        return None
    
    # The original call_egg_group_api is removed as it was incorrect and unused
    # (The endpoint: /api/v2/egg-group/{id} is for querying a group, not a Pokémon's groups)

def call_evolution_chain_api (chain_url):
    if not chain_url:
        return None
    
    try:
        response = requests.get(chain_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    except requests.exceptions.RequestException:
        return None

def generation_name_parser (species_data):
    generation_dict = species_data.get('generation')
    generation_name = generation_dict.get('name').replace('generation-', '')

    match generation_name:
        case 'i': result = 1
        case 'ii': result = 2
        case 'iii': result = 3
        case 'iv': result = 4
        case 'v': result = 5
        case 'vi': result = 6
        case 'vii': result = 7
        case 'viii': result = 8

    return result

def main():
    # Loop through the first 151 Pokémon
    START_ID = 1
    END_ID = 154
    
    print(f"--- Starting data collection for Pokémon IDs {START_ID} to {END_ID} ---")
    
    for pokemon_id in range(START_ID, END_ID + 1):
        # Get Core Data (Name, Stats, Types)
        base_info = call_pokemon_api(pokemon_id)
                

        # Get Species Data (Egg Groups)
        species_data = call_pokemon_species_api(pokemon_id)

        # 3. Parse the data 


        if base_info and species_data:
            # Data obtained from base_info api call
            name = base_info['name'].capitalize()
            types = [t['type']['name'].capitalize() for t in base_info['types']]
            height = base_info['height']
            weight = base_info['weight']

            # Data obtained from Pokemon Location Areas

            # Data obtained from Pokemon Shapes

            # Data obtained from species_data api call
            egg_groups = [g['name'].capitalize() for g in species_data['egg_groups']]
            is_lengendary = species_data['is_legendary']
            is_mythical = species_data['is_mythical']
            
            parent_species_dict = species_data.get('evolves_from_species')
            evolves_from_name = parent_species_dict.get('name').capitalize() if parent_species_dict else None

            generation_num = generation_name_parser(species_data)



            # Data obtained from evolution_chain api call
            chain_dict = species_data.get('evolution_chain')
            chain_url = chain_dict.get('url') if chain_dict else None

            if chain_url:
                chain_id = int(chain_url.split('/')[-2])
            else:
                chain_id = None
            
        
            # Structure the data
            pokemon_entry = {
                'ID': pokemon_id,
                'Name': name,
                'Type_1': types[0],
                'Type_2': types[1] if len(types) > 1 else None,
                'Height': height,
                'Weight': weight,

                'Egg_Groups': egg_groups,
                'Lengendary': is_lengendary,
                'Mythical' : is_mythical,
                'Evolves_from': evolves_from_name,
                'Evolution_Chain_ID': chain_id,
                'Generation': generation_num
            }

            pokemon_data_list.append(pokemon_entry)
            #print(f"{pokemon_id}: {name} ({', '.join(egg_groups)} Egg Group(s))")
            print(f"{pokemon_id}: {name}")

            # Add some delay to the api inorder to limit the rate
            time.sleep(0.05)

        else:
            print(f"Skipping ID {pokemon_id} due to failed API call.")


        
    print("\n--- Data Collection Complete ---")
    print(f"Successfully collected data for {len(pokemon_data_list)} Pokémon.")
    
    # Save the data to a JSON file
    with open('pokemon_data.json', 'w') as f:
        json.dump(pokemon_data_list, f, indent=4)
        
    print("Data saved to 'pokemon_data.json'")


if __name__ == "__main__":
    main()