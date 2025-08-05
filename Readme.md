Kasilink

A Flask-based backend API for managing user authentication, posting, and protected routes—powered by JWT auth and PostgreSQL.

🗂 Project Structure

arduino
Copy
Edit


kasilink/
├── run.py
├── config.py
├── requirements.txt
└── app/
    ├── __init__.py
    ├── extensions.py
    ├── models.py
    ├── schemas.py
    └── routes/
        ├── __init__.py
        ├── auth_routes.py
        └── posts_routes.py


⚙️ Key Features

Secure user registration and login using password hashing (werkzeug.security)

JWT-based authentication for protected routes

CRUD-post model resources connected to authenticated users

PostgreSQL integration with Flask‑Migrate for migrations

User profile routes: Fetch and update account info, change password


🚀 Setup & Run Locally

Clone the repo:

bash
Copy
Edit
git clone https://github.com/1Gift3/Kasilink.git
cd Kasilink
Create and activate your virtual environment:

bash
Copy
Edit
python -m venv venv
.\venv\Scripts\activate  # Windows
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Configure PostgreSQL in config.py (set SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY).

Run database migrations:

bash
Copy
Edit
flask db upgrade
Start the app:

bash
Copy
Edit
python run.py



🧪 API Endpoints

Authentication (open):

POST /auth/register – Register user

POST /auth/login – Login and receive access_token

Profile (requires auth):

GET /auth/profile – Get current user info

PUT /auth/profile – Update username/email

PUT /auth/change-password – Update password securely

Posts (requires auth):

GET /posts/protected – Sample protected endpoint

POST /posts – Create a post linked to authenticated user

Make sure to include JWT token in headers as:

makefile
Copy
Edit
Authorization: Bearer <your_access_token>


📈 Future Enhancements

Add GET /posts, GET /posts/<id>, DELETE /posts/<id>

Add pagination and filtering (e.g., posts by user)

Add Jinja2 templates or a separate frontend (React, Vue, etc.)

Deploy to Render or Railway with managed PostgreSQL

Add tests using pytest and API documentation (Swagger/OpenAPI)

✅ License & Contact
Under MIT License.
Feel free to contribute or ask questions!

