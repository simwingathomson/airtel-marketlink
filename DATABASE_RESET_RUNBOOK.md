# Airtel MarketLink Database Reset Runbook

Use this only for the Airtel MarketLink database configured by `DATABASE_URL`. Do not run it against SINAMU or any other application database.

## 1. Identify Database

```powershell
flask --app wsgi:app db-info
```

Confirm:

- Provider is PostgreSQL/Neon for production.
- Database host matches the MarketLink Neon project.
- Tables listed are MarketLink tables.

## 2. Backup Current Data

```powershell
flask --app wsgi:app export-db-csv
```

Save the exported CSV folder before continuing.

## 3. Reset Database

This is destructive. It drops and recreates all MarketLink tables.

```powershell
$env:MARKETLINK_RESET_CONFIRM="RESET_AIRTEL_MARKETLINK"
flask --app wsgi:app reset-db
```

## 4. Seed Admin Only If Needed

```powershell
flask --app wsgi:app seed-data
```

The seed command creates the admin account for initial access. For production, change the password immediately.

## 5. Verify

```powershell
python check_neon.py
flask --app wsgi:app db-info
python -m pytest
```
