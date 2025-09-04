# CP_LittleLemonRestaurant_API

Visit http://127.0.0.1:8000/ to access the API.

Authentication
Most endpoints require authentication. Use Django's built-in authentication or create API tokens.

Permissions
Customers: Can view menu, manage cart, place orders
Managers: Full access to menu items, user management
Delivery Crew: Can view and update assigned orders
🔧 Technologies Used
Django 5.2
Django REST Framework
SQLite Database
Python 3.x

📝 License
This project is for educational purposes.

👨‍💻 Author
Created as part of Django REST Framework learning project.


# Little Lemon Restaurant API

Welcome to the Little Lemon Restaurant API! This Django REST Framework API provides endpoints for managing restaurant menu items and table bookings.

## Base URL

[http://127.0.0.1:8000](http://127.0.0.1:8000)

## Authentication

This API uses Token Authentication. You need to obtain a token first and include it in your requests.

### Authentication Endpoints

- POST /auth/users/ - Register new user
- POST /auth/token/login/ - Login and get token
- POST /auth/token/logout/ - Logout and destroy token
- GET /auth/users/me/ - Get current user profile
- POST /auth/users/set_password/ - Change password

## API Endpoints to Test

### Menu Items API

- GET /api/menu-items/ - List all menu items (requires authentication)
- POST /api/menu-items/ - Create new menu item (requires authentication)
- GET /api/menu-items/{id}/ - Get single menu item (requires authentication)
- PUT /api/menu-items/{id}/ - Update menu item (requires authentication)
- DELETE /api/menu-items/{id}/ - Delete menu item (requires authentication)

### Bookings API

- GET /restaurant/api/bookings/ - List all bookings (requires authentication)
- POST /restaurant/api/bookings/ - Create new booking (requires authentication)
- GET /restaurant/api/bookings/{id}/ - Get single booking (requires authentication)
- PUT /restaurant/api/bookings/{id}/ - Update booking (requires authentication)
- DELETE /restaurant/api/bookings/{id}/ - Delete booking (requires authentication)

## Testing Instructions

### 1. Register a User

POST /auth/users/
Content-Type: application/json

{
    "username": "testuser",
    "password": "testpass123",
    "email": "[test@example.com](mailto:test@example.com)"
}

### 2. Login to Get Token

POST /auth/token/login/
Content-Type: application/json

{
    "username": "testuser",
    "password": "testpass123"
}

Response: {"auth_token": "your_token_here"}

### 3. Test Menu Items

GET /api/menu-items/
Authorization: Token your_token_here

### 4. Create a Menu Item

POST /api/menu-items/
Authorization: Token your_token_here
Content-Type: application/json

{
    "title": "Margherita Pizza",
    "price": "12.99",
    "inventory": 10
}

### 5. Create a Booking

POST /restaurant/api/bookings/
Authorization: Token your_token_here
Content-Type: application/json

{
    "name": "John Doe",
    "no_of_guests": 4,
    "booking_date": "2024-12-25T19:00:00Z"
}

## Sample Data Models

### Menu Item

{
    "id": 1,
    "title": "Margherita Pizza",
    "price": "12.99",
    "inventory": 10
}

### Booking

{
    "id": 1,
    "name": "John Doe",
    "no_of_guests": 4,
    "booking_date": "2024-12-25T19:00:00Z"
}

## Setup Instructions

1. Clone the repository

2. Install dependencies: pip install -r requirements.txt

3. Run migrations: python manage.py migrate

4. Create superuser: python manage.py createsuperuser

5. Start server: python manage.py runserver

## Testing Tools

- Insomnia REST Client
- Postman
- curl
- DRF Browsable API (web browser)

## Status Codes

- 200 OK - Successful GET, PUT
- 201 Created - Successful POST
- 204 No Content - Successful DELETE
- 401 Unauthorized - Authentication required
- 403 Forbidden - Permission denied
- 404 Not Found - Resource not found

Happy testing!
