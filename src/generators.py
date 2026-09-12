import random
import os
import pandas as pd
from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import create_engine
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

load_dotenv()
DB_URL = os.getenv("DB_URL")

fake = Faker('en_US')

engine = create_engine(DB_URL)

SPENDING_PROFILES = ['Low', 'Medium', 'High']
SPENDING_WEIGHTS = [0.6, 0.3, 0.1]
PROFILE_RANGES = {'Low': (100,500), 'Medium': (500, 6000), 'High': (6000, 50000)}

def generate_branches(num_branches: int = 5) -> list[int]:
    branches_data = []

    for branch_id in range (1, num_branches + 1):
        city = fake.city()
        clear_city = city.lower().replace(' ', '_').replace('-', '_')     
        branch = {
            'branch_id': branch_id,
            'branch_name': f'Main branch - {city}',
            'location': fake.street_address() + ', ' + f'{city}',
            'branch_phone': fake.numerify('+1 (###) ###-##-##'),
            'branch_email': f'branch_{clear_city}@{fake.domain_name()}',
            'manager_id': None,
            'operating_hours': ' 07:00 AM - 06:00 PM'
        }
        branches_data.append(branch)

    df_branches = pd.DataFrame(branches_data)
    df_branches.to_sql(name='branches', con=engine, index= False, if_exists='append')
    print(f'Succesfully added branches: {len(df_branches)}')
    return df_branches['branch_id'].tolist()
   
def generate_employees(branches_ids: list[int], num_employees: int = 25) -> list[int]:
    positions = [
            "Teller",
            "Loan Officer",
            "Branch Manager",
            "Financial Advisor",
            "Customer Service Rep"
    ]
    qualifications = ["Bachelor", "Master", "Associate Degree", "High School", "PhD"]
    employees_data = []

    for employee_id in range (1, num_employees + 1):
        gender = random.choice(['M', 'F'])
        first_name = fake.first_name_male() if gender == 'M' else fake.first_name_female()
        last_name = fake.last_name()
        
        employee = {
            'employee_id': employee_id,
            'name': first_name + ' ' + last_name,
            'branch_id': random.choice(branches_ids),
            'position': random.choice(positions),
            'emp_phone': fake.numerify('+1(###)###-##-##'),
            'emp_email': f'{first_name.lower()}_{last_name.lower()}_{employee_id}@{fake.domain_name()}'[:50],
            'gender': gender,
            'hire_date': fake.date_between(start_date='-5y', end_date='today'),
            'qualification':random.choice(qualifications)
        }
        employees_data.append(employee)

    df_employees = pd.DataFrame(employees_data)
    df_employees.to_sql(name='employees', con=engine, if_exists='append', index=False)
    print(f'Successfully added employees: {len(df_employees)} ✅')
    return df_employees['employee_id'].tolist()

def generate_atm(branches_ids: list[int], num_atms: int = 10) -> list[int]:
    atms_data = []
    status = ['Active', 'Under Maintenance', 'Out of Service']

    for atm_id in range(1, num_atms + 1):
        atm = {
            'atm_id': atm_id,
            'branch_id': random.choice(branches_ids),
            'location': fake.street_address(),
            'status': random.choice(status),
            'operating_hours': '24/7',
            'supported_transactions': 'withdraw/deposit'
        }
        atms_data.append(atm)

    df_atms = pd.DataFrame(atms_data)
    df_atms.to_sql(name='atm', con=engine, if_exists='append', index=False)
    print(f'Successfully added atms: {len(df_atms)} ✅')
    return df_atms['atm_id'].tolist()

def generate_customers(branches_ids: list[int], num_customers: int = 100) -> list[int]:
    customers_data = []

    for customer_id in range(1, num_customers + 1):
        gender = random.choice(['M', 'F'])
        first_name = fake.first_name_male() if gender == 'M' else fake.first_name_female()
        last_name = fake.last_name()
        city = fake.city()
        state = fake.state()
        raw_ssn = fake.ssn()

        customer = {
            'customer_id': customer_id,
            'branch_id': random.choice(branches_ids),
            'first_name': first_name,
            'last_name': last_name,
            'address': fake.street_address() + ' ' + city,
            'city': city,
            'gender': gender,
            'state': state,
            'country': 'United States',
            'phone': fake.numerify('+1(###)###-##-##'),
            'email': f'{first_name}{last_name}@{fake.domain_name()}'[:50],
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=85),
            'ssn': f"***-**-{raw_ssn[-4:]}"
        }
        customers_data.append(customer)

    df_customers = pd.DataFrame(customers_data)
    df_customers.to_sql(name='customers', con= engine , if_exists='append', index=False)
    print(f'Successfully added customers: {len(customers_data)} ✅')
    return df_customers['customer_id'].tolist()

