import os
from fennel_invest_api import Fennel

def main():
    fennel = Fennel()

    # Check if fennel_credentials.pkl exists
    if not os.path.exists('fennel_credentials.pkl'):
        # Authentication process
        email = input("Enter your email: ")

        # Login
        try:
            fennel.login(email=email, wait_for_code=False)
            print("Login successful!")
        except Exception as e:
            print(f"Login failed: {e}")
            print("2FA code required. Please check your email.")
            code = input("Enter 2FA code: ")
            try:
                fennel.login(email=email, wait_for_code=False, code=code)
                print("Login successful!")
            except Exception as e:
                print(f"Login failed: {e}")
                return
    else:
        print("Using existing credentials from fennel_credentials.pkl")

    # Get stock information
    buy_or_sell = input("Do you want to buy or sell? (b/s) ").lower()
    action = "buy" if buy_or_sell == "b" else "sell"
    ticker = input(f"Enter the stock ticker you want to {action}: ").upper()
    quantity = int(input(f"Enter the quantity to {action}: "))

    # Confirmation
    print("\nThis is what you're about to do:")
    print(f"Action: {action.capitalize()}")
    print(f"Stock: {ticker}")
    print(f"Quantity: {quantity}")
    confirm = input("Do you want to proceed? This will place orders on all your accounts (y/n): ").lower()

    if confirm == 'y':
        # Get account IDs and place orders
        account_ids = fennel.get_account_ids()
        for account_id in account_ids:
            try:
                order = fennel.place_order(
                    account_id=account_id,
                    ticker=ticker,
                    quantity=quantity,
                    side=action,
                    price="market",
                    dry_run=False
                )
                print(f"Order placed for account {account_id}:")
                print(order)
            except Exception as e:
                print(f"Failed to place order for account {account_id}: {str(e)}")

        print("All orders have been processed.")
    else:
        print("Order cancelled.")

if __name__ == "__main__":
    main()
