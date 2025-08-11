# Build Log for KasiLink

# Actual May 5

- Created full project from scratch: made the base folder, initialized a Git repo, and created all required Flask files (app/, __init__.py, routes.py, etc.).
- Set up a virtual environment and installed Flask.
- Wrote your first version of the README.md.
- Pushed the initial version to GitHub.

## May 6, 2025
- **Feature**: Created `/posts` POST and GET endpoints in Flask.
  - Used Flask `request` and `jsonify` to handle data.
  - Added `Post` model with fields: title, description, location, and contact.
  - Connected to SQLite (in-memory) for quick testing.
- **Lesson Learned**: Setting up a Flask API using Blueprints and the app factory pattern (create_app).

Creating API routes:
- GET / → API health check.
- POST /posts → Submits a new community post.
- GET /posts → Lists all submitted posts.
- Accepting and returning JSON data with Flask.
- Working with virtual environments to isolate project dependencies.
- Using .gitignore to exclude folders like venv/ from version control.
- Using Postman and curl to test HTTP requests.
- Understanding Git warnings about line endings (LF vs CRLF) on  WindowsFlask routes are simpler than expected; need to improve understanding of Flask's request context.
  - Git kept warning about line endings when adding files. Added venv/ to .gitignore and unstaged everything.
  - Accidentally tracked venv/	Git was trying to add thousands of files.	Used git rm -r --cached venv/ to stop tracking it.
- Unsure how to submit a post	Needed to test the API	Used Postman to make POST requests successfully.
- Unsure how to activate virtualenv	Activation command varies by OS	Used OS-specific activate commands for venv.
- **Next Step**: Implement filtering by tag and location.

---

## May 6, 2025
- **Feature**: Implemented filter query for `/posts` (by tag and location).
✅ What I Set Up
Installed Flask and Flask-SQLAlchemy
Set up a virtual environment and activated it.
Installed dependencies using pip install flask flask_sqlalchemy.
Saved them to requirements.txt.
Configured the Database
Created a config.py file with a PostgreSQL URI:

python
SQLALCHEMY_DATABASE_URI = 'postgresql://<username>:<password>@localhost/kasilink'
Replaced with actual database name, user, and password.

Defined a Data Model
In models.py, I created a Post model:

python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    category = db.Column(db.String(20))
    location = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
Initialized SQLAlchemy in __init__.py

Set up the app factory function with db.init_app(app).

Created Tables

Used the Python shell to create tables:

python
from app import create_app
from app.models import db
app = create_app()
with app.app_context():
    db.create_all()

  - Users can now query `?tag=job` or `?location=Soweto`.
- **Lesson Learned**: Filters are easy with query params, but I need to test edge cases (e.g. empty fields).
- How to structure a Flask app using the application factory pattern (create_app()).
- How to define and manage models with Flask-SQLAlchemy.
- The difference between model classes and temporary in-memory variables (e.g. Post vs posts list).
- How to correctly initialize and use blueprints.
- How to create tables inside an app context using with app.app_context().
- The importance of step-by-step testing (first the app, then routes, then database).

- Set up PostgreSQL and connected it to Flask via SQLAlchemy.
- Created models and routes that support real data persistence.
- Successfully built and registered Flask blueprints.
- Wrote your first automated tests using pytest.
- Validated both successful and failed post creation.
- Confirmed everything works with GET, POST, and test database.

- **What went wrong**: 
Problem	                                                            Fix
ModuleNotFoundError: No module named 'flask_sqlalchemy'	        Installed it with pip install flask_sqlalchemy
NameError: name 'app' is not defined	                          Forgot to define app = create_app() before using it
ImportError: cannot import name 'posts' from 'app.models'	      Tried to import posts (which didn’t exist); fixed by importing the Post class
POST route didn’t save data	             Was appending to a missing posts list instead of using the model and database
Blueprint was named /posts	             Fixed by giving it a valid name: Blueprint('posts', __name__)
Nothing showed on GET /posts	           Fixed by querying Post.query.all() and returning results as JSON


1. Environment Issues
Error: At first, there were issues with Python environments, including missing or conflicting dependencies. For example, trying to install and configure packages like flask_marshmallow and flask_sqlalchemy resulted in errors.

Lesson Learned: It’s crucial to make sure the virtual environment (venv) is properly set up, activated, and that dependencies are installed using pip install. Errors often arise from missing packages, and using a requirements.txt file or Pipfile can streamline this process.

