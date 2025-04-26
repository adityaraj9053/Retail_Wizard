import sqlite3

def print_transactions():
    
    conn = sqlite3.connect("grocery.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    
    cursor.execute("PRAGMA table_info(transactions)")
    columns = [col[1] for col in cursor.fetchall()]
    
    print(" | ".join(columns))
    print("-" * 50)
    
    for row in rows:
        print(" | ".join(map(str, row)))
    
    conn.close()

if __name__ == "__main__":
    print_transactions()