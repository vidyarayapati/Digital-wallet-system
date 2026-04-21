# 💳 Digital Wallet System (Python + SQLite)

## 📌 Overview
This is a command-line based Digital Wallet System built using Python and SQLite.  
It simulates real-world wallet applications by allowing users to register, login, manage balance, transfer money, and view transaction history securely.

---

## 🚀 Features
- 🔐 User Registration & Login (Password Hashing)
- 💰 Wallet Balance Management
- ➕ Add Funds
- 🔁 Transfer Money Between Users
- 🔒 PIN Verification for Transactions
- 📊 Transaction History
- 🎁 Cashback System (Random Rewards)

---

## 🛠️ Tech Stack
- Python
- SQLite
- Hashlib (for encryption)
- Random module

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/digital-wallet.git
cd digital-wallet
2. Run the program
python wallet.py
🗄️ Database
SQLite database (wallet.db) is automatically created
Tables:
users
transactions
📸 Sample Output
1. Register
2. Login
3. Exit
Enter choice:
📚 What I Learned
Database integration with Python (SQLite)
Writing modular and reusable functions
Implementing secure authentication using hashing
Handling transactions and maintaining data consistency
Using exception handling for error management
🔮 Future Improvements
GUI using Tkinter or Web version using Flask
Email/SMS notifications
Advanced security features
Admin dashboard
🤝 Contributing

Feel free to fork this project and improve it!

📬 Contact

For suggestions or feedback, connect with me on LinkedIn.


---

If you want, I can also:
- :contentReference[oaicite:0]{index=0}
- :contentReference[oaicite:1]{index=1}
- Or :contentReference[oaicite:2]{index=2} 👍
README.md
for post in github

Here’s a polished README.md (GitHub-ready) you can directly paste 👇

# 💳 Digital Wallet System

A command-line based Digital Wallet application built using Python and SQLite.  
This project simulates basic features of real-world payment apps like user authentication, balance management, and secure money transfers.

---

## 🚀 Features
- 🔐 User Registration & Login (Password Hashing using SHA-256)
- 💰 Wallet Balance Management
- ➕ Add Funds
- 🔁 Transfer Money Between Users
- 🔒 PIN-based Transaction Verification
- 📊 Transaction History Tracking
- 🎁 Cashback System (1%–5% with 30% probability)

---

## 🛠️ Tech Stack
- **Language:** Python  
- **Database:** SQLite  
- **Libraries:** hashlib, random, os, sys  

---

## 📂 Project Structure

digital-wallet/
│── wallet.py # Main application file
│── wallet.db # SQLite database (auto-created)


---

## ⚙️ How to Run

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/digital-wallet.git
cd digital-wallet
2️⃣ Run the Application
python wallet.py
🗄️ Database Details

The application automatically creates a database (wallet.db) with:

Users Table
id
username
password_hash
pin_hash
balance
Transactions Table
id
user_id
type (DEPOSIT, TRANSFER_IN, TRANSFER_OUT, CASHBACK)
amount
related_username
timestamp
📸 Sample Output
1. Register
2. Login
3. Exit
Enter choice:
📚 Learning Outcomes
Practical implementation of database operations (CRUD)
Secure authentication using hashing
Transaction handling with consistency
Modular programming using functions
Exception handling in real-world scenarios
🔮 Future Enhancements
GUI (Tkinter) or Web App (Flask/React)
OTP/2FA Authentication
Email/SMS notifications
Admin Dashboard
REST API integration
🤝 Contributing

Contributions are welcome! Feel free to fork and improve the project.

📬 Contact

If you have suggestions or feedback, feel free to connect with me on LinkedIn.


---

If you want, I can also:
- :contentReference[oaicite:0]{index=0}
- :contentReference[oaicite:1]{index=1}
- :contentReference[oaicite:2]{index=2} 🔥
