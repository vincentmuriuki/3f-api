users_table = """
CREATE TABLE IF NOT EXISTS users (
    user_id serial, 
    username VARCHAR(25) NOT NULL,
    email VARCHAR(25) NOT NULL,
    password VARCHAR(20) NOT NULL,
    address VARCHAR(20) NOT NULL,
    type VARCHAR(20) NOT NULL
)
"""

meals_table = """
CREATE TABLE IF NOT EXISTS meals (
    name VARCHAR(25) NOT NULL,
    description VARCHAR(25) NOT NULL,
    price 
)
"""