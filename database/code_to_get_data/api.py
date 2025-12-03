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


def main():
    # Loop through the first 151 Pokémon
    START_ID = 1
    END_ID = 151
    
    print(f"--- Starting data collection for Pokémon IDs {START_ID} to {END_ID} ---")
    
    for pokemon_id in range(START_ID, END_ID + 1):
        # 1. Get Core Data (Name, Stats, Types)
        api_data = call_pokemon_api(pokemon_id)
        
        # 2. Get Species Data (Egg Groups)
        species_data = call_pokemon_species_api(pokemon_id)

        if api_data and species_data:
            # --- Data Extraction from API Data ---
            name = api_data['name'].capitalize()
            stats = {s['stat']['name']: s['base_stat'] for s in api_data['stats']}
            types = [t['type']['name'].capitalize() for t in api_data['types']]
            
            # --- Data Extraction from Species Data ---
            egg_groups = [g['name'].capitalize() for g in species_data['egg_groups']]

            # 3. Structure the data into a clean dictionary
            pokemon_entry = {
                'ID': pokemon_id,
                'Name': name,
                'Type_1': types[0],
                'Type_2': types[1] if len(types) > 1 else None,
                'HP': stats.get('hp'),
                'Attack': stats.get('attack'),
                'Defense': stats.get('defense'),
                'Egg_Groups': egg_groups, # ADDED: The new Egg Group data
                'Total_Stats': sum(stats.values()) 
            }
            
            pokemon_data_list.append(pokemon_entry)
            print(f"Collected data for ID {pokemon_id}: {name} ({', '.join(egg_groups)} Egg Group(s))")
            
            # Be polite to the API and prevent rate limiting
            time.sleep(0.05) 
        else:
            print(f"Skipping ID {pokemon_id} due to failed API call.")
        
    print("\n--- Data Collection Complete ---")
    print(f"Successfully collected data for {len(pokemon_data_list)} Pokémon.")
    
    # Save the data to a JSON file
    with open('first_151_pokemon_data.json', 'w') as f:
        json.dump(pokemon_data_list, f, indent=4)
        
    print("Data saved to 'first_151_pokemon_data.json'")


if __name__ == "__main__":
    main()