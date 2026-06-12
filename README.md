# 🍰 SirCake

A full-featured multi-vendor cake ordering platform built with Django. SirCake connects customers, bakers, and delivery personnel through dedicated dashboards and workflows, providing a complete e-commerce ecosystem for cake ordering and delivery.

![SirCake Banner](screenshots/banner.png)

<p align="center">
  <a href="https://github.com/Abhiram918/SirCake-A-cake-vendor-platform">
    <img src="https://img.shields.io/badge/Source_Code-GitHub-black?style=for-the-badge" />
  </a>
</p>

---

## 📸 Screenshots

### Home Page

![Home Page](screenshots/home.png)

### Product Catalog

![Products](screenshots/products.png)

### Seller Dashboard

![Seller Dashboard](screenshots/seller-dashboard.png)

### Delivery Dashboard

![Delivery Dashboard](screenshots/delivery-dashboard.png)

---

## ✨ Features

### Customer Features

* Browse cakes by category
* View detailed product information
* Add products to cart
* Place and track orders
* Leave reviews and ratings

### Seller Features

* Manage cake inventory
* Add and update products
* View incoming orders
* Track order status

### Delivery Features

* View assigned deliveries
* Update delivery status
* Manage delivery workflow

### System Features

* Custom user authentication
* Role-based access control
* Product categorization
* Order management
* Review and rating system
* Payment-ready architecture

---

## 🏗️ Architecture

The project follows a modular Django architecture:

```text
SirCake
│
├── accounts      # Authentication & User Roles
├── products      # Cake Catalog & Categories
├── orders        # Cart & Order Management
├── sellers       # Seller Dashboard
├── delivery      # Delivery Dashboard
├── reviews       # Ratings & Reviews
├── dashboard     # Analytics & Overview
├── payments      # Payment Processing
└── sircake       # Project Configuration
```

---

## 🚀 Tech Stack

| Category         | Technologies             |
| ---------------- | ------------------------ |
| Backend          | Python, Django           |
| Database         | SQLite                   |
| Frontend         | HTML, CSS, JavaScript    |
| Templates        | Django Templates         |
| Image Processing | Pillow                   |
| Authentication   | Custom Django User Model |

---

## 🛠️ Installation

### Clone Repository

```bash
git clone https://github.com/Abhiram918/SirCake-A-cake-vendor-platform.git
cd SirCake
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Admin User

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

Visit:

```text
http://127.0.0.1:8000/
```

---

## 🎯 Key Learning Outcomes

* Building scalable Django applications
* Implementing role-based access control
* Managing e-commerce workflows
* Designing modular application architecture
* Handling user-generated reviews and ratings
* Managing seller and delivery operations

---

## 🚀 Future Improvements

* Stripe/Razorpay Integration
* Email Notifications
* Real-Time Order Tracking
* Inventory Analytics
* Recommendation System
* Mobile Application

---

## 👨‍💻 Author

**Abhiram Shibu**

* GitHub: https://github.com/Abhiram918
* LinkedIn: https://linkedin.com/in/abhiramshibu

---