2. Circular Import Issues
Error: You faced circular import errors when trying to import models, the database (db), or other components (e.g., schemas) across multiple files like models.py and routes.py. This occurred because Flask applications use blueprints and often import things that reference each other.

Lesson Learned: Circular imports are common in Flask projects but can be managed by reordering imports and organizing application structure properly. A good strategy is to ensure that the db and ma (Marshmallow) instances are initialized in a separate file (like extensions.py) and then imported where needed.

3. Marshmallow and SQLAlchemy Schema Issues
Error: You faced an error regarding Marshmallow’s schema and SQLAlchemyAutoSchema, where Marshmallow had no attribute SQLAlchemyAutoSchema. Additionally, issues like cannot import pprint from marshmallow occurred.

Lesson Learned: When using Marshmallow with Flask and SQLAlchemy, make sure the packages are correctly installed and that the correct versions are in use. Marshmallow was updated to use SQLAlchemyAutoSchema, and the error related to pprint was due to version mismatches. Always verify the correct versions of dependencies are installed and ensure they are compatible with your Flask version.

4. Flask App Structure and Circular Imports
Error: The circular import error arose when trying to access db in the models.py file because db was being initialized in the create_app() function in __init__.py, which led to issues.

Lesson Learned: To resolve circular import errors, ensure that the db instance is initialized correctly and that create_app() returns the app instance that links all parts together without causing an import loop. Separate app initialization and model/database setup into distinct files.

5. Testing Issues
Error: When running pytest, you encountered issues related to test setup or model imports.

Lesson Learned: For automated testing, make sure your test environment is isolated (use pytest with an in-memory database or mock database setup) and verify that your routes and models are correctly imported in the test files.

---

## May 7, 2025
- **Feature**: User Authentication & Posts API with Flask, JWT, and PostgreSQL
Added `flagged` field to `Post` model for basic moderation.
  - Created `/flag/<post_id>` endpoint.
- **Lesson Learned**: Create a RESTful Flask API that allows users to: Register and log in securely using JWT
 Post categorized content with title, content, location, and timestamp
 Access certain routes only when authenticated 
 It’s easy to add extra features to the Post model. Flask makes it straightforward to add logic for moderation.

 - Blueprint Setup: Every route group needs a Blueprint, and the blueprint must be correctly registered with the app.

- POST Method 405 Errors: A 405 typically means the route exists but doesn’t support the HTTP method — double-check methods=['POST'] is declared.

- Schema Validation: Marshmallow will return Missing data for required fields and Unknown field if you pass fields not declared in the schema.

- Avoid Redefining Models: Never declare models (like Post) in more than one file (e.g. schemas.py). Always import instead.

- Password Hashing: Hashed passwords can be long. Define db.Column(db.String(256)) or more to avoid value too long errors.

- 500 Internal Errors: These usually stem from SQLAlchemy errors or Python exceptions — check your terminal for full traceback.

- JWT Setup: Must initialize JWTManager(app) in create_app() and use create_access_token() and @jwt_required() in your routes.

- Flask Config: Use app.config.from_object('config.Config') before initializing extensions to ensure everything loads properly.

- Debug Mode: Setting app.config["DEBUG"] = True is helpful, but ensure your error logs print to the console clearly.

- **Steps - taken**: 1. Project Setup
Initialized Flask with virtualenv

Installed: flask, flask_sqlalchemy, flask_migrate, flask_jwt_extended, marshmallow_sqlalchemy, and psycopg2

Created core folders: app/, config.py, run.py

2. Configured App
Used a factory pattern to create the Flask app

Loaded configs from config.py

Registered posts_bp and auth_bp Blueprints

3. Built Models
Created User and Post models with appropriate fields

Fixed issue with hashed password length (String(120) → String(256))

4. Marshmallow Schemas
Built PostSchema using SQLAlchemyAutoSchema

Handled serialization of query results and validation of incoming data

5. Post Routes
Implemented /posts [GET, POST] endpoints

Implemented /protected JWT-protected route

Validated input with Marshmallow, returned JSON responses

6. User Registration
Created /register route in auth_routes.py

Checked for existing user, hashed password using generate_password_hash, and committed new user

