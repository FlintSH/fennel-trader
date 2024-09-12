import os
import json
from fennel_invest_api import Fennel

def save_email(email):
    with open('user_data.json', 'w') as f:
        json.dump({'email': email}, f)

def load_email():
    if os.path.exists('user_data.json'):
        with open('user_data.json', 'r') as f:
            data = json.load(f)
            return data.get('email')
    return None

def main():
    fennel = Fennel()

    # Check if email is saved
    saved_email = load_email()
    if saved_email:
        use_saved = input(f"Use saved email ({saved_email})? (y/n): ").lower() == 'y'
        email = saved_email if use_saved else input("Enter your email: ")
    else:
        email = input("Enter your email: ")

    # Login
    try:
        fennel.login(email=email, wait_for_2fa=False)
    except Exception as e:
        print("2FA required. Please check your email.")
        code = input("Enter 2FA code: ")
        fennel.login(email=email, wait_for_2fa=False, code=code)

    # Ask to save email
    if email != saved_email:
        save_login = input("Save login for future use? (y/n): ").lower() == 'y'
        if save_login:
            save_email(email)

    # Get stock information
    ticker = input("Enter the stock ticker you want to buy: ").upper()
    quantity = int(input("Enter the quantity to buy: "))

    # Get account IDs and place orders
    account_ids = fennel.get_account_ids()
    for account_id in account_ids:
        try:
            order = fennel.place_order(
                account_id=account_id,
                ticker=ticker,
                quantity=quantity,
                side="buy",
                price="market",
                dry_run=False
            )
            print(f"Order placed for account {account_id}:")
            print(order)
        except Exception as e:
            print(f"Failed to place order for account {account_id}: {str(e)}")

    print("All orders have been processed.")

if __name__ == "__main__":
    main()
