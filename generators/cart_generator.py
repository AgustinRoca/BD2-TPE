import argparse
from numpy import random

# Some constants
MIN_AMOUNT = 1
MAX_AMOUNT = 15
FILENAME = "./data/carts.csv"


# Function to generate the carts information
def generate_carts(cart_amount, user_amount, product_amount):
    data = []
    users = {}
    for i in range(1, user_amount + 1):
        users[i] = set(())

    # Generates random arrays with the information
    u = random.randint(1, user_amount, cart_amount)
    a = random.randint(MIN_AMOUNT, MAX_AMOUNT, cart_amount)

    # Fills the data array with the information
    for i in range(cart_amount):
        ok = False
        while not ok:
            p = random.randint(1, product_amount)
            if not (p in users[u[i]]):
                ok = True
                users[u[i]].add(p)
        data.append([u[i], p, a[i]])
    return data


# Function to save the data to a file
def save_carts(filename, data):
    f = open(filename, 'w')

    # Adding the randomly generated information
    for d in data:
        f.write('{};{};{}\n'.format(d[0], d[1], d[2]))
    f.close()


# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Main program for BD2 TPE")

    # add arguments
    parser.add_argument('-c', dest='cart_amount', required=True)
    parser.add_argument('-u', dest='user_amount', required=True)
    parser.add_argument('-p', dest='product_amount', required=True)
    args = parser.parse_args()

    # Convert params into an integer
    cart_amount = int(args.cart_amount)
    user_amount = int(args.user_amount)
    product_amount = int(args.product_amount)

    # Genrate and store the info
    data = generate_carts(cart_amount, user_amount, product_amount)
    save_carts(FILENAME, data)


# call main
if __name__ == '__main__':
    main()
