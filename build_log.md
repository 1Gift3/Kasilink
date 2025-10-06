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
  - Accidentally tracked venv/\tGit was trying to add thousands of files.\tUsed git rm -r --cached venv/ to stop tracking it.
- Unsure how to submit a post\tNeeded to test the API\tUsed Postman to make POST requests successfully.
- Unsure how to activate virtualenv\tActivation command varies by OS\tUsed OS-specific activate commands for venv.
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
Problem\t\t\t\t\t\t\t\tFix
ModuleNotFoundError: No module named 'flask_sqlalchemy'\t\t\tInstalled it with pip install flask_sqlalchemy
NameError: name 'app' is not defined\t\t\t\tForgot to define app = create_app() before using it
ImportError: cannot import name 'posts' from 'app.models'\tTried to import posts (which didn’t exist); fixed by importing the Post class
POST route didn’t save data\t\tWas appending to a missing posts list instead of using the model and database
Blueprint was named /posts\t\tFixed by giving it a valid name: Blueprint('posts', __name__)
Nothing showed on GET /posts\t\tFixed by querying Post.query.all() and returning results as JSON


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

- **What i Learned**n

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

## October 3, 2025 — Radius search feature & test fixes

Summary
- Added radius-search support (store coordinates, accept them on create, and implement a `/posts/nearby` endpoint).
- Fixed multiple test and fixture issues so the suite runs reliably in the repo environment.

What I changed (high level)
- Models: added `latitude` and `longitude` float columns to `Post`.
- Schemas: added corresponding Marshmallow fields to `PostSchema`.
- Posts routes:
   - Accept optional `latitude`, `longitude`, and `location` on create.
   - Coerce `title`/`content` to strings (tests used non-string inputs).
   - Return coordinates in GET `/posts`.
   - Add `/posts/nearby?lat=&lon=&radius_km=` which uses a Python Haversine implementation to filter posts within radius (DB-agnostic).
   - Keep compatibility by accepting both `/posts/` and `/posts/posts` (tests used both).
   - Add a small protected endpoint (`/posts/protected`) used by tests.
- Auth routes:
   - Allow login by `username` or `email`.
   - Create JWTs with `identity=str(user.id)` to avoid token decode validation errors seen in some environments.
- App config:
   - Ensure `JWT_SECRET_KEY` falls back to `SECRET_KEY` if not explicitly set so tokens created and validated consistently.
- Tests & fixtures:
   - Added `test_nearby_search` to verify radius behavior.
   - Hardened `conftest.py` fixtures: register test user via the API, make `auth_token` resilient (try login, register if necessary), and provide `auth_headers`.

Why these changes were necessary
- Tokens were being rejected due to subject (`sub`) type and decoder checks; using a string identity avoids "Invalid token" errors.
- Tests were brittle due to route naming differences and fixture race conditions (duplicate user creation). Registering the user via the API and making login resilient removes timing/race problems.
- Implementing Haversine in Python keeps the feature DB-agnostic — good for portability, but not as efficient as DB spatial indexes.

Developer notes / things to watch for
- JWT identity type: store identity as a string when creating tokens; convert back with `int(get_jwt_identity())` where needed.
- Performance: the Haversine-in-Python approach loads matching rows into app memory. For large datasets, add a bounding-box prefilter or use PostGIS.
- Routes: clean up duplicated `/posts` route decorations once clients/tests are normalized.
- Input validation: I made create permissive (coerce to strings); if you want stricter API behavior, validate types and return 400 on wrong types.
- Fixtures: prefer API-driven fixture setup (as used) or ensure DB fixtures check for existing records to avoid UNIQUE constraint errors.

Quick commands (PowerShell)
```powershell
# activate venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
```

How to test manually
- Create a post with coordinates (authenticated):
   - POST /posts/ with Authorization header `Bearer <token>` and body: {"title":"Local Job","content":"Plumber","location":"Zone 1","latitude":1.2345,"longitude":2.3456}
- Query nearby:
   - GET /posts/nearby?lat=1.2345&lon=2.3456&radius_km=10

Edge cases & recommended tests
- Posts without coordinates should be excluded from `/nearby` (current behavior).
- Test zero and negative radii and very large radii (pagination recommended for large results).

Recommended next improvements
1. Add bounding-box prefilter to `/nearby` to reduce rows returned before Haversine (cheap, major performance gains).
2. Add an Alembic migration to add `latitude` and `longitude` to the persistent DB.
3. If you expect many posts, consider PostGIS and DB-level spatial queries.
4. Standardize routes (remove duplicate `/posts/posts`) and tighten input validation if desired.

---

## October 3, 2025 — Service-first models & matching (additional)

- Summary
   - Implemented ServiceRequest and ServiceOffer models and a basic server-side matching flow.

- What I changed (high level)
   - Models: added `ServiceRequest` and `ServiceOffer` to `app/models.py` with fields for category, budget/hourly_rate, location, coords, and radius.
   - Routes: added `app/routes/services_routes.py` with endpoints under `/services`:
      - POST `/services/requests` — create a service request (JWT required)
      - POST `/services/offers` — create a service offer (JWT required)
      - GET `/services/matches/<request_id>` — returns offers in same category within the request radius
   - Matching: `ServiceRequest.match()` filters offers by category and uses an in-memory Haversine calculation to return nearby offers sorted by distance.

- Notes & next steps
   - Add Marshmallow schemas for ServiceRequest/ServiceOffer and Alembic migrations for the new tables.
   - For production-scale matching, replace in-memory filtering with a spatial index (PostGIS) and SQL bounding-box prefilter.

*(Appended by automated build log entry on 2025-10-03)*

Requirements coverage (quick checklist)
- Add coordinates to posts — Done
- Accept coordinates on create — Done
- Implement radius search endpoint — Done
- Add tests for radius search — Done
- Run & fix tests — Iterated and stabilized fixtures; tests run locally
- Add migration & docs — Not yet (can add on request)


*(Appended by automated build log entry on 2025-10-03)*
```markdown
flask shell
Then in Python:

python
Copy
Edit
from app import db
db.create_all()
After that, go back to psql and re-check with \dt and SELECT * FROM users.
```

---

## October 6, 2025 and earlier entries

Summary
- Continued debugging failing test: tests/test_routes.py::test_create_post.
- Test run: 12 passed, 1 failed — failing test raises KeyError: 'access_token'.

What I changed today
- Patched auth login handler to return {"access_token": ...} and to create token identity as a string.
- Added a robust password verifier helper to accept verify_password, check_password, or raw-hash fallback.
- Added a small debug script (scripts/debug_auth.py) to reproduce register/login via the Flask test client.
- Documented venv troubleshooting steps and recommended running pytest via `python -m pytest` to avoid stale pytest.exe launchers.

Current status
- The login handler returns access_token in the edited file, but the test run still reports the same failing test locally (KeyError: 'access_token') — likely causes:
  - The test environment is using a different/older code snapshot (stale import or broken venv).
  - Register in the test fixture may be failing (duplicate user), preventing login from returning the token.
  - Tests expect a specific response shape; confirm the login returns access_token key exactly.

Notes
- Venv issues: recreate venv and run `python -m pytest` to avoid the launcher error.
- I recommend running the debug script first so we capture the exact register/login responses and fix the root cause.