import json
import csv

try:
    with open('info.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open('report.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Age', 'University'])
        if isinstance(data, list):
            for item in data:
                writer.writerow([item.get('name', 'N/A'), item.get('age', 'N/A'), item.get('university', 'N/A')])
        elif isinstance(data, dict):
            writer.writerow([data.get('name', 'N/A'), data.get('age', 'N/A'), data.get('university', 'N/A')])

    print("Success! report.csv created.")

except Exception as e:
    print(f"Error: {e}")