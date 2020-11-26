CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY,
    full_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY,
    title text NOT NULL,
    description text NOT NULL,
    price INT NOT NULL
);

CREATE TABLE IF NOT EXISTS carts (
    product_id INT,
    user_id INT,
    quantity INT NOT NULL,
    UNIQUE(user_id, product_id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    PRIMARY KEY (product_id, user_id)
);
