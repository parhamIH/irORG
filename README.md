# TechShop API

A Django REST Framework backend for an e-commerce platform specializing in tech products.

## Features

- Product management with various attributes (size, color, storage)
- Category and subcategory organization
- Product image gallery
- User reviews and ratings
- Admin-only access for product creation, updates, and deletion

## Technologies

- Django 
- Django REST Framework
- SQLite (Database)
- JWT Authentication (if implemented)

## API Endpoints

### Products

- `GET /products/` - List all products
- `GET /products/<id>/` - Get product details
- `POST /products/` - Create a new product (Admin only)
- `PUT /products/<id>/` - Update a product (Admin only)
- `DELETE /products/<id>/` - Delete a product (Admin only)

## Setup Instructions

1. Clone the repository
   ```
   git clone https://github.com/yourusername/techshop-api.git
   cd techshop-api
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run migrations
   ```
   python manage.py migrate
   ```

5. Create a superuser
   ```
   python manage.py createsuperuser
   ```

6. Run the development server
   ```
   python manage.py runserver
   ```

## Admin Dashboard

Access the admin dashboard at `/admin/` to manage:

- Products
- Categories
- Product Attributes (Size, Color, Storage)
- User Reviews

## License

[MIT License](LICENSE)

## Contributors

- Your Name - Initial work 