def generate_cards(customers_ids: list[int], num_cards: int = 50) -> list[int]:
    cards_data = []

    for card_id in range(1, num_cards + 1):

        card_type = ['Debit', 'Credit', 'Personal']
        status = ['Closed', 'Active', 'Frozen']

        card = {
            'card_number':fake.credit_card_number(card_type='visa'),
            'customer_id': random.choice(customers_ids),
            'card_type': random.choice(card_type),
            'exp_date': fake.date_between(start_date='today', end_date='+4y'),
            'card_status': random.choice(status)
        }
        cards_data.append(card)

    df_cards = pd.DataFrame(cards_data)
    df_cards.to_sql(name='cards', con=engine, if_exists= 'append', index=False)
    print(f'Successfully added cards: {len(cards_data)} ✅')
    return df_cards['card_number'].tolist()

def generate_loan_types() -> list[int]:
    loan_types_data = []

    categories = [

        {
            'loan_category': 'Mortgage',
            'base_interest_rate': 6.5,
            'base_amount': 250000.0,
            'description': 'Real estate purchase financing'
        },
        {
            'loan_category': 'Student',
            'base_interest_rate': 4.5,
            'base_amount': 20000.0,
            'description': 'Higher education loan'
        },
        {
            'loan_category': 'Auto',
            'base_interest_rate': 8.0,
            'base_amount': 35000.0,
            'description': 'Vehicle financing loan'
        },
        {
            'loan_category': 'Personal',
            'base_interest_rate': 12.5,
            'base_amount': 10000.0,
            'description': 'Unsecured personal loan'
        },
        {
            'loan_category': 'Business',
            'base_interest_rate': 10.0,
            'base_amount': 100000.0,
            'description': 'Commercial growth and equipment loan'
        }

    ]

    for loan_type_id, cat in enumerate(categories, start=1):
        cat['loan_type_id'] = loan_type_id
        loan_types_data.append(cat)

    df_loans_types = pd.DataFrame(loan_types_data)
    df_loans_types.to_sql(name='loan_types', con=engine, index=False, if_exists='append')
    print(f'Succesfully added loan_types ✅')
    return df_loans_types['loan_type_id'].tolist()

def generate_loans(customers_ids: list[int], branches_ids: list[int], loan_types_ids: list[int] , num_loans: int = 55) -> list[int]:

    loans_data = []

    for loan_id in range(1, num_loans + 1):
        start_date = fake.date_between(start_date = '-10y', end_date='today')
        term_months = random.choice([12, 24, 36, 48, 60, 84, 120])
        end_date = start_date + relativedelta(months=term_months)
        today = date.today()
        if end_date < today:
            status = 'CLOSED'
        else:
            status = random.choice(['ACTIVE', 'DEFAULTED', 'PENDING'])

        loan = {
            'loan_id': loan_id,
            'customer_id': random.choice(customers_ids),
            'branch_id': random.choice(branches_ids),
            'loan_amount': random.randint(1000, 100000),
            'status': status,
            'end_date': end_date,
            'start_date': start_date,
            'interest_rate': round(random.uniform(5.49, 24.9), 2),
            'term_months': term_months,
            'loan_type_id': random.choice(loan_types_ids)
        }
        loans_data.append(loan)

    df_loans = pd.DataFrame(loans_data)
    df_loans.to_sql(name='loans', con=engine, index=False, if_exists='append')
    print(f'Successfully added loans: {len(loans_data)} ✅')
    return df_loans['loan_id'].tolist()

def generate_accounts(customers_ids: list[int], num_accounts: int = 50) -> list[dict]:
    accounts_data = []
    account_types = ['Platinum', 'Bronze', 'Silver']
    account_statuses = ['Active', 'Active', 'Active', 'Frozen', 'Closed']

    for account_id in range(1, num_accounts+1):

        registration_date = fake.date_between(start_date = '-4y', end_date='-1y')
        open_date = registration_date

        status = random.choice(account_statuses)

        if status == 'Closed':
            closed_date = fake.date_between(start_date = open_date, end_date='today')
            balance = None
        else:
            closed_date = None
            balance = round(random.uniform(1.0, 300000.0), 2)

        spending_profile = random.choices(SPENDING_PROFILES, SPENDING_WEIGHTS, k=1)[0]
        
        account = {
            'account_number': account_id,
            'customer_id': random.choice(customers_ids),
            'account_type': random.choice(account_types),
            'balance': balance,
            'account_status': status,
            'registration_date': registration_date,
            'open_date': open_date,
            'closed_date': closed_date,
            'spending_profile': spending_profile
        }
        accounts_data.append(account)

    df_accounts = pd.DataFrame(accounts_data)
    df_accounts = df_accounts.drop(columns=['spending_profile'])
    df_accounts.to_sql(name='accounts', con=engine, if_exists='append', index=False)
    print(f'Successfully added accounts: {len(df_accounts)} ✅')
    return accounts_data

