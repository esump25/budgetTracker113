import sqlite3

# --- SETUP: Connect to the database file ---
conn = sqlite3.connect('budget.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        cost REAL,
        store TEXT,
        category TEXT
    )
''')
conn.commit()

# --- CRUD OPERATIONS ---

def add_item(name, cost, store, category):
    cursor.execute('INSERT INTO expenses (item_name, cost, store, category) VALUES (?, ?, ?, ?)', 
                   (name, cost, store, category))
    conn.commit()
    print(f"✅ Added {name} successfully!")

def view_items(sort_by_cost=False):
    # This fulfills your "filtered/sorted" requirement
    query = "SELECT * FROM expenses"
    if sort_by_cost:
        query += " ORDER BY cost DESC"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    print("\n--- Current Shopping List ---")
    for row in rows:
        print(f"ID: {row[0]} | Item: {row[1]} | Cost: ${row[2]:.2f} | Store: {row[3]} | Category: {row[4]}")

def update_cost(item_id, new_cost):
    cursor.execute('UPDATE expenses SET cost = ? WHERE id = ?', (new_cost, item_id))
    conn.commit()
    print("✅ Price updated!")

def delete_item(item_id):
    cursor.execute('DELETE FROM expenses WHERE id = ?', (item_id,))
    conn.commit()
    print("🗑️ Item removed.")

def view_by_category():
    # Let the user pick which category to filter by
    CATEGORIES = ["Food", "Wellness", "Beauty/Skincare", "Clothing", "Accessories", "Household", "Tech"]
    
    print("\nWhich category would you like to view?")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}. {cat}")
    
    cat_idx = int(input("Enter number: ")) - 1
    selected_cat = CATEGORIES[cat_idx]

    # SQL query to filter results
    cursor.execute('SELECT * FROM expenses WHERE category = ?', (selected_cat,))
    rows = cursor.fetchall()
    
    print(f"\n--- Items in {selected_cat} ---")
    if not rows:
        print("No items found in this category.")
    else:
        for row in rows:
            print(f"ID: {row[0]} | Item: {row[1]} | Cost: ${row[2]:.2f} | Store: {row[3]}")

def view_summary():
    # SQL query: Select the category and the SUM of costs for that category
    # GROUP BY tells SQL to calculate the sum for each unique category name
    query = '''
        SELECT category, SUM(cost), COUNT(item_name) 
        FROM expenses 
        GROUP BY category 
        ORDER BY SUM(cost) DESC
    '''
    cursor.execute(query)
    rows = cursor.fetchall()

    print("\n--- 📊 Spending Summary ---")
    total_budget = 0
    for row in rows:
        category, total_cost, item_count = row
        print(f"{category}: ${total_cost:.2f} ({item_count} items)")
        total_budget += total_cost
    
    print("-" * 25)
    print(f"GRAND TOTAL: ${total_budget:.2f}")

# --- THE CLI MENU ---

def main():
    while True:
        print("\n--- 🛒 Shopping Budget Planner ---")
        print("1. Add Item")
        print("2. View All Items")
        print("3. View Items (Sorted by Cost)")
        print("4. View Items by Category")
        print("5. View Spending Summary")
        print("6. Update Item Price")
        print("7. Delete Item")
        print("8. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Item name: ")
            cost = float(input("Cost: $"))
            store = input("Store: ")
            # Define your master list
            CATEGORIES = ["Food", "Wellness", "Beauty/Skincare", "Clothing", "Accessories", "Household", "Tech", "Entertainment", "Gifts"]

            print("\nSelect a Category:")
            for i, cat in enumerate(CATEGORIES, 1):
                print(f"{i}. {cat}")

            # Get the choice and map it back to the string
            cat_choice = int(input("Enter number: ")) - 1
            category = CATEGORIES[cat_choice]
            add_item(name, cost, store, category)
        elif choice == '2':
            view_items()
        elif choice == '3':
            view_items(sort_by_cost=True)
        elif choice == '4':
            view_by_category()
        elif choice == '5':
            view_summary()
        elif choice == '6':
            id_to_upd = int(input("Enter ID to update: "))
            price = float(input("New price: "))
            update_cost(id_to_upd, price)
        elif choice == '7':
            id_to_del = int(input("Enter ID to delete: "))
            delete_item(id_to_del)
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
    conn.close()