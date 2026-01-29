import sys
from db import init_database
from auth import register_user, login_user
from banking import (
    get_balance,
    deposit,
    withdraw,
    transfer,
    get_transfer_history
)


def display_menu(username):
    """Display banking menu"""
    print('\n' + '=' * 40)
    print(f'Welcome, {username}')
    print('=' * 40)
    print('1. Check balance')
    print('2. Deposit')
    print('3. Withdraw')
    print('4. Transfer')
    print('5. Transaction History')
    print('6. Log out')
    print('=' * 40)


def get_valid_amount(prompt):
    """Safely get a positive float amount"""
    try:
        amount = float(input(prompt))
        if amount <= 0:
            print('Amount must be greater than zero.')
            return None
        return amount
    except ValueError:
        print('Invalid amount.')
        return None


def main_menu(user_id, username):
    """Main banking menu after login"""
    while True:
        display_menu(username)
        choice = input('Enter an action (1-6): ').strip()

        if choice == '1':
            balance = get_balance(user_id)
            if balance is not None:
                print(f'Your current balance is: ${balance:.2f}')

        elif choice == '2':
            amount = get_valid_amount('Enter amount to deposit: $ ')
            if amount:
                deposit(user_id, amount)

        elif choice == '3':
            amount = get_valid_amount('Enter amount to withdraw: $ ')
            if amount:
                withdraw(user_id, amount)

        elif choice == '4':
            to_username = input('Enter recipient username: ').strip()
            amount = get_valid_amount('Enter amount to transfer: $ ')
            if amount:
                transfer(user_id, to_username, amount)

        elif choice == '5':
            transactions = get_transfer_history(user_id)
            if transactions:
                print('\n' + '=' * 60)
                print('Transaction History')
                print('=' * 60)
                for tx_type, amount, description, created_at in transactions:
                    print(f'{created_at} | {tx_type} | ${amount:.2f} | {description}')
                print('=' * 60)
            else:
                print('No transactions found.')

        elif choice == '6':
            print(f'Logged out. Goodbye, {username}!')
            break

        else:
            print('Invalid option. Please choose between 1–6.')


def main():
    """Main application menu"""
    print('\n' + '=' * 40)
    print('Mega Bank - CLI Application')
    print('=' * 40)
    print('1. Login')
    print('2. Register')
    print('3. Exit')

    choice = input('\nChoose an option (1-3): ').strip()

    if choice == '1':
        username = input('Username: ').strip()
        password = input('Password: ').strip()
        user_id = login_user(username, password)

        if user_id:
            print('Login successful!')
            main_menu(user_id, username)
        else:
            print('Invalid username or password.')

    elif choice == '2':
        username = input('Choose a username: ').strip()
        password = input('Choose a password: ').strip()
        register_user(username, password)

    elif choice == '3':
        print('Thank you for using Mega Bank!')
        sys.exit(0)

    else:
        print('Invalid choice. Please select 1–3.')


if __name__ == "__main__":
    init_database()
    while True:
        main()
