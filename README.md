# NetFix 🛠️🏡

*The Trusted Platform for Home Services*

NetFix is a Django web application connecting customers with trusted companies providing home services like plumbing, painting, gardening, and more. Both companies and customers can register, manage profiles, and interact securely. Admins can manage all data using Django’s admin interface.

---

## Table of Contents

* [Features](#features)
* [Tech Stack](#tech-stack)
* [Screenshots](#screenshots)
* [Installation](#installation)
* [Usage](#usage)
* [Folder Structure](#folder-structure)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

---

## Features

* **Two User Roles:**

  * **Companies:** Register, login, create and manage service listings, view and edit their company profile.
  * **Customers:** Register, login, browse/request services, rate companies, manage personal profile.
* **Service Management:**

  * Companies can add, edit, and delete home services.
  * Customers can browse and request services.
* **Service Rating System:**

  * Customers can rate services after completion.
* **Profile Avatars:**

  * Dynamic avatars via Dicebear.
* **Modern Responsive UI:**

  * Custom CSS and flexible layouts.
* **Admin Panel:**

  * Manage users, services, and requests through Django’s built-in admin panel.

---

## Tech Stack

* **Backend:** Django 3.1.14 (Python 3.10)
* **Database:** SQLite3 (default; can be swapped)
* **Frontend:** HTML, CSS (custom, can be extended with Bootstrap)
* **Other:** Static files for images/icons, Dicebear Avatars


---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/netfix.git
cd netfix
```

### 2. Set up a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Collect static files

```bash
python manage.py collectstatic
```

### 6. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

*Follow the prompts to set username, email, and password for the admin account.*

### 7. Run the development server

```bash
python manage.py runserver
```

### 8. Access the app

* App: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Usage

* **Companies:** Register → Login → Add Services → Edit Company Profile → View Requests.
* **Customers:** Register → Login → Browse/Request Services → View Customer Profile → Rate Services.
* **Admin:** Login at `/admin/` and manage all users/services/requests.

---

## Folder Structure

```
netfix/
│
├── manage.py
├── db.sqlite3
├── static/
│   ├── css/
│   ├── images/
│   └── ...
├── templates/
│   ├── main/
│   ├── users/
│   ├── services/
│   └── ...
├── users/
├── services/
├── main/
└── ...
```

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## Contact

* Project Owners: Maria Tzemanaki & Thanos Ziagakis
* Email: [tzemanakimaria97@hotmail.com](mailto:your.email@example.com) & [ziagakisthanos@gmail.com](mailto:your.email@example.com)
* [GitHub Repo](https://github.com/MariaTze/netfix)

---
