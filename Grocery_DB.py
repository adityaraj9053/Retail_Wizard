import sqlite3

def view_database():
    conn = sqlite3.connect("grocery.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM grocery")
    rows = cursor.fetchall()
    
    
    if not rows:
        print("No data found in the grocery database.")
    else:
        print("\nStored Grocery Data:\n")
        for row in rows:
            print(row)


        print("\nSchema of Grocery Table:")
        cursor.execute("PRAGMA table_info(grocery);")
        grocery_schema = cursor.fetchall()
        for column in grocery_schema:
            print(column)


        print("\nSchema of Selected Product Table:")
        cursor.execute("PRAGMA table_info(selected_product);")
        selected_product_schema = cursor.fetchall()
        for column in selected_product_schema:
            print(column)

    cursor.execute("SELECT * FROM selected_product")
    selected_rows = cursor.fetchall()
    
    if not selected_rows:
        print("\nNo data found in the selected_product table.")
    else:
        print("\nStored Selected Product Data:\n")
        for row in selected_rows:
            print(row)
    
    conn.close()




if __name__ == "__main__":
    view_database()