Debugged 500 error caused by field size and fixed it
- **Next Step**: 🔑 1. Implement /login Route
- Accept username and password
- Authenticate user and return JWT token using create_access_token
🧪 2. Test Authorization
- Use token in Postman headers to access /protected and /posts [POST]
- Confirm token-based access works
🔒 3. Apply JWT Protection
- Require authentication for creating posts or other user-specific routes
🗃️ 4. Improve Models and Relationships
- Link Post model to User via user_id foreign key (optional enhancement)
🧼 5. Clean & Document
Move schemas to schemas/post.py and schemas/user.py for clarity
- Write README or inline comments for team/your future self
- Set up basic UI (HTML form for submitting posts).

---

## May 8, 2025
- **Feature**: 1. Flask Setup and Routes
You’ve set up a Flask app with two main blueprints:

auth_bp for authentication (login, register)

posts_bp for post-related functionality.

These blueprints are registered within the create_app() function in the app’s __init__.py.

You've correctly configured the app to connect to PostgreSQL, and also added JWT for handling token-based authentication.

2. Password Hashing
Passwords are hashed using scrypt (instead of the default pbkdf2 from werkzeug).

You used passlib to generate the scrypt hash when registering a new user and verified the hashed password on login.

When testing, you generated a valid scrypt hash in the correct format (scrypt:32768:8:1$...) and updated it in the database for the user testuser.

3. Authentication Flow
Registration: When users register, their passwords are hashed using scrypt and stored in the database.

Login: During login, the entered password is hashed and compared to the hash in the database. If they match, a JWT token is generated for the user.

You've successfully created the route for user login and token generation but ran into issues verifying the password.

4. Issues Faced
Login Failure: Despite generating a valid scrypt hash, you're still getting an "Invalid credentials" error. The issue likely lies in:

Password hash mismatch: Perhaps the scrypt method for verifying passwords is not matching properly.

Database hash format: You were correctly updating the password hash in the database, but the format or verification process may not be aligning correctly with how the hash was stored.

Verification Method: The login code might not be correctly using the scrypt verification method.

- **What i Learned**
Flask Setup: How to organize blueprints and set up a Flask app for user registration, login, and protected routes.

JWT: How to use JWT for authentication to protect routes, with jwt_required() protecting routes and create_access_token() for generating tokens.

Password Hashing: How to use scrypt for password hashing and verification, and how to store and validate these hashes.

Database Integration: The importance of correctly updating and storing password hashes in the database, and ensuring that the hash format matches during login.

**Next Steps / Issues to Investigate**
Check Hash Format: Double-check the format in which the hash is stored in the database, especially how scrypt hashes are being processed.

Ensure Correct Verification: Ensure the scrypt.verify() method is correctly verifying the password against the hash stored in the database.

Test with Postman: Test the login and registration endpoints with Postman using the correct payload and ensure that the JWT is generated after successful login.

Built a simple HTML form to create a post and display the list of posts.
  - Integrated with `/posts` GET API.
- **Lesson Learned**: Connecting the backend to frontend is not as hard as it seems; Flask and vanilla JS are a good combination for now.
- **Next Step**: Make UI mobile-responsive, and add basic filter options.


**May 13, 2025**
### Step 1: Ensuring Password Hash Format Consistency

---

**What Was Happening:**
In the initial code, we were using `generate_password_hash()` from **Werkzeug** for password hashing during user registration. This method uses **PBKDF2** by default and generates password hashes in the format:

```
pbkdf2:sha256:...$<salt>$<hash>
```

However, for **login**, we were trying to verify passwords using **`passlib.scrypt`**, which generates a different hash format:

```
scrypt:32768:8:1$<salt>$<hash>
```

Since the two hash formats were incompatible, when a user tried to log in, the password verification failed even if the credentials were correct. This caused the login to fail with a **401 Unauthorized** error, even though the **username existed** in the database.

---

**What Went Wrong:**
The root cause of the issue was **inconsistent hashing algorithms**. On registration, the password was hashed using Werkzeug’s `generate_password_hash()` method, but on login, we were trying to verify the password using `passlib.scrypt`, which expects a hash in a **completely different format**.

* The **Werkzeug** hash format (`pbkdf2:sha256`) wasn't compatible with **passlib's scrypt** hash (`scrypt:`).
* The login route tried to use **`passlib.scrypt`**’s `.verify()` method, but it couldn't match the password input with the incorrectly formatted hash stored in the database.

---

**What I Learned:**

