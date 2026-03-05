import json
from datetime import datetime, timedelta

# 1. Read
try:
    with open('info.json', 'r', encoding='utf-8') as file:
        user_data = json.load(file)
    
    # 2. Process
    user_data['age'] += 1
    
    if "subjects" in user_data and isinstance(user_data['subjects'], list):
        if "Algorithms" not in user_data['subjects']:
            user_data['subjects'].append("Algorithms")
    
    user_data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 3. Write
    with open('updated_info.json', 'w', encoding='utf-8') as out_file:
        json.dump(user_data, out_file, indent=4)
        
    print("Success: updated_info.json created.")

except FileNotFoundError:
    print("Error: info.json not found.")
except Exception as e:
    print(f"Error: {e}")