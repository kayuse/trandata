import json
import random
import time

from faker import Faker
import uuid
import requests
from datetime import datetime

faker = Faker()

Username = "ifedamilola2009@gmail.com"
Password = "123@ifeDAM567"
BaseUrl = "https://testdapdeel-dcc9cyd7gsgkgvf8.eastus-01.azurewebsites.net/api/"


def login():
    h = {
        "Content-Type": "application/json"
    }

    record = dict()
    record["Username"] = Username
    record["Password"] = Password
    response = requests.post(BaseUrl + "auth/login", data=json.dumps(record), headers=h)
    if response.status_code == 200:
        result = response.json()
        return result['data']['token']


Token = str(login())
headers = {
    "Authorization": "Bearer " + Token,
    "Content-Type": "application/json"
}


def get_banks():
    response = requests.get(BaseUrl + "bank/all", headers=headers)
    if response.status_code == 200:
        return response.json()['data']


banks = get_banks()


def generate_customer():
    bank = random.choice(banks)
    return {
        "email": faker.email(),
        "customerId": str(uuid.uuid4()),
        "name": faker.name(),
        "phone": faker.phone_number(),
        "Device": {
            "DeviceId": faker.uuid4(),
            "ipAddress": faker.ipv4(),
            "deviceType": random.randint(0, 5)
        },
        "account": {
            "accountNumber": faker.iban(),
            "bankCode": bank['code'],
            "country": "NGN"
        }
    }


def pick_random_customer():
    return random.choice(customers)


def post(t):
    data = t
    response = requests.post(BaseUrl + "transfer/Ingest",
                             headers=headers, json=t)
    return response


def generate_transaction():
    from_customer = pick_random_customer()
    to_customer = pick_random_customer()
    while from_customer["customerId"] == to_customer["customerId"]:
        to_customer = pick_random_customer()

    transaction_type = random.choice(["WITHDRAWAL", "TRANSFER"])

    amount = 0
    rand_num = random.random()
    if rand_num < 0.80:
        amount = random.randint(100, 1000000)
    elif rand_num < 0.95:
        amount = random.randint(1000000, 5000000)
    else:
        amount = random.randint(5000000, 10000000)
    t = {
        "debitCustomer": from_customer,
        "creditCustomer": to_customer,
        "transaction": {
            "transactionId": str(uuid.uuid4()),
            "amount": amount,
            "TransactionDate": faker.date_time_this_decade().strftime("%Y-%m-%d %H:%M:%S"),
            "description": faker.sentence(),
            "type": transaction_type
        },
        "ObservatoryId": 1
    }
    print(t)
    time.sleep(5)
    response = post(t)
    if response.status_code == 200:
        print(response.json())
    print(response.status_code)
    return response

    # Token, RefreshToken = refresh_token(Token, RefreshToken)


print("Starting")

customers = [generate_customer() for _ in range(100000)]

for _ in range(5000000):
    generate_transaction()

# with open('transactions.json', 'w') as f:
#     json.dump(transactions, f)

print("Data generation complete.")
