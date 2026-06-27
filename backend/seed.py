"""Seed the SQLite database with large sample business data."""

import sqlite3
import random
from datetime import date, timedelta

random.seed(42)

conn = sqlite3.connect("text_to_sql.db")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS employees;
"""
)

cur.executescript("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    city TEXT,
    country TEXT,
    phone TEXT,
    created_at TEXT DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    supplier TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    order_date TEXT,
    status TEXT DEFAULT 'pending',
    shipping_city TEXT
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT,
    role TEXT,
    salary REAL,
    hire_date TEXT,
    manager_id INTEGER REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES products(id),
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date TEXT
);
""")



first_names = ["Alice","Bob","Carol","David","Eva","Frank","Grace","Henry","Isla","Jack",
               "Karen","Liam","Mia","Noah","Olivia","Paul","Quinn","Rachel","Sam","Tina",
               "Uma","Victor","Wendy","Xander","Yara","Zoe","Aaron","Bella","Chris","Diana",
               "Ethan","Fiona","George","Hannah","Ivan","Julia","Kevin","Laura","Mike","Nancy",
               "Oscar","Pam","Quentin","Rose","Steve","Tracy","Uri","Vera","Will","Xena"]

last_names = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Wilson",
              "Moore","Taylor","Anderson","Thomas","Jackson","White","Harris","Martin","Thompson",
              "Young","Allen","King","Scott","Green","Baker","Adams","Nelson","Carter","Mitchell",
              "Perez","Roberts","Turner","Phillips","Campbell","Parker","Evans","Edwards","Collins",
              "Stewart","Sanchez","Morris","Rogers","Reed","Cook","Morgan","Bell","Murphy","Bailey"]

cities = ["New York","Los Angeles","Chicago","Houston","Phoenix","Philadelphia","San Antonio",
          "San Diego","Dallas","San Jose","Austin","Jacksonville","Fort Worth","Columbus","Charlotte",
          "Indianapolis","Seattle","Denver","Nashville","Oklahoma City","Miami","Atlanta","Boston",
          "Las Vegas","Portland","Memphis","Louisville","Baltimore","Milwaukee","Albuquerque"]

countries = ["USA","Canada","UK","Australia","Germany","France","India","Brazil","Mexico","Japan"]

suppliers = ["TechSupply Co","Global Goods","FastShip Inc","Quality First","BulkDeal Ltd",
             "Prime Wholesale","EcoSource","TechParts Pro","ValueChain Co","DirectSupply"]

customers = []
for i in range(200):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    name = f"{fn} {ln}"
    email = f"{fn.lower()}.{ln.lower()}{i}@example.com"
    city = random.choice(cities)
    country = random.choice(countries)
    phone = f"+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
    created = date(2022, 1, 1) + timedelta(days=random.randint(0, 730))
    customers.append((name, email, city, country, phone, created.isoformat()))

cur.executemany("INSERT INTO customers (name, email, city, country, phone, created_at) VALUES (?,?,?,?,?,?)", customers)

categories = {
    "Electronics": [
        ("Laptop Pro 15\"", 1299.99), ("Laptop Air 13\"", 999.99), ("Gaming Laptop", 1599.99),
        ("Wireless Mouse", 29.99), ("Mechanical Keyboard", 89.99), ("USB-C Hub", 49.99),
        ("Monitor 27\"", 349.99), ("Monitor 32\" 4K", 599.99), ("Webcam HD", 79.99),
        ("Noise Cancelling Headphones", 249.99), ("Bluetooth Speaker", 69.99),
        ("Smartphone X", 899.99), ("Tablet Pro", 649.99), ("Smartwatch", 299.99),
        ("External SSD 1TB", 109.99), ("USB Flash Drive 128GB", 19.99),
    ],
    "Furniture": [
        ("Standing Desk", 499.99), ("Ergonomic Chair", 399.99), ("Bookshelf", 149.99),
        ("Filing Cabinet", 199.99), ("Whiteboard 4x3", 89.99), ("Desk Lamp", 39.99),
        ("Monitor Arm", 59.99), ("Cable Management Kit", 24.99),
    ],
    "Stationery": [
        ("Notebook Pack (5)", 12.99), ("Ballpoint Pens (20)", 5.99), ("Highlighters Set", 8.99),
        ("Sticky Notes Pack", 6.49), ("Stapler", 14.99), ("Paper Clips Box", 3.99),
        ("Binder A4", 7.99), ("Printer Paper (500)", 9.99),
    ],
    "Clothing": [
        ("Company T-Shirt S", 19.99), ("Company T-Shirt M", 19.99), ("Company T-Shirt L", 19.99),
        ("Polo Shirt", 34.99), ("Hoodie", 49.99), ("Cap", 15.99),
    ],
    "Food & Beverage": [
        ("Coffee Beans 1kg", 24.99), ("Green Tea Pack", 12.99), ("Protein Bar Box (12)", 29.99),
        ("Mineral Water 24pk", 14.99), ("Snack Mix 1kg", 18.99),
    ],
}

