MIS PROJECT SETUP GUIDE
========================

Project Info:
-------------
- Project Name: MIS
- Framework: Django + Django REST Framework
- Database: PostgreSQL
- Database Name: berar_database_prod

---------------------------------------
SETUP INSTRUCTIONS (STEP-BY-STEP)
---------------------------------------

1. Clone the Repository:
------------------------
   git clone <your-repo-url>
   cd mis

2. Create Virtual Environment:
------------------------------
   python -m venv venv

3. Activate the Environment:
----------------------------
   On Windows:
       venv\Scripts\activate
   On Mac/Linux:
       source venv/bin/activate

4. Install Dependencies:
------------------------
   pip install -r requirements.txt

5. Configure Database (settings.py):
------------------------------------

   # Server Database Configuration:
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.postgresql",
           "NAME": "berar_database_prod",
           "USER": "berar_database_prod",
           "PASSWORD": "Berar@2025#nagpur$",
           "HOST": "10.0.100.85",
           "PORT": "5432",
       }
   }

   # Local Database Configuration:
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.postgresql",
           "NAME": "berar_database_prod",
           "USER": "postgres",
           "PASSWORD": "root",
           "HOST": "localhost",
           "PORT": "5432",
       }
   }

   ➤ Choose the appropriate config based on your environment (server/local).

6. Apply Migrations:
--------------------
   python manage.py makemigrations
   python manage.py migrate

7. Seed Admin User:
-------------------
   python manage.py seed_admin_user

   This creates an admin user with the following credentials:

   Email:    admin@example.com  
   Password: Admin@12345

8. Seed Loan Account Data (Local Only):
---------------------------------------
   python manage.py seed_loan_accounts

   This will insert test data (e.g., 10 rows) into the `LoanAccount` table.

9. Run the Development Server:
------------------------------
   python manage.py runserver

   Access the project at:
   http://127.0.0.1:8000/

---------------------------------------
API ENDPOINTS
---------------------------------------

1. Test API
-----------
   Method: GET  
   URL:    http://127.0.0.1:8000/test/  
   Response:
   {
     "message": "Hello from mis app!"
   }

---------------------------------------
NOTES
---------------------------------------

- Ensure PostgreSQL service is running.
- Database name must match: `berar_database_prod`
- If models are changed, run:
     python manage.py makemigrations
     python manage.py migrate
- Use Postman or curl to test API endpoints.
- For production:
     - Set DEBUG = False
     - Configure ALLOWED_HOSTS
     - Use environment variables for secrets

---------------------------------------
TROUBLESHOOTING
---------------------------------------

- Database connection errors? Check:
   ✓ PostgreSQL is installed and running  
   ✓ User and database exist  
   ✓ Credentials are correct in settings.py  
   ✓ psycopg2 or psycopg2-binary is installed

- Pip install issues?
   Run:
   python -m pip install --upgrade pip

---------------------------------------


---------------------------------------
MAINTAINER
---------------------------------------

For support, contact the development team or open an issue in the repository.
