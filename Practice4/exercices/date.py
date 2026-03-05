import json
from datetime import datetime, timedelta

# --- PART 1: READING THE JSON FILE ---
try:
    with open('sample-data.json', 'r') as file:
        data = json.load(file)
    
    # Extracting the timestamp from the first interface
    raw_date = data["imdata"][0]["l1PhysIf"]["attributes"]["modTs"]
    # Parsing the date string (first 19 chars: YYYY-MM-DDTHH:MM:SS)
    clean_date_str = raw_date[:19].replace('T', ' ')
    sample_date = datetime.strptime(clean_date_str, '%Y-%m-%d %H:%M:%S')
except Exception as e:
    print(f"Error reading JSON: {e}")
    sample_date = datetime.now()

# --- PART 2: DATETIME TASKS ---

# 1. Subtract five days from the date
five_days_ago = sample_date - timedelta(days=5)

# 2. Yesterday, Today, Tomorrow (based on current system time)
today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

# 3. Drop microseconds from datetime
# We use replace(microsecond=0) to remove them
no_microseconds = today.replace(microsecond=0)

# 4. Calculate difference in seconds
# Difference between current time and the date from JSON
difference_in_seconds = (today - sample_date).total_seconds()

# --- PART 3: WRITING RESULTS TO A NEW FILE ---
with open('results.txt', 'w', encoding='utf-8') as out:
    out.write("=== DATA FROM JSON ===\n")
    out.write(f"Original Date: {sample_date}\n")
    out.write(f"Five days ago: {five_days_ago}\n\n")
    
    out.write("=== CALENDAR TASKS ===\n")
    out.write(f"Yesterday: {yesterday.strftime('%Y-%m-%d')}\n")
    out.write(f"Today:     {today.strftime('%Y-%m-%d')}\n")
    out.write(f"Tomorrow:  {tomorrow.strftime('%Y-%m-%d')}\n\n")
    
    out.write("=== ADDITIONAL OPERATIONS ===\n")
    out.write(f"Without Microseconds: {no_microseconds}\n")
    out.write(f"Difference in seconds: {difference_in_seconds:.2f} sec\n")

print("Success! The results have been saved to 'results.txt'.")