products = []
for category, items in categories.items():
    for name, price in items:
        stock = random.randint(10, 500)
        supplier = random.choice(suppliers)
        products.append((name, category, price, stock, supplier))

cur.executemany("INSERT INTO products (name, category, price, stock, supplier) VALUES (?,?,?,?,?)", products)

statuses = ["completed", "completed", "completed", "shipped", "pending", "cancelled"]

start_date = date(2023, 1, 1)
orders = []
for i in range(500):
    customer_id = random.randint(1, 200)
    order_date = start_date + timedelta(days=random.randint(0, 730))
    status = random.choice(statuses)
    shipping_city = random.choice(cities)
    orders.append((customer_id, order_date.isoformat(), status, shipping_city))

cur.executemany("INSERT INTO orders (customer_id, order_date, status, shipping_city) VALUES (?,?,?,?)", orders)

num_products = sum(len(v) for v in categories.values())
order_items = []
for order_id in range(1, 501):
    num_items = random.randint(1, 5)
    chosen_products = random.sample(range(1, num_products + 1), min(num_items, num_products))
    for product_id in chosen_products:
        quantity = random.randint(1, 10)
        cur.execute("SELECT price FROM products WHERE id=?", (product_id,))
        row = cur.fetchone()
        unit_price = row[0] if row else 9.99
        order_items.append((order_id, product_id, quantity, unit_price))

cur.executemany("INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?,?,?,?)", order_items)

departments = {
    "Engineering": ["Software Engineer","Senior Engineer","Lead Engineer","Engineering Manager"],
    "Sales": ["Sales Rep","Senior Sales Rep","Sales Manager","Account Executive"],
    "Marketing": ["Marketing Analyst","Content Writer","Marketing Manager","SEO Specialist"],
    "HR": ["HR Coordinator","HR Manager","Recruiter","HR Director"],
    "Finance": ["Accountant","Financial Analyst","Finance Manager","CFO"],
    "Support": ["Support Agent","Senior Support Agent","Support Manager","Technical Support"],
}

employees = []
for dept, roles in departments.items():
    for i in range(8):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        role = random.choice(roles)
        salary = round(random.uniform(40000, 150000), 2)
        hire_date = date(2018, 1, 1) + timedelta(days=random.randint(0, 2000))
        employees.append((f"{fn} {ln}", dept, role, salary, hire_date.isoformat(), None))

cur.executemany("INSERT INTO employees (name, department, role, salary, hire_date, manager_id) VALUES (?,?,?,?,?,?)", employees)

comments = [
    "Great product!", "Works as expected.", "Good value for money.", "Highly recommend.",
    "Not bad.", "Could be better.", "Excellent quality.", "Fast delivery.",
    "Would buy again.", "Meets expectations.", "Decent product.", "Love it!",
]

reviews = []
for _ in range(400):
    product_id = random.randint(1, num_products)
    customer_id = random.randint(1, 200)
    rating = random.choices([1,2,3,4,5], weights=[5,10,15,35,35])[0]
    comment = random.choice(comments)
    review_date = (start_date + timedelta(days=random.randint(0, 730))).isoformat()
    reviews.append((product_id, customer_id, rating, comment, review_date))

cur.executemany("INSERT INTO reviews (product_id, customer_id, rating, comment, review_date) VALUES (?,?,?,?,?)", reviews)

conn.commit()

cur.execute("SELECT COUNT(*) FROM customers"); print(f"Customers:   {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM products");  print(f"Products:    {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM orders");    print(f"Orders:      {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM order_items"); print(f"Order items: {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM employees"); print(f"Employees:   {cur.fetchone()[0]}")
cur.execute("SELECT COUNT(*) FROM reviews");   print(f"Reviews:     {cur.fetchone()[0]}")

conn.close()
print("\nSample questions to try:")
print("  - Which city has the most customers?")
print("  - What is the total revenue by product category?")
print("  - Show top 10 customers by total spend")
print("  - Which products have average rating above 4?")
print("  - What is the average salary per department?")
print("  - How many orders were placed each month in 2024?")
print("  - List products with stock below 50")
print("  - Which employees earn more than 100000?")
