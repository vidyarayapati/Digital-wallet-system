import sqlite3
import hashlib
import random
import sys
import os

# ================= DATABASE SETUP =================
DB_PATH = os.path.join(os.path.dirname(__file__), 'wallet.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            pin_hash TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0.0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            related_username TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

# ================= AUTHENTICATION FUNCTIONS =================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, pin):
    if not username or not password or not pin:
        return False, "Fields cannot be empty."
    hashed_pw = hash_password(password)
    hashed_pin = hash_password(pin)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, pin_hash) VALUES (?, ?, ?)",
            (username, hashed_pw, hashed_pin)
        )
        conn.commit()
        return True, "User registered successfully."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

def login_user(username, password):
    hashed_pw = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and user['password_hash'] == hashed_pw:
        return dict(user), "Login successful!"
    elif not user:
        return None, "User not found."
    else:
        return None, "Incorrect password."

def verify_pin(user_id, pin):
    hashed_pin = hash_password(pin)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pin_hash FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result and result['pin_hash'] == hashed_pin

# ================= WALLET FUNCTIONS =================
def get_balance(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result['balance'] if result else 0.0

def add_funds(user_id, amount):
    if amount <= 0:
        return False, "Amount must be greater than zero."
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, user_id))
        cursor.execute(
            "INSERT INTO transactions (user_id, type, amount) VALUES (?, ?, ?)",
            (user_id, 'DEPOSIT', amount)
        )
        conn.commit()
        return True, f"Successfully added ${amount:.2f}"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def transfer_funds(sender_id, receiver_username, amount):
    if amount <= 0:
        return False, "Amount must be greater than zero."
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT username, balance FROM users WHERE id = ?", (sender_id,))
        sender = cursor.fetchone()
        if sender['balance'] < amount:
            return False, "Insufficient balance."
        if sender['username'] == receiver_username:
            return False, "Cannot send to yourself."
        cursor.execute("SELECT id FROM users WHERE username = ?", (receiver_username,))
        receiver = cursor.fetchone()
        if not receiver:
            return False, "Receiver not found."
        receiver_id = receiver['id']
        sender_username = sender['username']
        # Deduct sender
        cursor.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, sender_id))
        cursor.execute(
            "INSERT INTO transactions (user_id, type, amount, related_username) VALUES (?, ?, ?, ?)",
            (sender_id, 'TRANSFER_OUT', amount, receiver_username)
        )
        # Add receiver
        cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, receiver_id))
        cursor.execute(
            "INSERT INTO transactions (user_id, type, amount, related_username) VALUES (?, ?, ?, ?)",
            (receiver_id, 'TRANSFER_IN', amount, sender_username)
        )
        conn.commit()
        # Cashback logic
        cashback_val = 0.0
        if random.random() < 0.30:
            cb_percent = random.uniform(0.01, 0.05)
            cashback_val = round(amount * cb_percent, 2)
            if cashback_val > 0:
                cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (cashback_val, sender_id))
                cursor.execute(
                    "INSERT INTO transactions (user_id, type, amount, related_username) VALUES (?, ?, ?, ?)",
                    (sender_id, 'CASHBACK', cashback_val, 'System Reward')
                )
                conn.commit()
        msg = f"Transferred ${amount:.2f} to {receiver_username}"
        if cashback_val > 0:
            msg += f" | Cashback: ${cashback_val:.2f}"
        return True, msg
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

def get_transaction_history(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    data = cursor.fetchall()
    conn.close()
    return data

# ================= MAIN MENU & LOOP =================
def main():
    init_db()
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            username = input("Username: ")
            password = input("Password: ")
            pin = input("4-digit PIN: ")
            print(register_user(username, password, pin)[1])
        elif choice == '2':
            username = input("Username: ")
            password = input("Password: ")
            user, msg = login_user(username, password)
            print(msg)
            if user:
                while True:
                    print("\n1. Balance\n2. Add Funds\n3. Transfer\n4. History\n5. Logout")
                    c = input("Choice: ")
                    if c == '1':
                        print(f"Balance: ${get_balance(user['id']):.2f}")
                    elif c == '2':
                        try:
                            amt = float(input("Amount: "))
                            print(add_funds(user['id'], amt)[1])
                        except:
                            print("Invalid amount")
                    elif c == '3':
                        pin = input("Enter PIN: ")
                        if verify_pin(user['id'], pin):
                            r = input("Receiver: ")
                            try:
                                amt = float(input("Amount: "))
                                print(transfer_funds(user['id'], r, amt)[1])
                            except:
                                print("Invalid amount")
                        else:
                            print("Incorrect PIN")
                    elif c == '4':
                        history = get_transaction_history(user['id'])
                        for t in history:
                            print(dict(t))
                    elif c == '5':
                        break
        elif choice == '3':
            sys.exit()

if __name__ == "__main__":
    main()