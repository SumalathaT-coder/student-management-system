# Student Management System

A web-based Student Management System built with Python and Django to manage student records, courses, user accounts, and academic performance.

## Features

- User registration, login, and logout
- Student management: create, view, update, and delete records
- Course management
- Search and pagination
- User profiles
- Dashboard and reports
- Role-based permissions
- CSV export
- Student marks and result validation

## Technologies Used

- Python
- Django
- HTML and CSS
- SQLite
- Git and GitHub

## Installation and Setup

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Create a `.env` file in the project root and configure the required environment variables:

   `DJANGO_SECRET_KEY=your-secret-key`

   `DJANGO_DEBUG=True`

   `DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost`

5. Apply database migrations:

   `python manage.py migrate`

6. Start the development server:

   `python manage.py runserver`

7. Open `http://127.0.0.1:8000/` in your browser.

## Security Notes

- Keep your `.env` file and secret key private.
- Do not commit your local database or virtual environment.
- Use appropriate production settings before deployment.

## Project Status

Developed as a practical Python Full Stack learning project.
