# KasiLink

**KasiLink** is a community-driven platform where local individuals and businesses can **request and offer services** within their neighborhoods — all powered by location-based matching, trust, and connection.

---

## ✨ Vision & Purpose

- Enable people **needing help** (tasks, services, consultations) to make requests.  
- Enable those **offering help** (skilled individuals, small businesses) to list their services.  
- Match requests and offers based on **category**, **location radius**, and availability.  
- Foster trust via reviews, secure interactions, and responsible design.  
- Grow a community where giving and receiving help is seamless and dignified.

---

## 🚀 Core Features

- **Authentication & Profiles**  
  Register / Login securely with hashed passwords & JWT.  
  User profiles, ability to edit username / email / password.

- **Service Requests & Offers**  
  Create, view, edit requests (“I need help”) and offers (“I can help”) with title, description, category, location, and radius.

- **Location-based Matching**  
  Search offers that fall within the request’s radius.  
  (Using geospatial queries: with latitude/longitude + PostGIS or similar.)

- **Protected Routes & Authorization**  
  Operations like edit/delete are only allowed by the owning user.  
  All service endpoints require authentication.

- **Extensible Future Modules**  
  Chat / messaging between users, reviews & ratings, payment flow, frontend UI (React/Vue), and more.

---

## 🗂 Project Structure (Example)

```

kasilink/
├── run.py
├── config.py
├── requirements.txt
├── app/
│   ├── **init**.py
│   ├── extensions.py
│   ├── models.py
│   ├── schemas.py
│   └── routes/
│       ├── auth_routes.py
│       ├── request_routes.py
│       ├── offer_routes.py
│       └── match_routes.py
├── tests/
│   └── test_routes.py
└── build_log.md

````

---

## 🛠 Setup & Running Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/1Gift3/Kasilink.git
   cd Kasilink
````

2. Activate virtual environment & install:

   ```bash
   python -m venv venv
   source venv/bin/activate       # or .\venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. Configure environment / database:

   * Set `SQLALCHEMY_DATABASE_URI` in `config.py` (e.g. PostgreSQL)
   * Set `JWT_SECRET_KEY`

4. Run migrations:

   ```bash
   flask db upgrade
   ```

5. Start the app:

   ```bash
   python run.py
   ```

---

## 📦 API Endpoints (Draft)

| Method | Route                     | Description                                      |
| ------ | ------------------------- | ------------------------------------------------ |
| POST   | `/auth/register`          | Register new user                                |
| POST   | `/auth/login`             | Login and get access token                       |
| GET    | `/auth/profile`           | Retrieve user profile                            |
| PUT    | `/auth/profile`           | Update username/email                            |
| PUT    | `/auth/change-password`   | Update user password                             |
| POST   | `/requests`               | Create a service request                         |
| GET    | `/offers`                 | List service offers (with optional filtering)    |
| POST   | `/offers`                 | Submit your service offer                        |
| GET    | `/match/<int:request_id>` | Find offers matching request (radius & category) |

---

## 📈 Roadmap & Next Steps

* Add **radius search** and geospatial matching.
* Develop **reviews & ratings** for completed services.
* Add **messaging / chat** between users.
* Build a **frontend UI** (React/Vue) for better usability.
* Deploy publicly (Render / Railway) with monitoring & CI.

---

## 🤝 Contributing & Community

Your contributions welcome!

* Please review open issues before creating new ones.
* Write clear, atomic pull requests.
* Include tests where relevant.
* This repo serves not just as software, but as a **shared community-building tool**.

---

## 🧾 License

MIT License — see [LICENSE](LICENSE) for details.

---
