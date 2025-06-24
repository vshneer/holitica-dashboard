import pandas as pd
import numpy as np
from faker import Faker
import random
import uuid



fake = Faker()

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

def simulate_for_segmentation(num_users, num_products, num_transactions):

    # Generate users
    genders = ['Male', 'Female']
    countries = ['USA', 'UK', 'Germany', 'France', 'Canada']
    traffic_sources = ['Instagram', 'Google', 'Direct', 'Facebook', 'Email']
    devices = ['Mobile', 'Desktop', 'Tablet']

    users = []
    user_to_order = {}
    for i in range(num_users):
        user_id = f"U{str(i).zfill(4)}"
        user_to_order[user_id] = [str(uuid.uuid4()) for _ in range(np.random.randint(1, 25))]
        age = np.random.randint(18, 65)
        gender = random.choice(genders)
        country = random.choice(countries)
        traffic_source = random.choice(traffic_sources)
        device = random.choice(devices)
        users.append([user_id, age, gender, country, traffic_source, device])

    users_df = pd.DataFrame(users, columns=['user_id', 'age', 'gender', 'country', 'traffic_source', 'device'])
    # Generate products
    categories = ['Beauty', 'Tech', 'Home', 'Fashion', 'Sportswear']
    products = []
    for i in range(num_products):
        product_id = f"P{str(i).zfill(3)}"
        category = random.choice(categories)
        price = round(np.random.uniform(5, 100), 2)
        products.append([product_id, category, price])

    products_df = pd.DataFrame(products, columns=['product_id', 'category', 'price'])

    # Generate transactions
    transactions = []
    for _ in range(num_transactions):
        user = users_df.sample(1).iloc[0]
        product = products_df.sample(1).iloc[0]
        quantity = np.random.randint(1, 25)
        timestamp = fake.date_time_between(start_date='-6M', end_date='now')
        transactions.append([
            user['user_id'],
            random.choice(user_to_order[user['user_id']]),
            product['product_id'],
            product['category'],
            quantity,
            product['price'],
            quantity * product['price'],
            timestamp
        ])

    transactions_df = pd.DataFrame(transactions, columns=['user_id', 'order_id', 'product_id', 'category', 'quantity', 'price', 'total_price', 'timestamp'])
    return transactions_df.merge(users_df, on='user_id')