1. **Consistency Is Crucial**: When working with password hashing, **both the registration and login processes must use the same hashing algorithm**. Mixing different hashing algorithms (like `PBKDF2` and `scrypt`) leads to verification issues, which is exactly what happened.

2. **`passlib` Over `Werkzeug`**: Switching to `passlib.scrypt` for password hashing ensures **better control** and security. **`passlib`** provides strong cryptographic support with various algorithms like **`scrypt`**, which is more secure than **PBKDF2** for modern applications.

3. **Migration for Existing Users**: If you have existing users who were hashed using a different method (like `generate_password_hash()`), you need to either:

   * **Rehash** their passwords with the new method, or
   * **Delete and re-register** them, as I did during testing.

4. **Debugging Skills**: The process helped me understand how to debug password authentication failures — logging the hashed password and the input password made it clear where the mismatch occurred.

--

**What Should Be Done Going Forward:**

1. **Ensure Hash Format Consistency**: Always use the same hashing algorithm for both registration and login (in this case, `passlib.scrypt`).

2. **Handle Password Migration**: When switching hashing algorithms, ensure you have a strategy for handling existing user records — either by re-hashing their passwords or prompting them to reset their password.

3. **Thorough Testing**: Always test registration and login after implementing changes, especially when dealing with authentication and security mechanisms. This helps catch errors like format mismatches early.

---
**Part 2**

### ✅ Step 2 Recap: Verifying the Login Flow & JWT Authentication

---

### 🧩 **What Was Happening**

After getting registration and login working, you received a JWT token — but when trying to access your `/protected` route:

* You initially got a **404 Not Found**, which meant the route URL was incorrect.
* Then, when you fixed the URL, you ran into `"Invalid crypto padding"`, meaning the token in your request was malformed or corrupted.
* After correcting the request format (method, header, and full token), the protected route finally worked and returned a valid response — `"Hello, user 5"`.

---

### ❌ **What Went Wrong**

1. **Incorrect Route Access**
   You were trying to access `/protected`, but your route was actually under `/posts/protected` because of the blueprint prefix. Flask couldn't find the route, leading to a 404.

2. **Wrong HTTP Method & Payload**
   You initially used `POST` with a body. But the route only accepted `GET`, and JWTs must be passed in the `Authorization` header — not the body.

3. **Malformed JWT Token**
   A copy-paste error or partial token led to `"Invalid crypto padding"` — which is a cryptographic error from trying to decode a broken token.

---

### 💡 **What I Learned**

1. ✅ **JWTs must be passed via headers**, not in the body, using:

   ```
   Authorization: Bearer <your_token>
   ```

2. ✅ **Blueprint URL prefixes affect your routes**. If your blueprint uses `url_prefix='/posts'`, all routes inside it are accessed with that prefix.

3. ✅ **Flask-JWT-Extended handles a lot of security for you**, like checking for missing/expired/invalid tokens and returning appropriate errors.

4. ✅ **Testing JWT-protected routes involves careful attention to method, URL, and headers** — even small mistakes (like a missing space) can break it.

---

### 🔐 Final Result

You successfully authenticated a user, verified the access token, and used it to access a protected route — which is the core of modern token-based authentication systems.

You're now fully set up to:

* Protect APIs
* Personalize responses by user ID
* Scale your app securely

---

🔹 2. Open PowerShell and test:
powershell
Copy
Edit
psql --version
If that works, then run:

powershell
Copy
Edit
psql -U postgres -d kasilink -h localhost -p 5432
Once inside psql, check for your users table:

sql
Copy
Edit
\dt                -- shows tables
SELECT * FROM users;
If the table doesn't exist yet:

🔹 3. Create the table from Flask:
powershell
Copy
Edit
$env:FLASK_APP = "app:create_app"
flask shell
Then in Python:

python
Copy
Edit
from app import db
db.create_all()
After that, go back to psql and re-check with \dt and SELECT * FROM users;.


*** Part 3 ***

Database Structure Check
🔍 What Was Happening
You were able to register users and log in via Postman.

You got valid JWT tokens (meaning the database was working under Flask).

But you couldn’t see your users or tables in psql, and were unsure how to inspect your database directly.

❌ What Went Wrong
psql wasn't installed or in your system’s PATH.

You accidentally tried to run psql inside the Python shell.

PostgreSQL client tools were missing or not yet active due to no restart.

✅ What You Learned
bash, PowerShell, and psql each have specific roles — they are not interchangeable.

