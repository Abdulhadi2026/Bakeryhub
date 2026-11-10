# Bakery Management System

A professional bakery management system built with Django, SQLite, Bootstrap 5, and Chart.js. It includes inventory tracking, sales management, customer management, order tracking, suppliers, employees, expenses, and reporting.

## Features
- Responsive dashboard with bakery-themed UI
- User authentication and role-based access
- Product and category management
- Inventory monitoring and stock movement tracking
- POS sales with receipt generation
- Customer, order, supplier, and employee management
- Expense tracking and financial reports
- SQLite database setup with Django ORM

## Tech Stack
- Python 3.12+
- Django 6.1.2
- SQLite
- Bootstrap 5
- Chart.js
- Pillow

## Installation
1. Open a terminal in the project folder.
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the environment:
   - Windows PowerShell:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - Command Prompt:
     ```cmd
     .venv\Scripts\activate.bat
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup
1. Run migrations:
   ```bash
   python manage.py migrate
   ```
2. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
3. Load sample bakery data:
   ```bash
   python manage.py seed_data
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```
5. Open the application at http://127.0.0.1:8000/
6. Admin panel is available at http://127.0.0.1:8000/admin/

## Default Login
- Username: the superuser you created
- Password: the password you set during `createsuperuser`

## Project Structure
- bakery_management/ - Django project settings and URL configuration
- accounts/ - authentication and user profile logic
- dashboard/ - dashboard summary views
- products/ - product and category management
- inventory/ - stock and inventory movement management
- sales/ - POS and sales transactions
- customers/ - customer management
- orders/ - order management
- suppliers/ - supplier management
- employees/ - employee management
- expenses/ - business expense tracking
- reports/ - reporting pages and CSV export
- static/ - CSS and JavaScript assets
- templates/ - HTML templates for the application

## Production note
This project is configured for local development and uses SQLite for ease of setup. For production deployment, use a secure environment and revise the Django secret key and ALLOWED_HOSTS settings.
