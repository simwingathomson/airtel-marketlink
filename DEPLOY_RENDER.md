# Deploy Airtel MarketLink On Render

## Current Status

This project is ready to deploy from GitHub to Render.

Local Git commit:

```text
c5f6360 Prepare Airtel MarketLink for online deployment
```

## Push To GitHub

Create an empty GitHub repository, then run from this folder:

```powershell
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## Deploy On Render

1. Open Render and create a new Blueprint or Web Service from the GitHub repository.
2. Use the included `render.yaml`.
3. Confirm these settings:

```text
Build command: pip install -r requirements-server.txt
Start command: flask --app wsgi:app seed-data && gunicorn --bind 0.0.0.0:$PORT wsgi:app
Health check: /health
```

## Login

After deployment opens successfully:

```text
Username: admin
Password: admin123
```

