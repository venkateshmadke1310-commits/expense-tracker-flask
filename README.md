# 💰 Expense Tracker – Flask Web Application

A full-stack Expense Tracker web application built using **Python, Flask, SQLite, HTML, and CSS**.  
The app allows users to securely manage their personal expenses with authentication, filtering, summaries, and CSV export.

## 🔗 Live Demo
https://expense-tracker-flask-1.onrender.com/login

---

## 🚀 Features

- 🔐 User Registration & Login (Session-based authentication)
- ➕ Add new expenses
- ✏️ Edit existing expenses
- 🗑️ Delete expenses
- 🔍 Filter expenses by category and date range
- 📊 Category-wise expense summary
- 📅 Monthly expense summary
- 📁 Export monthly expenses as CSV
- 👤 User-specific data isolation
- 📱 Responsive UI (Desktop & Mobile)

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask  
- **Database:** SQLite  
- **Frontend:** HTML, CSS  
- **Authentication:** Flask Sessions  
- **Deployment:** Render  
- **Version Control:** Git & GitHub  

---

## 📂 Project Structure

```text
expense-tracker-flask/
│
├── app.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── view.html
│   ├── add.html
│   ├── edit.html
│   ├── summary.html
│   └── monthly.html
│
├── static/
│   └── style.css
│
└── README.md

⚙️ Setup Instructions (Local)
1. Clone the repository
https://github.com/venkateshmadke1310-commits/expense-tracker-flask.git

2. Install dependencies
pip install -r requirements.txt

3. Run the application
python app.py

4. Open in browser
http://127.0.0.1:5000/login

🔐 Authentication Flow

New users must register first

Login creates a session

All expenses are linked to the logged-in user

Users cannot view or modify other users’ data

📌 Security Notes

Session-based access control

User-specific database queries

Unauthorized access is restricted

SQLite used for simplicity (can be upgraded to PostgreSQL)

🌱 Future Improvements

Password hashing (bcrypt)

Pagination for large expense lists

Charts & analytics (Chart.js)

Admin dashboard

Cloud database (PostgreSQL)

Dark mode UI

👨‍💻 Author

Venkatesh Madke
Python & Flask Developer
📌 LinkedIn: https://www.linkedin.com/in/venkatesh-madke-675760375/

⭐ If you like this project

Give it a ⭐ on GitHub — it motivates me to build more!
