import os
import json
import re

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(BASE_DIR, "json_output1_recipes_detail")
RAW_OUTPUT = os.path.join(BASE_DIR, "raw_mustika_rasa_full.json")

def get_page_number(filename):
    match = re.search(r'page_(\d+)', filename)
    return int(match.group(1)) if match else 99999

def main():
    all_files = sorted(
        [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".json")],
        key=get_page_number
    )
    
    raw_list = []
    print(f"📂 Extracting fragments from {len(all_files)} files...")

    for filename in all_files:
        page_num = get_page_number(filename)
        file_path = os.path.join(INPUT_FOLDER, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                for index, recipe in enumerate(data):
                    # Create unique ID: MR_Page_Index
                    recipe['recipe_id'] = f"MR_{page_num}_{str(index + 1).zfill(2)}"
                    recipe['_source_page'] = page_num 
                    raw_list.append(recipe)
                    
        except Exception as e:
            print(f"❌ Error in {filename}: {e}")

    with open(RAW_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(raw_list, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Raw data saved to {RAW_OUTPUT}")

if __name__ == "__main__":
    main()