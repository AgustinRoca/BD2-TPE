DROP TABLE IF EXISTS carts;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY,
    full_name TEXT NOT NULL
);

create sequence users_id_seq;

alter table users alter column id set default nextval('public.users_id_seq');

alter sequence users_id_seq owned by users.id;

CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY,
    title text NOT NULL,
    description text NOT NULL,
    price INT NOT NULL
);

create sequence products_id_seq;

alter table products alter column id set default nextval('public.products_id_seq');

alter sequence products_id_seq owned by products.id;

CREATE TABLE IF NOT EXISTS carts (
    product_id INT,
    user_id INT,
    quantity INT NOT NULL,
    UNIQUE(user_id, product_id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    PRIMARY KEY (product_id, user_id)
);

COPY users(id, full_name)
FROM '/users.csv'
DELIMITER ';'
CSV HEADER;

COPY products(id, title, description, price)
FROM '/products.csv'
DELIMITER ';'
CSV HEADER;