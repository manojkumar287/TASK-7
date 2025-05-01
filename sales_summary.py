import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1. Connect to the SQLite database
conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()

# **Important:** Let's first create a sample 'sales' table and insert some data
# for this script to work if you don't have a 'sales_data.db' already.
# You can skip this part if you already have your database and table.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        product TEXT,
        quantity INTEGER,
        price REAL
    )
''')

sales_data = [
    ('Laptop', 5, 1200.00),
    ('Mouse', 20, 25.00),
    ('Keyboard', 15, 75.00),
    ('Monitor', 8, 300.00),
    ('Webcam', 12, 50.00)
]
cursor.executemany("INSERT INTO sales VALUES (?, ?, ?)", sales_data)
conn.commit()
print("Sample sales data created and inserted.")
print("-" * 30)

# 2. Define the SQL query
query = """
SELECT
    product,
    SUM(quantity) AS total_qty,
    SUM(quantity * price) AS total_revenue
FROM sales
GROUP BY product;
"""

# 3. Execute the SQL query and load into pandas DataFrame
df = pd.read_sql_query(query, conn)

# 4. Print the DataFrame (basic output)
print("Sales Summary:")
print(df)
print("-" * 30)

# 5. Plot a simple bar chart
plt.figure(figsize=(10, 6))
plt.bar(df['product'], df['total_revenue'], color='skyblue')
plt.xlabel("Product")
plt.ylabel("Total Revenue")
plt.title("Total Revenue per Product")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 6. Save the chart (optional)
# plt.savefig('sales_chart.png')

# 7. Close the database connection
conn.close()