Flask can work with the database without you ever touching psql, but to inspect the data directly, psql is essential.

To view DB records manually, you need:

PostgreSQL tools like psql

Your tables created via db.create_all()

A working DB URI in Flask

Restarting your machine is often necessary to apply system PATH changes.


*** 14 May 2025 ***

🧠 What i Learned
Schema Design Matters
When using marshmallow_sqlalchemy.SQLAlchemyAutoSchema, fields like user_id are inferred but still require correct setup (e.g., include_fk=True) or explicit definition.

JWT Integration Best Practices
It's best to avoid trusting the client with user_id. Instead, extract it securely from the JWT using get_jwt_identity().

Validation Needs a Session
Marshmallow with load_instance=True needs a DB session for validation. If not set properly, you’ll get "Validation requires a session" errors.

Explicit Error Handling is Crucial
Catching exceptions, logging them, and rolling back DB sessions prevents silent failures and helps during debugging.

404 vs. 500 Confusion

404 (Not Found) = route or URL is incorrect.

500 (Internal Server Error) = something went wrong in the code logic, often in DB or schema handling.

🧨 What Went Wrong
Initially, your schema was trying to validate a user_id that was injected from JWT but also passed (or missing) in the request payload, causing Unknown field or Missing data errors.

You received a 500 error due to Marshmallow raising ValueError: Validation requires a session because the schema tried to validate with load_instance=True but didn’t have an active SQLAlchemy session.

There was also some route confusion (/posts, /posts/posts) which led to 404 errors.


** pArt 2 **

📖 What Happened
Today, you focused on getting your /posts endpoint to work correctly in your Flask API. You:

Created a protected route to allow post creation only for authenticated users.

Implemented a Marshmallow PostSchema using SQLAlchemyAutoSchema for validation.

Encountered multiple issues including:

JWT token expiration.

Route not being recognized due to incorrect URL paths.

500 Internal Server Errors during post creation.

Schema validation errors (user_id being an unknown or missing field).

Logging errors due to undefined app or logger objects.

Added db.session.rollback() and began setting up logging for clearer debugging.

🌱 What You’re Learning
JWT authentication flow — how to get and use a token properly in a protected route.

Schema validation in Marshmallow — understanding how to separate fields used for deserialization vs. those set manually (like user_id from get_jwt_identity()).

Flask route registration — importance of url_prefix, Blueprint registration, and route paths.

Error handling best practices — using try/except, db.session.rollback(), and logging to diagnose and prevent crashes.

Logging setup in Flask — and how to avoid NameError by using current_app.logger inside route files instead of app.logger.
---

**Prompt for ChatGPT:**

"Hey ChatGPT, let's continue debugging the 500 error from my Flask app when trying to create a post. We confirmed the following yesterday:

The Post model and schema are up to date.

PostgreSQL is running and the schema matches.

JWT authentication works and returns a valid user_id.

We've wrapped the DB commit in a try-except block with rollback and logging.

Flask logging is set up, but I hit a NameError because app or logger wasn't defined in routes.py.

Let’s start by fixing the logging setup properly in routes.py, verify again whether the user exists before inserting the post, and ensure that the user_id is not being included in the marshmallow PostSchema load, but is manually injected."

07/31/2025

✅ KasiLink Flask Backend – Progress Summary (Today)
🔧 Project Setup
Cleaned up your project structure and removed OneDrive-related file permission issues.

Created a new app/__init__.py with the proper Flask app factory setup.

🧱 Extensions + Config
Set up flask_sqlalchemy, flask_migrate, and flask_jwt_extended in extensions.py.

Connected everything to config.Config and initialized the extensions in your app.

🧩 Blueprints & Routes
Registered two blueprints:

/auth (login/register) via auth_bp

/posts (protected post routes and test route) via posts_bp

🛠️ Auth System
Built register and login endpoints with password hashing (passlib) and token-based auth using JWT.

Cleaned up logic for proper error handling and credential checking.

📦 Models & Schemas
Set up database models and Marshmallow schemas (e.g., PostSchema).

Installed marshmallow_sqlalchemy to serialize/deserialize post data.

🧪 App is Now Running
Successfully launched the Flask app with:

arduino
Copy
Edit
python run.py
Confirmed routes like:

http://127.0.0.1:5000/posts/test

http://127.0.0.1:5000/auth/register

