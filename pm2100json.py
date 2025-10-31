import json
import os # Imported for better file path handling (optional, but good practice)

#--------------------------------------------------------------------
# FILE_PATH : PM2100 register map in json format
# pm2100_register_map : json strcture having PM2100 register map
# length : count of block in number of register (a word)
#          INT16U : a single word ( 2 bytes or 16bits)
#          FLOAT32 : two (2) words
#          INT64 : four (4) words
# num_registers : number of register (count in word where FLOAT32 counted as 2)
#--------------------------------------------------------------------
# read register map fle 
#--------------------------------------------------------------------
DEBUG=False

def pm2120_registermap(jsonfile):
    try:
        # Use 'with open' to ensure the file is properly closed even if errors occur
        with open(jsonfile, 'r') as file:
            # json.load(file) reads directly from the file object
            register_map = json.load(file)

        if DEBUG :
            print(f"Successfully loaded data from {jsonfile}.")
    
            # The 'for' loop implicitly uses the list's built-in iterator
            for block in register_map:
                category = block['category']
                address = block['address']
                length = block['length']        #- counts of registers
                num_registers = len(block['registers'])

                print(f"Processing category: {category}")
                print(f"  Start Address: {address}")
                print(f"  Contains {num_registers} register definitions.")
        
                for reg in block['registers']:
                    print(f"    - Register at {reg['addr']} (Type: {reg['type']})")
        return register_map
    except FileNotFoundError:
        print(f"Error: The file '{jsonfile}' was not found. Please create it and add the JSON content.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{jsonfile}'. Details: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
#----------------------------------------------------------------

if DEBUG :
    pm2120_registermap('pm2100mapabreidged.json')