import json
import psycopg2
from connect import get_connection

def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD) or enter: ")
    group_name = input("Group: ")
    phone = input("Phone: ")
    p_type = input("Phone type (mobile/work): ")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            res = cur.fetchone()
            g_id = res[0] if res else None
            
            if not g_id and group_name:
                cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group_name,))
                g_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO contacts (name, email, birthday, group_id) 
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (name, email, birthday if birthday else None, g_id))
            
            c_id = cur.fetchone()[0]
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", (c_id, phone, p_type))
            conn.commit()

def export_json(path):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, c.email, c.birthday, g.name, 
                       json_agg(json_build_object('phone', p.phone, 'type', p.type)) FILTER (WHERE p.phone IS NOT NULL)
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                GROUP BY c.id, g.name
            """)
            rows = cur.fetchall()
            data = [{"name": r[0], "email": r[1], "birthday": str(r[2]) if r[2] else None, 
                     "group": r[3], "phones": r[4] if r[4] else []} for r in rows]
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)

def import_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    with get_connection() as conn:
        with conn.cursor() as cur:
            for item in data:
                cur.execute("SELECT id FROM contacts WHERE name = %s", (item['name'],))
                exists = cur.fetchone()
                if exists:
                    if input(f"{item['name']} exists. Skip(s) or Overwrite(o)? ").lower() == 's': continue
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

def search():
    print("\nSearch by:")
    print("1. Name")
    print("2. Email")
    print("3. Phone")
    choice = input("Choice (1-3): ")
    
    val = input("Enter search value: ")
    
    query = val
    if choice == '3':
        query = f"%{val}%"

    with get_connection() as conn:
        with conn.cursor() as cur:
            if choice == '1':
                cur.execute("SELECT * FROM search_contacts(%s) WHERE name ILIKE %s", (val, f"%{val}%"))
            elif choice == '2':
                cur.execute("SELECT * FROM search_contacts(%s) WHERE email ILIKE %s", (val, f"%{val}%"))
            elif choice == '3':
                cur.execute("SELECT * FROM search_contacts(%s) WHERE phones ILIKE %s", (val, f"%{val}%"))
            else:
                cur.execute("SELECT * FROM search_contacts(%s)", (val,))
            
            rows = cur.fetchall()
            if not rows:
                print("No results found.")
            for r in rows:
                print(f"{r[1]} | {r[2]} | {r[3]} | {r[4]} | Phones: {r[5]}")

def main():
    lim, off, sort = 10, 0, 'c.name'
    while True:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT c.name, c.email, c.birthday, g.name 
                    FROM contacts c 
                    LEFT JOIN groups g ON c.group_id = g.id 
                    ORDER BY {sort} LIMIT %s OFFSET %s
                """, (lim, off))
                rows = cur.fetchall()
                print("\n" + "="*60)
                for r in rows:
                    print(f"{r[0]:<15} | {r[1]:<20} | {str(r[2]):<12} | {r[3]}")
        
        cmd = input("\n[a]dd, [n]ext, [p]rev, [s]earch, [sort], [e]xport, [i]mport, [q]uit: ").lower()
        if cmd == 'a': add_contact()
        elif cmd == 'n': off += lim
        elif cmd == 'p': off = max(0, off - lim)
        elif cmd == 's': search()
        elif cmd == 'sort':
            f = input("Field (name, birthday, date_added): ")
            sort = f"c.{f}" if f in ['name', 'birthday', 'date_added'] else 'c.name'
        elif cmd == 'e': export_json('contacts.json')
        elif cmd == 'i': import_json('contacts.json')
        elif cmd == 'q': break

if __name__ == "__main__":
    main()