🔜 Prompt to Continue Tomorrow
“KasiLink backend is now running with auth and protected routes. Let’s continue by adding user models, enabling real posts linked to users, and managing database migrations with Flask-Migrate.”

🧭 What's Next? (Tomorrow)
Here are your top options:

🔐 Add Full User Model

Define User in models.py

Hook it into auth_routes properly

Create migration: flask db init, flask db migrate, flask db upgrade

📫 Connect Posts to Users

Add user-post relationship

Only allow logged-in users to post under their ID

🧪 Test with Postman

Send JWT in headers

Register & login easily with JSON payloads

📄 Add Swagger UI or API Docs

Use flasgger or apispec to auto-document your endpoints

☁️ PostgreSQL + Deployment (Render)

Swap SQLite for PostgreSQL

Push to GitHub

Deploy on Render for real use


08/02/2025

📝 Summary of Today’s Work:
You:

Recovered your missing __init__.py file in your Flask app.

Cleaned up import errors caused by broken/missing modules.

Installed packages like flask-migrate, flask-jwt-extended, and marshmallow-sqlalchemy.

Created and tested user registration and login routes in Postman.

Fixed JSON input issues in the login route.

Updated your User model to include email.

Connected to PostgreSQL and successfully ran migrations with Flask-Migrate.

📝 Today’s Progress Report — Flask Authentication & DB Update
What we accomplished:
Implemented password hashing with werkzeug.security in the User model to securely store passwords as hashes instead of plaintext.

Updated registration and login routes to use the hashed password methods (set_password and check_password).

Resolved database schema mismatch by renaming the password column to password_hash via a custom Alembic migration.

Applied migrations successfully, verified the database schema to reflect the changes.

Tested user registration and login flows with Postman and confirmed JWT tokens are issued correctly.

Established a clean foundation for future protected routes using JWT.

What’s next:
Add protected routes that require JWT authentication.

Implement user profile management (update details, change password).

Possibly add HTML templates or connect with a frontend framework.

Prepare for deployment (e.g., to Render, Railway).

08/04/2025

✅ Quick Recap So Far
You've successfully:

Registered users with hashed passwords

Logged in users and generated JWT tokens

Created protected routes (like /auth/me, /posts/protected)

Verified JWT authentication works via Postman

⏭️ Next Step: User Profile Management
Let's implement two more features:


✅ Progress Recap
OneDrive + Path Fixes: Fixed import and environment issues (flask not recognized, migration errors, etc.).

JWT Auth Setup: Login, register, and protected route successfully tested.

Schema Fixes: Switched from password to password_hash, updated Alembic migrations.

User Profile: /auth/me and /auth/profile endpoints fully working.

Password Change: /auth/change-password route tested and working with token auth.

Database Integrity: Tables now match model structure after reset and migrations.

▶️ Next Steps (Tomorrow)
Post Creation Routes:

Implement POST /posts to create posts (authenticated users only).

Implement GET /posts to list all posts.

Later: Add filtering by user or category.

User Management:

Add ability to delete account.

Optional: Add email verification (via token, just backend-side for now).

Frontend or Templates:

Either integrate with a frontend (React, Vue, etc.) or add simple HTML templates (Jinja2).

Prepare for Deployment:

Clean up .env, update config.py.

Setup on Render or Railway with PostgreSQL.

08/05/2025

✅ Issue: Import Errors and ModuleNotFoundError
You were getting errors like:

ModuleNotFoundError: No module named 'app.routes.routes.auth_routes'

ModuleNotFoundError: No module named 'app.routes.posts_routes'

And similar module resolution problems

🧰 Cause
Your routes/ folder is inside the app/ directory, but:

You didn’t have an __init__.py file inside app/routes/, so Python didn’t treat it as a package.

There were import mistakes like trying to do from app.routes.routes.auth_routes due to wrong nesting.

🛠️ Fixes Applied
Added __init__.py to the app/routes/ folder to mark it as a package.

Corrected imports in app/__init__.py:

python
Copy
Edit
from .routes.auth_routes import auth_bp
from .routes.posts_routes import posts_bp
Made sure you run the app from the root (kasilink/) folder, not inside app/.

🧪 Result
Now your Flask app starts without errors, and your route blueprints (auth_bp, posts_bp) are correctly registered.

Today’s Summary
Successfully set up user registration and login with JWT authentication.

Created protected routes that require JWT tokens.

Implemented CRUD endpoints for posts:

Create (POST /posts) with authenticated user association.

