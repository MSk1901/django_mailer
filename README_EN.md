## Mailer

Web application for managing email newsletters.
- Registration with email confirmation
- User management for admins and the ability to block them
- Manager functionality
- Adding and configuring custom email newsletters (frequency, start and end time, recipients)

### Technology Stack:

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.1-green)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-grey)](https://www.postgresql.org/)

- `python`
- `django`
- `postgreSQL`
- `crontab`

<details>
  <summary>Deployment and Usage</summary>

### 1. Clone the project:

```bash
git clone https://github.com/MSk1901/django_mailer.git
```

### 2. Navigate to the project root directory:

```bash
cd django_mailer
```

### 3. Set up environment variables: 

   1. Create a file named `.env` in the root directory 
   2. Copy the contents of the `.env.template` file into it and replace the values with your own
   3. For the project to work correctly in a local development environment, set the value `DEBUG=True` to automatically handle static files and provide detailed error messages.


### 4. Install dependencies:

```bash
pip install -r requirements.txt
```

### 5. Run database migrations:

```bash
python3 manage.py migrate
```

### 6. Start the development server:

```bash
python3 manage.py runserver
```

### Usage

Go to http://127.0.0.1:8000/  
First, you need to register in order to be able to add newsletters and clients (recipients) later.  
To do this, click on the button in the top right corner - a menu will open.

#### Administrative Panel:
To access the admin panel, create a superuser:

```bash
python3 manage.py csu
```

Open the administrative panel at http://127.0.0.1:8000/admin/ and log in with the superuser credentials.

In the admin panel, you can grant manager access rights so that they can:
 - view any newsletters
 - view the list of service users
 - block service users
 - disable newsletters

</details>

### Project Author

Maria Kuznetsova - kuznetsova19.m@gmail.com