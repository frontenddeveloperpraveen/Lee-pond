# Django Application

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Routes](#routes)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## Overview

This is a Django-based web application for managing user authentication, document uploads, and order tracking. The application allows users to log in, submit forms, reset passwords, view notifications, and track orders.

## Features

- User Authentication (Login, Logout, Password Reset)
- Form Submission and Document Upload
- Email Notifications for Password Reset
- Order Tracking and Status Updates
- User Profile Management
- Admin Media Download

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/your-repository.git
   ```

2. Navigate to the project directory:

   ```sh
   cd your-repository
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Set up your email configuration in `settings.py`:

   ```python
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_HOST_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your-company-email@example.com'
   EMAIL_HOST_PASSWORD = 'your-app-password'
   ```

5. Apply migrations:

   ```sh
   python manage.py migrate
   ```

6. Create a superuser:

   ```sh
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```sh
   python manage.py runserver
   ```

## Usage

- Access the application at `http://localhost:8000`.
- Log in with your user credentials.
- Use the navigation menu to access different sections of the application.
- Submit forms, reset passwords, and track orders as needed.

## Routes

### Static Pages

- **Login**: `/login/` (Serves the login page)
- **Logout**: `/logout/` (Logs out the user)
- **Reset Password**: `/reset_password/` (Serves the password reset page)
- **Forget Password**: `/forget_password/` (Serves the forget password page)

### Request Handlers

- **Login Submit**: `/login_submit/` (Handles login form submission)
- **Form Submit**: `/form_submit/` (Handles form submissions)

### Main Routes

- **Home**: `/home/` (Displays the home page with user details)
- **Page1**: `/page1/` (Displays the index page)

### API Routes

- **Base Page**: `/base_page/` (Displays the base page with notifications and orders)
- **Notification API**: `/notification_api/` (Fetches user notifications)
- **Profile API**: `/profile_api/` (Displays user profile details)
- **Orders API**: `/orders_api/` (Displays user orders)
- **Home API**: `/home_api/` (Displays home page with notifications and orders)
- **Order Switch**: `/order_switch/<route>/` (Displays past or pending orders)
- **Particular Order**: `/particular_order/<param>/` (Displays details for a specific order)
- **User Activity**: `/user_activity/<state>/` (Updates user activity status)

### Admin Routes

- **Media Download**: `/media_download/<file_path>/` (Allows admin to download files)

## Technologies Used

- Django
- HTML/CSS
- JavaScript
- OpenCV
- Threading
- Base64
- SMTP (Email)

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License.

## Author

- **Praveen KR** - [Linkedin Profile](https://www.linkedin.com/in/mepraveenkr/)

Feel free to reach out with any questions or feedback!