Read (GET /posts/<id>) to retrieve individual posts.

Began working on the Update (PUT /posts/<id>) route, facing some issues to troubleshoot.

Tested protected routes and token authorization using Postman.

Fixed schema and serialization issues with Marshmallow and SQLAlchemy integration.

Next Steps (Tomorrow)
Fix and finalize the PUT /posts/<id> update route.

Implement the Delete (DELETE /posts/<id>) route with appropriate permissions.

Add user profile management endpoints (view and update profile, change password).

Optionally, implement pagination and filtering for posts.

Explore connecting HTML templates or integrating a frontend framework.

Prepare the app for deployment (Dockerize, deploy to Render/Railway, etc.).

08/06/2025

✅ What You’ve Just Accomplished:
🔐 JWT login fully working

🧠 Fixed the tricky "Subject must be a string" bug

🔧 Built authenticated post creation

✏️ Successfully updated a post with PUT (with ownership check)

💪 Fully working JWT-protected CRUD system for posts

🚀 What’s Next (Suggested Steps):
Add Delete Route
Allow users to delete their own posts (DELETE /posts/<id>).

Get All Posts by User
Add an endpoint like /posts/mine that returns only the posts of the authenticated user.

Validation & Pagination (optional)

Prevent empty content

Add ?page=1&limit=10 to /posts for scalable listing

Frontend / HTML Templates (optional)
If you're doing HTML output (Flask templates) or building an API for React/Vue.

Deployment Ready
Set up for Render or Railway with .env, production configs, and Procfile.

✅ KasiLink Dev Log — CRUD Progress Summary
🔐 Authentication & Token Fixes
Resolved "Subject must be a string" error by converting user.id to str(user.id) in create_access_token.

Confirmed access token is being returned correctly during login.

Verified token works with protected routes using @jwt_required().

🛠️ Post Routes (CRUD Progress)
✔️ Create Post: User can create a post (title, content) with their token. User ID is auto-attached from JWT.

✔️ Read Post(s):

/posts - Get all posts (public or protected depending on design).

/posts/<id> - Get specific post by ID.

✔️ Update Post:

Implemented secure update route using PUT /posts/<post_id>.

Verified post belongs to the logged-in user before allowing updates.

Resolved 403 and JWT issues, now fully functional.

✅ Debugging Milestones
Fixed:

Token expiration issues

Missing or invalid JWT subject

403 forbidden on update

Schema errors during post creation (Unknown field, requires session, etc.)

🧪 Tested Successfully In Postman
Logged in, copied access token, and used it for:

Creating posts

Getting individual posts

Updating a post (with full authorization check)

📍 You’re Now At:
CRUD Progress: 3/4 routes done

✅ Create

✅ Read

✅ Update

⏳ Delete (next)

🚀 Next Steps (Suggestions)
🔥 Add Delete Post route with JWT ownership check.

📦 List posts by logged-in user (/posts/mine).

🎨 (Optional) Add HTML templates or build a frontend.

🚀 Prepare for deployment to Render or Railway.



08/08/25

Today’s Progress Review:
Successfully implemented JWT authentication with registration, login, and protected routes.

Built CRUD endpoints for posts, including create, read, update, and delete.

Implemented user profile management with view and update profile.

Added change password endpoint with password hashing and verification.

Troubleshot import/module path issues and resolved routing conflicts.

Tested endpoints using Postman and Python requests (still tweaking testing in Python shell).

What’s Next:
Polish testing process: fix the testing script or interactive shell usage.

Implement any missing CRUD features for posts or users.

Add soft delete for posts if needed.

Start integrating frontend or add HTML templates.

Prepare deployment setup (e.g., on Render or Railway).


08/11/2025

Testing Progress


* Implemented and refined automated tests using `pytest` for key API endpoints in Kasilink.
* Covered:

  * Home route check (`GET /`) — simple health check.
  * User registration and login endpoints (`POST /auth/register`, `POST /auth/login`) with JWT token verification.
  * Post creation endpoint (`POST /posts/`) with authentication and data validation.
* Debugged and fixed several issues related to:

  * Configuration for test environment and in-memory SQLite database.
  * Passing JWT tokens correctly in test requests.
  * Adjusting Marshmallow schemas to align with test data fields.
* Achieved all tests passing successfully, ensuring endpoint functionality and security (auth-protected routes).
* Prepared codebase for future test expansions and continuous integration setup.

