from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_NAME = 'budget.db'
CATEGORIES = ["Food", "Wellness", "Beauty/Skincare", "Clothing", "Accessories", "Household", "Tech"]

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # This lets us access columns by name
    return conn

@app.route('/')
def index():
    conn = get_db()
    
    # Get the "sort" and "filter" parameters from the URL
    sort_by = request.args.get('sort')
    filter_cat = request.args.get('category')

    query = 'SELECT * FROM expenses'
    params = []

    # Logic for Filtering by Category
    if filter_cat and filter_cat != "All":
        query += ' WHERE category = ?'
        params.append(filter_cat)

    # Logic for Sorting
    if sort_by == 'cost':
        query += ' ORDER BY cost DESC'
    else:
        query += ' ORDER BY id DESC'

    items = conn.execute(query, params).fetchall()
    summary = conn.execute('SELECT category, SUM(cost) as total FROM expenses GROUP BY category').fetchall()
    conn.close()
    
    return render_template(
        'index.html', 
        items=items, 
        categories=CATEGORIES, 
        summary=summary,
        current_sort=sort_by,
        current_filter=filter_cat
    )

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    new_cost = request.form['new_cost']
    conn = get_db()
    conn.execute('UPDATE expenses SET cost = ? WHERE id = ?', (new_cost, id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    cost = request.form['cost']
    store = request.form['store']
    category = request.form['category']
    
    conn = get_db()
    conn.execute('INSERT INTO expenses (item_name, cost, store, category) VALUES (?, ?, ?, ?)',
                 (name, cost, store, category))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute('DELETE FROM expenses WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)