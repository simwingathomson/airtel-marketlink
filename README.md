# Airtel MarketLink

**Airtel MarketLink** is a field sales resource and operations management platform.

**Connecting People, Partners & Markets.**  
**Version 1.0.0**

It connects districts, territories, markets, booths, channel partners, employees, resources, tasks, audits, notifications, and accountability records through a Flask REST API and a browser-based web application. The earlier CustomTkinter desktop client remains in the repository as an optional local client, but the primary app is now the web app.

## Architecture

```text
Browser Web App
        |
        | Flask sessions / JSON API
        v
Flask Web + REST API + SQLAlchemy
        |
        v
SQLite development database
```

Render hosts the Flask web application and REST API together. Users access Airtel MarketLink in a browser.

## Key Features

- Role-based access for Administrator, ZBM, TSM, TL, TSE, and Chabeba.
- Employee hierarchy with manager relationships.
- District, territory, market, booth, and channel partner modules.
- Resource inventory with assignment, transfer, return, incident, and history workflows exposed in both the web app and API.
- Task, audit, notification, search, CSV report export, and audit log endpoints.
- Password hashing, bearer tokens, role validation, friendly API errors, and upload restrictions.
- Seed data for demo use with fictional employees, markets, booths, partners, and resources.

## Windows 10 Setup

Install Python 3.11, then run:

```powershell
py -3.11 -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the web app locally:

```powershell
python backend/run.py
```

Optional desktop client, if you still want it:

```powershell
python desktop/main.py
```

Demo login:

```text
Username: admin
Password: admin123
```

For browser use, you can also run `START_MARKETLINK_WEB.bat` after creating the virtual environment and installing requirements.


## Browser Web App Access

Run the backend/web server:

```powershell
venv\Scripts\activate
python backend/run.py
```

Then open this link in your browser:

```text
http://127.0.0.1:5000
```

Login with:

```text
Username: admin
Password: admin123
```

You can also double-click `START_MARKETLINK_WEB.bat` after creating the virtual environment and installing requirements.
## API

Important endpoints include:

```text
/health
/api/auth/login
/api/auth/logout
/api/users
/api/employees
/api/districts
/api/territories
/api/markets
/api/booths
/api/channel-partners
/api/resources
/api/resource-assignments
/api/resource-transfers
/api/resource-returns
/api/resource-requests
/api/resource-incidents
/api/tasks
/api/audits
/api/notifications
/api/reports/summary
/api/search
```

## Seed Data

From the project root:

```powershell
$env:FLASK_APP="backend.wsgi:app"
flask seed-data
```

The local `backend/run.py` also seeds demo data automatically when empty.

## Render Deployment

Render should run the Flask API with Gunicorn:

```text
gunicorn --bind 0.0.0.0:$PORT wsgi:app
```

The included `render.yaml` uses:

```text
Build: pip install -r requirements-server.txt
Start: gunicorn --bind 0.0.0.0:$PORT wsgi:app
```

Production deployment should use Neon Postgres through `DATABASE_URL`. SQLite remains available only as the local fallback when `DATABASE_URL` is not set. In Render, create a Neon database, copy its pooled connection string, and add it as the `DATABASE_URL` environment variable.

## Environment Variables

Copy `.env.example` to `.env` locally if needed:

```text
SECRET_KEY=
DATABASE_URL=
API_BASE_URL=http://127.0.0.1:5000
```

For production desktop clients, set `API_BASE_URL` to your Render service URL. Do not invent or hard-code the production URL.

## GitHub Preparation

```powershell
git init
git add .
git commit -m "Initial Airtel MarketLink application"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY
git push -u origin main
```

Do not commit secrets, `.env`, database files, virtual environments, uploads, or credentials.

## CSV Reports

Administrators, ZBMs, and TSMs can export CSV reports from the desktop Reports screen. The backend currently supports:

```text
resources
assigned-resources
lost-resources
damaged-resources
transfers
returns
markets
booths
channel-partners
employees
tasks
audits
```

## Desktop Workflow Screens

The desktop sidebar includes real API-backed screens for resource assignments, transfers, returns, resource requests, incidents, tasks, audits, notifications, global search, and CSV reports. Buttons save records through the Flask API instead of acting as placeholders.




## Neon Postgres Setup

1. Create a Neon project and database.
2. Copy the pooled connection string from Neon. It should start with `postgresql://`.
3. In Render, open the Airtel MarketLink service and add this environment variable:

```text
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require
```

4. Keep the Render start command as:

```bash
flask --app wsgi:app seed-data && gunicorn --bind 0.0.0.0:$PORT wsgi:app
```

The startup seed creates tables and demo records if needed, and also ensures `admin / admin123` works.
