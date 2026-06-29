# Real Estate Operations Dashboard

A backend-focused real estate operations demo built with Flask, SQLite, JavaScript, HTML/CSS, and REST-style routes.

## Overview

This project is a small internal real estate operations dashboard for managing property listings, agents, and office locations. It was built to demonstrate backend and software development skills including authentication, session handling, CRUD operations, relational database design, dashboard metrics, and clean project structure.

The system is designed like an internal tool that a brokerage or real estate operations team could use to manage listings, assign agents, track listing statuses, and generate simple listing summaries.

## Features

* User authentication and session handling
* Dashboard with listing, agent, and office metrics
* CRUD operations for property listings
* CRUD operations for agents
* Office/location management
* Agent-to-listing assignment
* Listing status tracking
* Listing show-sheet / marketing summary generation
* SQLite relational database
* Modular backend structure using routes, repositories, and services

## Tech Stack

* Python
* Flask
* SQLite
* JavaScript
* HTML/CSS
* REST-style API routes

## Backend Concepts Demonstrated

* Authentication flow
* Session-based access control
* REST-style API design
* CRUD operations
* Relational database schema design
* Foreign key relationships
* Dashboard aggregation queries
* Modular project structure
* Separation of route, repository, and service logic

## Main Modules

### Authentication

The application includes login, registration, logout, and session-check functionality.

### Dashboard

The dashboard displays operational metrics such as:

* Total listings
* Available listings
* Pending listings
* Rented listings
* Sold listings
* Active agents
* Office locations
* Unassigned listings

### Listings

Users can create, view, update, and delete property listings. Each listing includes title, address, city, property type, price/rent, bedrooms, bathrooms, status, description, assigned agent, and office location.

### Agents

Users can manage agents, including their contact details, specialization, office location, and active/inactive status.

### Offices

Users can manage brokerage office locations and view how many agents and listings are connected to each office.

### Show Sheet

The show-sheet feature generates a simple client-ready listing summary from stored listing data.

## Demo Login

Email: [sahil@example.com](mailto:sahil@example.com)
Password: 123456

## How to Run Locally

1. Clone the repository

```bash
git clone https://github.com/sahilkumar-sk/real-estate-listing-dashboard.git
```

2. Go into the project folder

```bash
cd real-estate-listing-dashboard
```

3. Create a virtual environment

```bash
python -m venv .venv
```

4. Activate the virtual environment

For Windows:

```bash
.venv\Scripts\activate
```

For macOS/Linux:

```bash
source .venv/bin/activate
```

5. Install dependencies

```bash
pip install -r requirements.txt
```

6. Create the database tables

```bash
python db_setup.py
```

7. Seed demo data

```bash
python seed.py
```

8. Run the application

```bash
python app.py
```

9. Open the app in your browser

```text
http://127.0.0.1:5000/
```

## Project Structure

```text
real-estate-listing-dashboard/
│
├── app.py
├── db.py
├── db_setup.py
├── seed.py
├── requirements.txt
├── README.md
│
├── repositories/
│   ├── assets.py
│   ├── employees.py
│   ├── locations.py
│   └── users.py
│
├── routes/
│   ├── assets_rt.py
│   ├── auth.py
│   ├── dashboard_rt.py
│   ├── employees_rt.py
│   ├── locations_rt.py
│   └── users_rt.py
│
├── services/
│   └── dashboard.py
│
└── static/
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── assets.html
    ├── employees.html
    ├── locations.html
    │
    ├── css/
    │   ├── auth.css
    │   └── ams-theme.css
    │
    └── js/
        ├── config.js
        ├── session.js
        ├── login.js
        ├── register.js
        ├── dashboard.js
        ├── assets.js
        ├── employees.js
        └── locations.js
```

## API Routes

### Authentication

```text
POST /register
POST /login
POST /logout
GET /session
```

### Dashboard

```text
GET /dashboard/stats
```

### Listings

```text
GET /listings
GET /listings/<id>
POST /listings
PUT /listings/<id>
DELETE /listings/<id>
GET /listings/<id>/show-sheet
```

### Agents

```text
GET /agents
GET /agents/<id>
POST /agents
PUT /agents/<id>
DELETE /agents/<id>
```

### Offices

```text
GET /locations
GET /locations/<id>
POST /locations
PUT /locations/<id>
DELETE /locations/<id>
```

## Notes

This is a focused backend demo, not a full production platform. It is intended to demonstrate backend architecture, database workflows, CRUD functionality, authentication, and real-estate-style internal operations.

## Future Improvements

* Role-based access control for admins and agents
* Search and filtering for listings
* Property image uploads
* PostgreSQL migration
* API documentation with Swagger or Postman
* Deployment with production-ready configuration
* Email or social sharing for listing show sheets
