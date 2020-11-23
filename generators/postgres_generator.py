import psycopg2 as psycopg2
from faker import Faker
from faker_commerce import Provider

fake = Faker()
fake.add_provider(Provider)

conn = psycopg2.connect(
    host="localhost",
    port=5433,
    database="latambox",
    user="postgres",
    password="postgres"
)


def populate_database(con: psycopg2.extensions.connection):
    transaction = conn.cursor()

    _drop_users_constraints(transaction)
    for i in range(1, 15000):
        _generate_users(transaction, i)
    _create_users_constraints(transaction)

    conn.commit()
    transaction.close()

    transaction = conn.cursor()

    _drop_products_constraints(transaction)
    for i in range(1, 1000000):
        _generate_products(transaction, i)
    _create_products_constraints(transaction)

    conn.commit()
    transaction.close()

    # transaction = conn.cursor()
    # for i in range(1, 1000000):
    #     _generate_carts(transaction)
    # conn.commit()
    # transaction.close()


def _drop_users_constraints(transaction):
    transaction.execute(
        """
            ALTER TABLE public.users DROP CONSTRAINT IF EXISTS users_pkey;
        """
    )


def _create_users_constraints(transaction):
    transaction.execute(
        """
            ALTER TABLE public.users ADD CONSTRAINT users_pkey PRIMARY KEY (id);
        """
    )


def _drop_products_constraints(transaction):
    transaction.execute(
        """
            ALTER TABLE public.products DROP CONSTRAINT IF EXISTS products_pkey;
        """
    )


def _create_products_constraints(transaction):
    transaction.execute(
        """
            ALTER TABLE public.products ADD CONSTRAINT products_pkey PRIMARY KEY (id);
        """
    )


def _drop_carts_constraints(transaction):
    transaction.execute(
        """
            ALTER TABLE public.carts DROP CONSTRAINT IF EXISTS carts_pkey;
            ALTER TABLE public.carts DROP CONSTRAINT IF EXISTS carts_product_id_fkey;
            ALTER TABLE public.carts DROP CONSTRAINT IF EXISTS carts_user_id_fkey;
        """
    )


def _create_carts_constraints(transaction):
    transaction.execute(
        """
            ALTER TABLE public.carts ADD CONSTRAINT carts_pkey PRIMARY KEY (product_id, user_id);
            ALTER TABLE public.carts ADD FOREIGN KEY (product_id) REFERENCES products(id);
            ALTER TABLE public.carts ADD FOREIGN KEY (user_id) REFERENCES users(id);
        """
    )


def _generate_products(transaction, i):
    product = {
        'id': i,
        'title': fake.ecommerce_name(),
        'description': fake.text(max_nb_chars=200),
        'price': fake.ecommerce_price()
    }

    transaction.execute(
        """
            INSERT INTO public.products (id, title, description, price) 
                VALUES (%(id)s, %(title)s, %(description)s, %(price)s);
        """,
        product
    )


def _generate_users(transaction, i):
    product = {
        'id': i,
        'full_name': fake.name()
    }

    transaction.execute(
        """
            INSERT INTO public.users (id, full_name) VALUES (%(id)s, %(full_name)s);
        """,
        product
    )


# def _generate_carts(transaction, i):
#     product = {
#         'product_id': i,
#         'user_id': fake.name()
#     }
#
#     transaction.execute(
#         """
#             INSERT INTO public.users (id, full_name) VALUES ({}, '{}');
#         """.format(product['id'], product['full_name'])
#     )
