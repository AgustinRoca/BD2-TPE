CREATE TABLE IF NOT EXISTS users (
    id INT,
    full_name VARCHAR(255) NOT NULL
);

ALTER TABLE users ADD CONSTRAINT users_pkey PRIMARY KEY (id);

CREATE TABLE IF NOT EXISTS products (
    id INT,
    title text NOT NULL,
    description text NOT NULL,
    price int NOT NULL
);

ALTER TABLE products ADD CONSTRAINT products_pkey PRIMARY KEY (id);

CREATE TABLE IF NOT EXISTS carts (
    product_id INT,
    user_id INT,
    quantity INT NOT NULL,
    UNIQUE(user_id, product_id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

ALTER TABLE carts ADD CONSTRAINT carts_pkey PRIMARY KEY (product_id, user_id);
ALTER TABLE carts ADD FOREIGN KEY (product_id) REFERENCES products(id);
ALTER TABLE carts ADD FOREIGN KEY (user_id) REFERENCES users(id);
