# 🍰 SirCake: The Ultimate Beginner's Setup Guide

Hello! If you have been given this folder, this guide will tell you **exactly** how to open the project on your computer, run it, and understand what files do what. Please follow the steps one by one.

---

## 🛠️ Step 1: Getting Your Computer Ready

Before you do anything, you need Python installed on your computer. 
1. I have already provided you with the Python installation file (a `.exe` file). Double-click on it to run it.
2. **CRITICAL STEP:** On the very first screen of the installer, **check the box at the bottom that says "Add Python.exe to PATH"**. Do NOT skip this, or the code won't work!
3. Click "Install Now" and wait for it to finish.

## 📂 Step 2: Opening the Code

1. Right-click the `.zip` file you received and click **Extract All**. 
2. Open a program called **VS Code** (or whatever code editor you like).
3. If using VS Code, click on `File` -> `Open Folder` and select the **SirCake** folder you just extracted.
4. Open the Terminal in your editor. (In VS Code, click `Terminal` at the top -> `New Terminal`).

## ⚙️ Step 3: Running the Setup Commands

You need to type these precise commands into your terminal at the bottom of the screen. Press **Enter** after typing each line.

**1. Create a "Bubble" for the code (called a Virtual Environment)**
We do this so the code doesn't mess with other stuff on your computer.
```bash
python -m venv venv
```

**2. Turn on the "Bubble"**
If you are using Windows, type:
```bash
venv\Scripts\activate
```
*(If you are on a Mac, type: `source venv/bin/activate`)*
You will know it worked if you see `(venv)` pop up on the left side of your terminal typing line.

**3. Install the Code Tools**
The app needs a few extra tools to work (like Django, which is the framework we built it on). Type this:
```bash
pip install -r requirements.txt
```

**4. Setup the Database**
Next, we need to create the database where all the cakes, users, and orders will be saved. Type these two lines one by one:
```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Create the "Boss" Account (Admin)**
You need an admin account to log in and control the entire website. Type this:
```bash
python manage.py createsuperuser
```
It will ask for a Username, Email (you can skip email by pressing Enter), and a Password. **Note: When you type your password, it won't show anything on the screen. That is normal for security. Just type it and press Enter.**

---

## 🚀 Step 4: Starting the Website!

Now the moment of truth! Every time you open your computer to work on this, you just need to type this one command:
```bash
python manage.py runserver
```

Once it starts, you will see a message with a web link. 
Open your browser (Chrome/Edge/Safari) and go to:
👉 **http://127.0.0.1:8000/**

To log into your "Boss" dashboard, go to:
👉 **http://127.0.0.1:8000/admin/**

---

## 📁 Step 5: What Do All These Folders Do?

The code is broken down into small folders called "Apps". Think of each folder like a worker who has a specific job in the bakery.

* **`sircake` (The Manager):** This is the main folder. It holds the `settings.py` file which has the master switches and rules for the whole website.
* **`accounts` (The Security Guard):** This handles people logging in, signing up, and keeping track of whether someone is a normal Customer, a Seller (Baker), or a Delivery Boy.
* **`products` (The Menu):** This is where all the Cakes and Categories (like Wedding Cakes, Birthday Cakes) are stored in the code.
* **`orders` (The Cashier):** This manages the Shopping Cart and tracks the orders when someone buys a cake.
* **`sellers` (The Baker's Kitchen):** This handles the special dashboard for Sellers. Only sellers use this to add new cakes or see what they need to bake.
* **`delivery` (The Delivery Guy):** Handles the dashboard for the delivery drivers to see which cakes are ready to be taken to the customer.
* **`reviews` (The Feedback Box):** Holds the code that lets users give 1 to 5-star ratings or leave comments on cakes.
* **`static` & `templates` (The Decorator):** Contains the actual look of the website. `templates` has all the HTML files (the structure of the pages), and `static` has the CSS (colors), JS (animations), and images.

That's it! Take it one folder at a time, and don't panic if an error pops up. Happy coding!
