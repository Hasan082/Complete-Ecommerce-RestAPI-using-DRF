# Django E-Commerce API

This project is a **Django REST Framework (DRF)** based e-commerce API with authentication, product and category management, cart and order handling, and API documentation using **drf-spectacular**.

## Features

- **Authentication & Registration**: Powered by `dj-rest-auth`  
- **Products & Categories**: CRUD operations via `ProductViewSet` and `CategoryViewSet`  
- **Cart Management**: `CartViewSet` for adding/removing products  
- **Order Management**: `OrderViewwSet` and `OrderItemViewwSet` for order handling  
- **API Documentation**: Swagger UI and Redoc using `drf-spectacular`  
- **Password Reset**: Supports confirmation via `PasswordResetConfirmView`

## API Endpoints

### Authentication
- `POST /registration/` – Register a new user  
- `POST /login/` – Login user  
- `POST /logout/` – Logout user  
- `POST /password/reset/` – Request password reset  
- `POST /password/reset/confirm/` – Confirm password reset

### Product & Category
- `GET /categories/` – List categories  
- `GET /products/` – List products  
- `POST /products/` – Create product  
- `PUT /products/{id}/` – Update product  
- `DELETE /products/{id}/` – Delete product

### Cart
- `GET /carts/` – Get user cart  
- `POST /carts/` – Add product to cart  
- `PUT /carts/{id}/` – Update cart item  
- `DELETE /carts/{id}/` – Remove from cart

### Orders
- `GET /orders/` – List orders  
- `POST /orders/` – Create order  
- `GET /orderitems/` – List order items  

### API Documentation
- Swagger UI: `/swagger-ui/`  
- Redoc: `/redoc/`  
- OpenAPI Schema: `/schema/`

## Installation

```bash
# Clone the repository
git clone <repo_url>
cd <project_name>

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
````
