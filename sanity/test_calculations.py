# This Module Tests other modules function 
# Since the File name is main_test.py, It will executed when we run pytest 

import pytest
from app.calculation import add, BankAccount, InsufficientFunds

# Fixtures is like a function that runs before a test case function
@pytest.fixture
def zero_balance_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

# Test Cases with Input and expected output
@pytest.mark.parametrize("input1, input2, output", [
    (5, 4, 9),
    (13, 26, 39),
    (17, 47, 64)
])
# Naming Convetion matters for function name so that 
# auto discovery feature of pytest can find out the block that needs to tested
def test_add(input1, input2, output):
    print("Entered Testing Function!!!")
    assert add(input1, input2) == output


def test_bank_account_zero_balance(zero_balance_bank_account):
    assert zero_balance_bank_account.balance == 0

def test_bank_account_with_balance(bank_account):
    assert bank_account.balance == 50

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 5) == 55

@pytest.mark.parametrize("deposit, withdraw, balance", [
    (75, 4, 121),
    (99, 27, 122)
])
def test_bank_transactions(bank_account, deposit, withdraw, balance):
    bank_account.deposit(deposit)
    bank_account.withdraw(withdraw)
    assert bank_account.balance == balance

@pytest.mark.parametrize("deposit, withdraw, balance", [
    (75, 4, 71),
    (99, 27, 72)
])
def test_zero_balance_bank_transactions(zero_balance_bank_account, deposit, withdraw, balance):
    zero_balance_bank_account.deposit(deposit)
    zero_balance_bank_account.withdraw(withdraw)
    assert zero_balance_bank_account.balance == balance    

# Expecting a general exception scenario
def test_insufficient_funds_1(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(51)

# Expecting a specific exception (standard way) scenario
def test_insufficient_funds_2(bank_account):
    bank_account.deposit(100)
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(151) 