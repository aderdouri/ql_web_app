# Django App Setup and Run Guide

## Step 1: Create Virtual Environment

```bash
python -m venv venv
```

## Step 2: Activate Virtual Environment

```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

## Step 3: Install Django

```bash
pip install django
pip install quantlib
```

## Step 4: Install Project Dependencies (if requirements.txt exists)

```bash
pip install -r requirements.txt
```

## Step 5: Apply Database Migrations

```bash
python manage.py migrate
```

## Step 6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

## Step 7: Run the Development Server

```bash
python manage.py runserver
```

## Step 8: Access the Application

- Open your browser and go to: <http://127.0.0.1:8000/>
- Admin panel: <http://127.0.0.1:8000/admin/>

## Additional Commands

```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply new migrations
python manage.py migrate

# Run on different port
python manage.py runserver 8080
```

