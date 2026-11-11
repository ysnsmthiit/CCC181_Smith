# angOrderQ

> Real-Time Order Queue System for Local Food Stalls & Pop-up Vendors.

Built for **CCC181**.

---

## About the Setting
**angOrderQ** is designed for bustling local food stalls, kiosks, and pop-up food vendors. 
- **For Customers:** Place quick food orders from your phone, choose Dine-in or Take-out, and monitor your queue position remotely via a live claim board without having to crowd around smoky fryers.
- **For Stall Operators:** A fat-finger-friendly tablet dashboard designed for fast kitchen turnover, featuring category filtering, live wait counts, and one-tap order calling, serving, and completion.

*Note: Staff authentication will be introduced in Week 11. For MVP testing, the Staff Dashboard (`/staff`) and Category Management (`/staff/services`) are open.*

---

## Documentation
- [Project Requirements](docs/requirements.md)
- [Week 4 Schema & ERD](docs/week4/schema.md)
- [Week 4 Persistence Proof](docs/week4/persistence.md)
- [Week 4 Report](docs/week4/report.md)

---

## Setup & Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ysnsmthiit/CCC181_Smith.git
   cd CCC181_Smith
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Copy `.env.example` to `.env` and configure your local PostgreSQL password:
   ```bash
   # Windows PowerShell:
   Copy-Item .env.example .env
   # macOS/Linux:
   cp .env.example .env
   ```

5. **Start PostgreSQL in Docker:**
   ```bash
   docker compose up -d
   ```
   Verify status shows healthy with `docker compose ps`.

6. **Run database migrations and seed data:**
   ```bash
   flask --app app db upgrade
   flask --app app seed
   ```

7. **Run the development server:**
   ```bash
   flask --app app run --debug
   ```
   Open `http://127.0.0.1:5000` in your browser.
