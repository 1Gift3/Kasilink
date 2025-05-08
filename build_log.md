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



Summary for Tomorrow’s Continuation
Tomorrow, you can continue your progress from this point with the following next steps:

Flask Migrations:
Set up Flask-Migrate to handle database schema changes and migrations. This will allow you to make changes to your models and keep track of changes in the database schema.

Steps:

Install Flask-Migrate if not already installed.

Initialize the migration folder and perform the first migration.

Learn to use flask db migrate, flask db upgrade, and flask db downgrade for easy database migrations.

Authentication:
Add JWT Authentication (e.g., with Flask-JWT-Extended) to secure your endpoints. This will allow users to register, log in, and access secure routes with a token.

Steps:

Install Flask-JWT-Extended.

Implement routes for user registration and login.

Protect routes with JWT token authentication.

Write More Tests:
Continue writing unit tests using pytest to test both your routes (e.g., POST and GET requests) and authentication flow. Testing your application will ensure that it behaves as expected and will help prevent errors when scaling.


Here's a clear and ready-to-use prompt you can use tomorrow to pick up exactly where you left off:

---

**Prompt for ChatGPT:**

Next Steps Prompt for Tomorrow
Ensure Password Hash Format Consistency:

Recheck the hash format in your login route. Make sure that the hash stored in the database is using the same format expected by passlib.scrypt (e.g., scrypt:32768:8:1$...).

Verify that the hash generated during registration is correctly stored and used during login.

Verify the Login Flow:

Test the login functionality thoroughly:

Make sure you're sending the correct username and password in your request.

Log the hash value on the server to ensure that the correct hash is being used to compare against the password.

Improve Error Handling and Logging:

Add more detailed logging and error handling in your login and registration routes. For instance, print the user’s hashed password and the hashed password in the database for debugging purposes.

JWT Testing:

Once the login works, ensure you’re able to generate and retrieve the JWT correctly.

Test the protected routes to make sure the JWT is being correctly passed and validated.

Database Structure Check:

Inspect your PostgreSQL database once again to ensure the correct hash format is stored and that all the user records are properly updated.