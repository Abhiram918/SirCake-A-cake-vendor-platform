# 🍰 SirCake

SirCake is a comprehensive cake vendor platform built with Django. It provides a complete ecosystem for cake enthusiasts, sellers, and delivery personnel to interact seamlessly. From browsing a delectable menu of cakes to managing bakery kitchens and delivery logistics, SirCake handles it all.

## ✨ Features

- **Multi-User Roles**: Custom user model supporting Customers, Sellers (Bakers), and Delivery Boys.
- **Product Management**: Categorized cake listings (e.g., Wedding Cakes, Birthday Cakes).
- **Shopping Cart & Checkout**: Robust order management and tracking.
- **Seller Dashboard**: A dedicated space for bakers to manage their inventory and view incoming baking tasks.
- **Delivery Management**: A dashboard for delivery personnel to track and manage cake deliveries.
- **Reviews & Ratings**: Integrated feedback system allowing customers to leave 1-5 star ratings and comments on cakes.
- **Payments Integration**: Ready for payment processing.

## 🏗️ Architecture & Apps

The project is structured into modular Django apps, each handling a specific domain:

- `sircake`: The main configuration and routing hub.
- `accounts`: Manages user authentication, registration, and role-based access.
- `products`: Handles the catalog of cakes and their categories.
- `orders`: Manages the shopping cart and user order history.
- `sellers`: The dedicated interface for bakers to add new products and manage their kitchen.
- `delivery`: Interface for delivery drivers to manage their assignments.
- `reviews`: Manages customer feedback and ratings.
- `dashboard`: General dashboard views and analytics.
- `payments`: Handles order transactions.

## 🚀 Tech Stack

- **Backend**: Python, Django 5.2.11
- **Database**: SQLite (default, ready for PostgreSQL/MySQL integration)
- **Image Processing**: Pillow
- **Frontend**: Django Templates, HTML, CSS, JavaScript (served via `static/`)

## 🛠️ Installation & Setup

Follow these steps to run SirCake locally:

### 1. Prerequisites
- Python 3.8+ installed (ensure Python is added to your PATH).

### 2. Clone the Repository
```bash
git clone <your-repository-url>
cd SirCake
```

### 3. Set Up Virtual Environment
Create and activate a virtual environment to isolate dependencies:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Database Setup
Run migrations to create the database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)
Create an admin account to access the Django backend:
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Main Site**: `http://127.0.0.1:8000/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.
