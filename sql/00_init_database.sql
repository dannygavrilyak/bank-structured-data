-- 00_init_database.sql: Core Banking Relational Schema
-- 1. Reset Schema
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;

-- 2. Organization Layer
CREATE TABLE public.branches (
    branch_id SERIAL PRIMARY KEY,
    branch_name VARCHAR(255) NULL,
    location VARCHAR(255) NULL,
    branch_phone VARCHAR(20) NULL,
    branch_email VARCHAR(100) NULL,
    manager_id INT NULL,
    operating_hours VARCHAR(50) NOT NULL
);

CREATE TABLE public.atm (
    atm_id SERIAL PRIMARY KEY,
    branch_id INT REFERENCES public.branches(branch_id),
    location VARCHAR(50) NULL,
    status VARCHAR(20) NULL,
    operating_hours VARCHAR(50) NULL,
    supported_transactions VARCHAR(20) NULL
);

CREATE TABLE public.employees (
    employee_id SERIAL PRIMARY KEY,
    branch_id INT REFERENCES public.branches(branch_id),
    name VARCHAR(50) NULL,
    position VARCHAR(30) NULL,
    emp_phone VARCHAR(20) NULL,
    emp_email VARCHAR(50) NULL,
    gender CHAR(1) NULL,
    hire_date DATE NULL,
    qualification VARCHAR(25) NULL
);

-- 3. Customer & Credit Layer
CREATE TABLE public.customers (
    customer_id SERIAL PRIMARY KEY,
    branch_id INT REFERENCES public.branches(branch_id),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    address VARCHAR(100) NULL,
    city VARCHAR(50) NULL,
    gender CHAR(1) NULL,
    state VARCHAR(50) NULL,
    country VARCHAR(50) NULL,
    phone VARCHAR(20) NULL,
    email VARCHAR(50) NULL,
    date_of_birth DATE NOT NULL,
    ssn VARCHAR(20) NULL
);

CREATE TABLE public.loan_types (
    loan_type_id SERIAL PRIMARY KEY,
    loan_category VARCHAR(50) NOT NULL,
    base_interest_rate NUMERIC(6, 4) NOT NULL,
    base_amount NUMERIC(15, 2) NOT NULL,
    description VARCHAR(255) NULL
);

CREATE TABLE public.loans (
    loan_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES public.customers(customer_id),
    loan_type_id INT REFERENCES public.loan_types(loan_type_id),
    branch_id INT REFERENCES public.branches(branch_id),
    loan_amount NUMERIC(15, 2) NOT NULL,
    interest_rate NUMERIC(6, 4) NOT NULL,
    term_months INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) CHECK (status IN ('ACTIVE', 'CLOSED', 'DEFAULTED', 'PENDING'))
);

-- 4. Accounts & Cards Layer
CREATE TABLE public.accounts (
    account_number SERIAL PRIMARY KEY,
    customer_id INT REFERENCES public.customers(customer_id),
    account_type VARCHAR(20) NULL,
    balance NUMERIC(16, 2) NULL,
    account_status VARCHAR(20) NULL,
    registration_date DATE NULL,
    open_date DATE NULL,
    closed_date DATE NULL,
    spending_profile VARCHAR(10) NOT NULL CHECK (spending_profile IN ('Low', 'Medium', 'High'))
);

CREATE TABLE public.cards (
    card_number VARCHAR(20) PRIMARY KEY,
    customer_id INT REFERENCES public.customers(customer_id),
    card_type VARCHAR(20) NULL,
    exp_date DATE NULL,
    card_status VARCHAR(20) NULL
);

-- 5. Transactions Layer
CREATE TABLE public.transactions (
    transaction_id SERIAL PRIMARY KEY,
    account_number INT NOT NULL REFERENCES public.accounts(account_number),
    transaction_type VARCHAR(20) NULL,
    amount NUMERIC(16, 2) NOT NULL,
    date_time TIMESTAMP NULL
);

CREATE TABLE public.transaction_details (
    transaction_id INT PRIMARY KEY REFERENCES public.transactions(transaction_id),
    description VARCHAR(255) NULL,
    merchant_payee VARCHAR(50) NULL,
    transaction_category VARCHAR(50) NULL,
    currency VARCHAR(20) NULL,
    notes VARCHAR(255) NULL
);

CREATE TABLE public.transaction_status (
    status_id SERIAL PRIMARY KEY,
    transaction_id INT REFERENCES public.transactions(transaction_id),
    status_type VARCHAR(25) NOT NULL,
    description VARCHAR(255) NULL,
    time TIMESTAMP NULL
);