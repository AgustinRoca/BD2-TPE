from faker import Faker
from faker_commerce import Provider
import argparse

# Some constants
FILENAME_USERS = "../data/users.csv"
FILENAME_PRODUCTS = "../data/products.csv"


# GENERATION

def generate_users(user_amount, fake):
    users = []
    portion = int(user_amount / 10)
    counter = 1
    for i in range(1, user_amount + 1):
        if i % portion == 0:
            print(counter * 10, "% Completed")
            counter += 1
        users.append((i, fake.name()))
    return users


def generate_products(product_amount, fake):
    products = []
    portion = int(product_amount / 10)
    counter = 1
    for i in range(1, product_amount + 1):
        if i % portion == 0:
            print(counter * 10, "% Completed")
            counter += 1
        products.append((i, fake.ecommerce_name(), fake.text(max_nb_chars=200).replace('\n', '').replace('\t', ''), fake.ecommerce_price()))
    return products


# SAVING

def save_users(data, filename=FILENAME_USERS):
    f = open(filename, 'w')
    f.write('id;full_name\n')
    for d in data:
        f.write('{};{}\n'.format(d[0], d[1]))
    f.close()


def save_products(data, filename=FILENAME_PRODUCTS):
    f = open(filename, 'w')
    f.write('id;title;description;price\n')
    for d in data:
        f.write('{};{};{};{}\n'.format(d[0], d[1], d[2], d[3]))
    f.close()


# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Main program for BD2 TPE")

    # add arguments
    parser.add_argument('-u', dest='user_amount', required=True)
    parser.add_argument('-p', dest='product_amount', required=True)
    args = parser.parse_args()

    # Creating Faker instance
    fake = Faker()
    fake.add_provider(Provider)

    # Convert params into an integer
    user_amount = int(args.user_amount)
    product_amount = int(args.product_amount)

    # Generating and storing the info
    print("Generating users...")
    # users = generate_users(user_amount, fake)
    print("Generating products...")
    products = generate_products(product_amount, fake)
    print("Saving users...")
    # save_users(users)
    print("Saving products...")
    save_products(products)


# call main
if __name__ == '__main__':
    main()
