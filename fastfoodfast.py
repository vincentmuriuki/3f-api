users_table = """
CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY, 
    username VARCHAR(55) NOT NULL,
    email VARCHAR(55) NOT NULL,
    password VARCHAR(255) NOT NULL,
    address VARCHAR(25) NOT NULL,
    is_admin boolean DEFAULT false
)
"""

meals_table = """
CREATE TABLE IF NOT EXISTS meals (
    name VARCHAR(25) UNIQUE NOT NULL,
    description VARCHAR(25) NOT NULL,
    price INT NOT NULL,
    meal_id serial PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (category_name) REFERENCES categories (category_name)
)
"""

category_table = """
CREATE TABLE IF NOT EXISTS categories (
 category_id serial PRIMARY KEY,
 category_name VARCHAR(25) UNIQUE NOT NULL
)
"""

orders_table = """
CREATE TABLE IF NOT EXISTS orders (
    order_id serial PRIMARY KEY,
    user_id INT NOT NULL,
    meal VARCHAR(35) UNIQUE NOT NULL,
    ordered_date VARCHAR(99) NOT NULL,
    delivered_date VARCHAR(99),
    price INT NOT NULL,
    qty INT NOT NULL,
    amount INT NOT NULL,
    status VARCHAR(25) NOT NULL,
    description VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (meal) REFERENCES meals (name)
)
"""

blacklist = """
CREATE TABLE IF NOT EXISTS blacklist (
    token_id serial PRIMARY KEY,
    user_tokens character varying(900) NOT NULL
) 
"""

queries = [users_table, category_table, meals_table, orders_table, blacklist]
