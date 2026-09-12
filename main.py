from src.generators import (
    generate_accounts,
    generate_atm,
    generate_branches,
    generate_cards,
    generate_customers,
    generate_employees,
    generate_loan_types,
    generate_loans,
    generate_transaction_details,
    generate_transaction_status,
    generate_transactions
)

def run_pipe():
    print('The pipeline was started')

    active_branches_ids = generate_branches()
    active_employee_ids = generate_employees(branches_ids=active_branches_ids)
    active_atm_ids = generate_atm(branches_ids=active_branches_ids)
    active_customers_ids = generate_customers(branches_ids=active_branches_ids)
    active_cards_ids = generate_cards(customers_ids= active_customers_ids)
    active_loan_types_ids = generate_loan_types()
    active_loans_ids = generate_loans(customers_ids=active_customers_ids, branches_ids= active_branches_ids, loan_types_ids= active_loan_types_ids)
    active_accounts_numbers = generate_accounts(customers_ids=active_customers_ids)
    active_transactions_ids = generate_transactions(accounts=active_accounts_numbers)
    active_transaction_details_ids = generate_transaction_details(transactions_ids=active_transactions_ids)
    active_transaction_status_ids = generate_transaction_status(active_transactions_ids)

    print('Complete succesfully!')

if __name__ == "__main__":
    run_pipe()