def generate_transactions(accounts: list[dict], num_transactions: int = 1000, fraud_account_ratio = 0.03, outlier_ratio=0.015) -> list[dict]:

    usable_accounts = [acc for acc in accounts if acc['account_status'] in ['Active', 'Frozen']]

    fraud_accounts = set(random.sample(
        [acc['account_number'] for acc in usable_accounts],
        k=max(1, int(len(usable_accounts) * fraud_account_ratio))
    ))
    transaction_types = ['Deposit', 'Withdrawal', 'Transfer', 'Payment', 'ATM Withdrawal']
    transactions_data, anomaly_log = [], []
    tx_id = 1

    for acc in usable_accounts:
        low, high = PROFILE_RANGES[acc['spending_profile']]

        for _ in range(max(1, round(num_transactions/len(usable_accounts)))):
            transaction = {
                'transaction_id': tx_id,
                'account_number': acc['account_number'],
                'transaction_type': random.choice(transaction_types),
                'amount': round(random.uniform(low, high), 2),
                'date_time': fake.date_time_between(start_date=acc['open_date'], end_date='now')
            }
            transactions_data.append(transaction)
            tx_id += 1

        if acc['account_number'] in fraud_accounts:
            burst_time = fake.date_time_between(start_date=acc['open_date'], end_date='now')

            for i in range (random.randint(3,6)):
                t = burst_time + timedelta(seconds=random.randint(30, 500) * i)
                transaction = {
                    'transaction_id': tx_id,
                    'account_number': acc['account_number'],
                    'transaction_type': 'Withdrawal',
                    'amount': round(random.uniform(3, 50), 2),
                    'date_time': t
                }
                transactions_data.append(transaction)
                anomaly_log.append({'transaction_id': tx_id, 'anomaly_type': 'velocity_burst'})
                tx_id += 1

        if random.random() < outlier_ratio:
            transaction = {
                'transaction_id': tx_id,
                'account_number': acc['account_number'],
                'transaction_type': random.choice(['Transfer', 'Withdrawal']),
                'amount': round(high * random.randint(5,12), 2),
                'date_time': fake.date_time_between(start_date=acc['open_date'], end_date='now')
            }
            transactions_data.append(transaction)
            anomaly_log.append({'transaction_id': tx_id, 'anomaly_type': 'outlier'})
            tx_id += 1

    df_transactions = pd.DataFrame(transactions_data)
    df_transactions.to_sql(name='transactions', index=False, con=engine, if_exists='append')
    pd.DataFrame(anomaly_log).to_csv('anomaly_ground_truth.csv', index=False)
    print(f'Successfully added transactions: {len(df_transactions)} ✅, injected {len(anomaly_log)}')
    return transactions_data

def generate_transaction_details(transactions_ids: list[dict]) -> list[int]:
    details_data = []

    merchant_category_map = {
        'Amazon': 'Retail',
        'Walmart': 'Retail',
        'Target': 'Retail',
        'Starbucks': 'Food & Dining',
        'McDonalds': 'Food & Dining',
        'Uber': 'Transport',
        'Shell': 'Transport',
        'Netflix': 'Entertainment',
        'Spotify': 'Entertainment',
        'YouTube': 'Entertainment'
    }

    merchants = list(merchant_category_map.keys())
    currencies = ['USD', 'USD', 'USD', 'EUR', 'RSD']
    
    for tx_id in transactions_ids:
        merchant = random.choice(merchants)
        category = merchant_category_map[merchant]
        detail = {
            'transaction_id': tx_id['transaction_id'],
            'description': f'Pay to {merchant}' [:20],
            'merchant_payee': merchant [:20],
            'transaction_category': category [:20],
            'currency': random.choice(currencies) [:20],
            'notes': None
        }
        details_data.append(detail)

    df_transaction_details = pd.DataFrame(details_data)
    df_transaction_details.to_sql(name='transaction_details', con=engine, if_exists= 'append', index= False)
    print(f'Succesfully added transaction details: {len(details_data)} ✅')
    return df_transaction_details['transaction_id'].tolist()    

def generate_transaction_status(transactions: list[dict]) -> list[int]:
    status_data = []

    status_flow = {
        'Completed': [
            'Transaction processed successfully',
            'Funds settled',
            'Approved by issuer',
        ],
        'Pending': [
            'Awaiting merchant settlement',
            'Processing authorization hold',
        ],
        'Failed': [
            'Insufficient funds on account',
            'Daily spending limit exceeded',
            'Card expired or blocked',
        ],
        'Reversed': ['Customer initiated chargeback', 'Merchant refund issued'],
    }

    statuses = ['Completed', 'Pending', 'Failed', 'Reversed']
    status_weights = [0.88, 0.05, 0.05, 0.02]
    
    for status_id, tx in enumerate(transactions, start=1):
        selected_status = random.choices(statuses, weights=status_weights, k=1)[0]
        description = random.choice(status_flow[selected_status])
        status_time = tx['date_time'] + relativedelta(seconds=random.randint(1, 5))

        status = {
            'status_id': status_id,
            'transaction_id': tx['transaction_id'],
            'status_type': selected_status,
            'description': description,
            'time': status_time
        }

        status_data.append(status)

    df_transaction_status = pd.DataFrame(status_data)
    df_transaction_status.to_sql(name='transaction_status', index=False, if_exists='append', con=engine)
    print(f'Succesfully added transactions statuses: {len(status_data)} ✅')
    return df_transaction_status['status_id'].tolist()

