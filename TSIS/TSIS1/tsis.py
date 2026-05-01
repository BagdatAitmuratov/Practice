import json
import csv
import psycopg2
from connect import get_connection

def export_json(path):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, 
               json_agg(json_build_object('phone', p.phone, 'type', p.type)) FILTER (WHERE p.phone IS NOT NULL)
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, g.name
    """)
    rows = cur.fetchall()
    data = []
    for r in rows:
        data.append({
            "name": r[0], "email": r[1], "birthday": str(r[2]) if r[2] else None,
            "group": r[3], "phones": r[4] if r[4] else []
        })
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    cur.close()
    conn.close()

def import_json(path):
    conn = get_connection()
    cur = conn.cursor()
    with open(path, 'r') as f:
        data = json.load(f)
    for item in data:
        cur.execute("SELECT id FROM contacts WHERE name = %s", (item['name'],))
        exists = cur.fetchone()
        if exists:
            print(f"{item['name']} exists. Skip(s) or Overwrite(o)?")
            if input().lower() == 's': continue
            cur.execute("DELETE FROM contacts WHERE id = %s", (exists[0],))
        
        cur.execute("SELECT id FROM groups WHERE name = %s", (item['group'],))
        g_id = cur.fetchone()
        if not g_id and item['group']:
            cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (item['group'],))
            g_id = cur.fetchone()
            
        cur.execute("INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id",
                    (item['name'], item['email'], item['birthday'], g_id[0] if g_id else None))
        c_id = cur.fetchone()[0]
        for p in item['phones']:
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", (c_id, p['phone'], p['type']))
    conn.commit()
    cur.close()
    conn.close()

def search():
    q = input("Search: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    for r in cur.fetchall():
        print(f"{r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]}")
    cur.close()
    conn.close()

def main():
    lim, off, sort = 5, 0, 'c.name'
    while True:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT c.name, c.email, c.birthday, g.name FROM contacts c LEFT JOIN groups g ON c.group_id = g.id ORDER BY {sort} LIMIT %s OFFSET %s", (lim, off))
        rows = cur.fetchall()
        for r in rows: print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}")
        cur.close()
        conn.close()
        
        cmd = input("\n[n]ext, [p]rev, [s]earch, [sort], [e]xport, [i]mport, [q]uit: ").lower()
        if cmd == 'n': off += lim
        elif cmd == 'p': off = max(0, off - lim)
        elif cmd == 's': search()
        elif cmd == 'sort':
            field = input("Field (name, birthday, date_added): ")
            sort = f"c.{field}" if field in ['name', 'birthday', 'date_added'] else 'c.name'
        elif cmd == 'e': export_json('contacts.json')
        elif cmd == 'i': import_json('contacts.json')
        elif cmd == 'q': break

if __name__ == "__main__":
    main()