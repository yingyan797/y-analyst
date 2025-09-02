import sqlite3

def initialize_db(db_name):
    with sqlite3.connect(db_name) as _con:
        # Create tables
        tables = [
            """CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                city TEXT,
                registration_date DATE
            )""",
            """CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category_id INTEGER,
                price DECIMAL(10,2),
                stock_quantity INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )""",
            """CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                order_date DATE,
                total_amount DECIMAL(10,2),
                status TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )""",
            """CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                unit_price DECIMAL(10,2),
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )""",
            """CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                contact_email TEXT,
                city TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS product_suppliers (
                id INTEGER PRIMARY KEY,
                product_id INTEGER,
                supplier_id INTEGER,
                supply_price DECIMAL(10,2),
                FOREIGN KEY (product_id) REFERENCES products(id),
                FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
            )""",
            """CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                product_id INTEGER,
                customer_id INTEGER,
                rating INTEGER CHECK(rating >= 1 AND rating <= 5),
                review_text TEXT,
                review_date DATE,
                FOREIGN KEY (product_id) REFERENCES products(id),
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )"""
        ]
        
        for query in tables:
            _con.execute(query)
        
        # Insert sample data
        _insert_sample_data(_con)

def _insert_sample_data(conn):
    # Categories
    categories = [
        (1, 'Electronics', 'Electronic devices and gadgets'),
        (2, 'Clothing', 'Apparel and fashion items'),
        (3, 'Books', 'Books and educational materials'),
        (4, 'Home & Garden', 'Home improvement and garden supplies')
    ]
    conn.executemany('INSERT OR IGNORE INTO categories VALUES (?, ?, ?)', categories)
    
    # Customers
    customers = [
        (1, 'John Smith', 'john@email.com', 'New York', '2023-01-15'),
        (2, 'Sarah Johnson', 'sarah@email.com', 'Los Angeles', '2023-02-20'),
        (3, 'Mike Brown', 'mike@email.com', 'Chicago', '2023-03-10'),
        (4, 'Lisa Davis', 'lisa@email.com', 'Houston', '2023-04-05'),
        (5, 'Tom Wilson', 'tom@email.com', 'Phoenix', '2023-05-12')
    ]
    conn.executemany('INSERT OR IGNORE INTO customers VALUES (?, ?, ?, ?, ?)', customers)
    
    # Products
    products = [
        (1, 'Laptop', 1, 999.99, 50),
        (2, 'Smartphone', 1, 699.99, 100),
        (3, 'T-Shirt', 2, 19.99, 200),
        (4, 'Jeans', 2, 49.99, 150),
        (5, 'Python Book', 3, 39.99, 75),
        (6, 'Garden Tools', 4, 89.99, 30)
    ]
    conn.executemany('INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?, ?)', products)
    
    # Suppliers
    suppliers = [
        (1, 'TechCorp', 'contact@techcorp.com', 'San Francisco'),
        (2, 'Fashion Plus', 'info@fashionplus.com', 'Miami'),
        (3, 'BookWorld', 'sales@bookworld.com', 'Boston')
    ]
    conn.executemany('INSERT OR IGNORE INTO suppliers VALUES (?, ?, ?, ?)', suppliers)
    
    # Orders
    orders = [
        (1, 1, '2023-06-01', 1019.98, 'completed'),
        (2, 2, '2023-06-02', 699.99, 'completed'),
        (3, 3, '2023-06-03', 69.98, 'pending'),
        (4, 4, '2023-06-04', 89.99, 'completed'),
        (5, 5, '2023-06-05', 39.99, 'shipped')
    ]
    conn.executemany('INSERT OR IGNORE INTO orders VALUES (?, ?, ?, ?, ?)', orders)
    
    # Order Items
    order_items = [
        (1, 1, 1, 1, 999.99),
        (2, 1, 3, 1, 19.99),
        (3, 2, 2, 1, 699.99),
        (4, 3, 3, 2, 19.99),
        (5, 3, 4, 1, 49.99),
        (6, 4, 6, 1, 89.99),
        (7, 5, 5, 1, 39.99)
    ]
    conn.executemany('INSERT OR IGNORE INTO order_items VALUES (?, ?, ?, ?, ?)', order_items)
    
    # Product Suppliers
    product_suppliers = [
        (1, 1, 1, 800.00),
        (2, 2, 1, 550.00),
        (3, 3, 2, 12.00),
        (4, 4, 2, 30.00),
        (5, 5, 3, 25.00)
    ]
    conn.executemany('INSERT OR IGNORE INTO product_suppliers VALUES (?, ?, ?, ?)', product_suppliers)
    
    # Reviews
    reviews = [
        (1, 1, 1, 5, 'Excellent laptop!', '2023-06-10'),
        (2, 2, 2, 4, 'Good phone, fast delivery', '2023-06-12'),
        (3, 3, 3, 5, 'Perfect fit and quality', '2023-06-15'),
        (4, 5, 5, 4, 'Very informative book', '2023-06-20')
    ]
    conn.executemany('INSERT OR IGNORE INTO reviews VALUES (?, ?, ?, ?, ?, ?)', reviews)

if __name__ == "__main__":
    initialize_db("data_engineering/exp.sqlite")