# 📚 Library Management System

A Django-based web application where users can view books, borrow and return them, deposit funds, and leave reviews. The system supports email notifications for deposits and borrow transactions, category-based filtering, and personal borrowing history tracking.

---

## Features

### Book Management
- Each book includes:
  - Title
  - Description
  - Image
  - Borrowing Price
  - User Reviews
- Books are organized by categories
  - Users can filter books by category
- Book detail page with all information and user reviews

### User Management
- User account creation (registration)
- Secure login and logout functionality
- Borrowing & Returning Books
  - Users can borrow books using deposited balance
  - Upon return, the borrowing amount is refunded
- Deposit System
  - Users can deposit money into their account
  - Email confirmation is sent after a successful deposit
- Borrowing System
  - After borrowing, the book price is deducted from the user balance
  - Email notification sent to the user
- Borrowing History
  - Tracks each book's borrow date
  - History displayed in user profile
- Reviews
  - Users can leave reviews for books they have borrowed

---

## Email Notifications
- Sent after successful deposits
- Sent after successful borrow transactions

---

## Technology Stack

- Backend: Django (Python)
- Database: SQLite (or PostgreSQL)
- Frontend: Django Templates + Bootstrap
- Authentication: Django's built-in auth system
- Email Backend: Django SMTP backend (Gmail)

---

## Project Structure

library_management/
├── books/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ └── templates/books/
├── users/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ └── templates/users/
├── templates/
├── static/
├── media/
├── db.sqlite3
├── manage.py
└── requirements.txt

---


## Create Superuser
- python manage.py createsuperuser

---


## Media Files
- Make sure to configure media in settings.py:
- MEDIA_URL = '/media/'
- MEDIA_ROOT = BASE_DIR / 'media'

---


## Testing
- python manage.py test

---


## Contributing
- Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


---
