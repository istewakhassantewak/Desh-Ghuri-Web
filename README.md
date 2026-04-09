# Desh-Ghuri Web

Modern Django travel booking platform with role-based users (Traveler/Tour Guide), package listing, booking flow, dashboard, and SSLCommerz payment integration.

## 1) Requirements

- Python 3.13 recommended (Windows users should avoid Python 3.14 for this project)
- pip
- virtualenv (optional but recommended)

## 2) Local Setup

1. Create and activate virtual environment:
   - Windows PowerShell:
     - `py -3.13 -m venv .venv`
     - `.venv\Scripts\Activate.ps1`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Create your env file:
   - Copy `.env.example` to `.env`
   - Update values as needed
4. Run migrations:
   - `python manage.py migrate`
5. Start server:
   - `python manage.py runserver`
6. Open:
   - `http://127.0.0.1:8000/`

## 3) Environment Variables

Required variables (see `.env.example`):

- `SECRET_KEY` - Django secret key
- `DEBUG` - `True` for local, `False` for production
- `ALLOWED_HOSTS` - comma-separated domains/IPs
- `BASE_URL` - full app base URL (used for payment callback URLs)
- `SSL_COMMERZ_STORE_ID`
- `SSL_COMMERZ_STORE_PASSWORD`
- `SSL_COMMERZ_SANDBOX_MODE` - `True`/`False`

## 4) Production Deploy (Render)

### Build Command

`pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`

### Start Command

`gunicorn core.wsgi:application`

### Environment Variables on Render

- `SECRET_KEY=...`
- `DEBUG=False`
- `ALLOWED_HOSTS=your-app.onrender.com`
- `BASE_URL=https://your-app.onrender.com`
- `SSL_COMMERZ_STORE_ID=...`
- `SSL_COMMERZ_STORE_PASSWORD=...`
- `SSL_COMMERZ_SANDBOX_MODE=False` (or `True` for sandbox/testing)

## 5) Important Notes

- Do not commit `.env` to version control.
- For production, use a managed Postgres database if possible.
- Run `python manage.py check --deploy` before going live.
