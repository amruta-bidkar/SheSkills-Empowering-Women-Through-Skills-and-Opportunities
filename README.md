# SheSkills – Empowering Women Through Skills and Opportunities

## 📌 Project Overview

**SheSkills** is a web-based women empowerment platform developed using Django. It helps women, especially homemakers and women who are not working outside the home, showcase their skills and connect with potential customers in their local communities.

Women can create professional profiles, list their skills, and upload portfolio images of their work. Customers can explore service providers, view their work, and contact them directly for services and orders.

## 🎯 Objectives

- Empower women by providing an online platform to showcase their skills.
- Help women promote their services and reach potential customers.
- Connect customers with local skilled service providers.
- Provide a portfolio feature to display work samples.
- Enable direct communication between customers and providers.

## ✨ Key Features

- **User Registration and Login:** Separate access for service providers and customers.
- **Provider Profiles:** Create and manage professional profiles.
- **Skill Management:** Add skills such as tailoring, mehendi art, cooking, crafting, and beauty services.
- **Portfolio Management:** Upload images and descriptions of completed work.
- **Skill Marketplace:** Browse and discover service providers.
- **Provider Details:** View provider information, skills, and portfolio.
- **Direct Contact:** Contact providers directly to discuss services and orders.
- **Profile Management:** Update professional information as needed.

## 🛠️ Technologies Used

- **Frontend:** HTML, CSS, JavaScript, Bootstrap (if used in the current implementation)
- **Backend:** Python, Django
- **Database:** SQLite
- **Version Control:** Git and GitHub

## 👥 User Roles

### 1. Service Provider
- Register and log in to the platform.
- Create and update a professional profile.
- Add skills and showcase work through portfolio images.
- Share their services with potential customers.

### 2. Customer
- Register and log in to the platform.
- Explore available skills and providers.
- View provider profiles and portfolio work.
- Contact providers directly for service enquiries.

## ⚙️ Installation and Setup

### Prerequisites
- Python installed
- Git installed
- pip package manager

### Step 1: Clone the repository

```bash
git clone https://github.com/amruta-bidkar/SheSkills-Empowering-Women-Through-Skills-and-Opportunities.git
cd SheSkills-Empowering-Women-Through-Skills-and-Opportunities
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

If a `requirements.txt` file exists:

```bash
pip install -r requirements.txt
```

Otherwise, install Django and any other dependencies used by the project.

```bash
pip install django pillow
```

### Step 4: Apply database migrations

```bash
python manage.py migrate
```

### Step 5: Create an administrator account (optional)

```bash
python manage.py createsuperuser
```

### Step 6: Run the development server

```bash
python manage.py runserver
```

Open the following URL in your browser:

http://127.0.0.1:8000/

## 📂 Project Structure

The project is organized into Django applications. The structure below is illustrative; adjust it to match the actual repository.

```text
SheSkills/
├── accounts/
├── profiles/
├── config/
├── templates/
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

- `accounts/` – User registration, login, logout, and role-based dashboards.
- `profiles/` – Provider profiles, skills, portfolio, and marketplace functionality.
- `config/` – Django project configuration and URL routing.
- `templates/` – HTML templates for the user interface.

## 🔄 Application Workflow

1. A user registers as a service provider or customer.
2. A provider creates a professional profile.
3. The provider adds skills and portfolio work samples.
4. Customers browse the marketplace and view provider details.
5. Customers contact suitable providers directly to discuss services.

## 🌟 Project Benefits

- Supports women's economic empowerment and digital visibility.
- Helps local service providers promote their skills.
- Makes it easier for customers to discover local services.
- Provides an accessible way to showcase work without requiring a complex online store.

## 🚀 Future Enhancements

- Advanced skill and location-based search.
- Provider verification and ratings.
- Email notifications for service enquiries.
- Improved mobile-responsive interface.
- Multilingual support.

## 🎓 Academic Project

SheSkills is developed as a web application project focused on women's empowerment, skill promotion, and community-based service discovery.

## 👩‍💻 Developer

**Amruta Bidkar**

GitHub: [amruta-bidkar](https://github.com/amruta-bidkar)

---

*SheSkills – Showcasing Skills, Creating Opportunities.*
