🌍 Desh-Ghuri Web – Travel Booking Platform

Desh-Ghuri is a modern Django-based travel booking platform with role-based authentication, package management, booking system, and integrated payment gateway support. It is designed for travelers and tour guides with a complete end-to-end booking flow.

🚀 Key Features
👤 Role-based system (Traveler / Tour Guide)
🧳 Travel package listing and management
📅 Booking system with dashboard support
💳 Payment integration (SSLCommerz)
🔐 Authentication system with Django
📊 Admin + user dashboards
⚙️ Modular Django app structure
🧰 Tech Stack
Backend: Django (Python)
Database: SQLite / PostgreSQL (production recommended)
Frontend: Django Templates (HTML, CSS)
Payments: SSLCommerz
Deployment: Render / Vercel (config included)
📁 Project Structure
Desh-Ghuri/
│── api/
│── auth_app/
│── bookings/
│── core/
│── payments/
│── static/
│── manage.py
│── requirements.txt
│── vercel.json
│── .env.example
│── .gitignore
└── README.md
⚙️ Local Setup
1. Clone Repository
git clone https://github.com/istewakhassantewak/desh-ghuri.git
cd desh-ghuri
2. Create Virtual Environment
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
3. Install Dependencies
pip install -r requirements.txt
4. Setup Environment

Copy .env.example → .env and configure:

SECRET_KEY
DEBUG
ALLOWED_HOSTS
BASE_URL
SSLCommerz credentials
5. Run Migrations
python manage.py migrate
6. Start Server
python manage.py runserver

Visit:
👉 http://127.0.0.1:8000/

🌐 Deployment (Render)
Build Command
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
Start Command
gunicorn core.wsgi:application
🔐 Environment Variables (Production)
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=your-domain.com
BASE_URL=https://your-domain.com
SSL_COMMERZ_STORE_ID=...
SSL_COMMERZ_STORE_PASSWORD=...
SSL_COMMERZ_SANDBOX_MODE=False
⚠️ Important Notes
Never commit .env file
Use PostgreSQL in production
Run deployment check:
python manage.py check --deploy
👨‍💻 Author

Istewak Hassan Tewak

GitHub: https://github.com/istewakhassantewak
Portfolio: desh-ghuri-web.vercel.app
