import sys
from db import init_database
from auth import register_user, login_user
from banking import get_balance, deposit, withdraw, transfer, get_transfer_history


def display_menu(username):
    '''Display main menu'''
    print('\n' + '=' * 40)
    print(f'Welcome {username}')
    print('=' * 40)
    
    print('1. Check balance')
    print('2. Deposit')
    print('3. Withdraw')
    print('4. Transfer')
    print('5. Transaction History')
    print('6. Log out')
    
    print('=' * 40)
    
def main_menu(user_id, username): 
    '''Main banking menu after logging in'''
    while True:
        display_menu(username)
        choice = input('Enter an action to perform (1-6): ')
        if choice == '1':
            balance = get_balance(user_id)
            if balance is not None:
                print(f'Your current balance is ${balance:.2f}')
                
        elif choice == '2':
            try:
                amount = float(input("Enter amount to deposit: $ "))
                deposit(user_id, amount)
            except ValueError:
                print('Invalid Amount')
        elif choice == '3':
            try:
                amount = float(input('Enter amount to withdraw: $ '))
                withdraw(user_id, amount)
            except ValueError:
                print('Invalid Amount')
                
        elif choice == '4':
            to_username = input('Enter recipient user: ')
            try:
                amount = float(input('Enter amount to transfer: $ '))
                transfer(user_id, to_username, amount)
            except ValueError:
                print('Invalid Amount')
            
        elif choice == '5':
            transactions = get_transfer_history()
            if transactions:
                print('\n' + "=" * 60)
                print('Transaction History')
                print('\n' + "=" * 60)
                for tx in transactions:
                    tx_type, amount, description, create_at = tx
                    print(f'{create_at} | {tx_type} | $ {amount:.2f} | {description}') 
                print('=' * 60)
            else:
                print('No transactions found')
                
        elif choice == '6':
            print(f'Goodbye, {username}')   
            
        else:
            print('Invalid Option! Please choose in range (1-6).')        
        


def main():
    print('\n' + '=' * 40)
    print('Mega Bank - CLI application system')
    print('=' * 40)

    print('1. Login')
    print('2. Register')
    print('3. Exit')

    choice = input('\nChoose from 1-3: ').strip()

    if choice == '1':
        username = input('Enter username: ')
        password = input('Enter password: ')
        user_id = login_user(username, password)

        if user_id:
            print('Login successful!')
            main_menu(user_id, username)
        else:
            print('Invalid username or password.')

    elif choice == '2':
        username = input('Choose a username: ')
        password = input('Choose a password: ')
        register_user(username, password)

    elif choice == '3':
        print('Thank you for using Mega Bank!')
        sys.exit(0)

    else:
        print('Invalid option! please choose (1-3).')



if __name__ == "__main__":
    init_database()
    while True:
        main()
