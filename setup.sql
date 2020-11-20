CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY,
    full_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY,
    description VARCHAR(511)
);

CREATE TABLE IF NOT EXISTS carts (
    product_id INT,
    user_id INT,
    quantity INT NOT NULL,
    UNIQUE(user_id, product_id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
