# angOrderQ

> Real-Time Order Queue System for Local Pop-up Food Stalls & Night Market Vendors.

Built for **CCC181**.

---

## About the Setting
**angOrderQ** is designed for bustling outdoor food bazaars, night markets, and street pop-up stalls. 
- **For Customers:** Place quick food orders from your phone, choose Dine-in or Take-out, and monitor your queue position remotely via a live Jollibee-style claim board without having to crowd around smoky fryers.
- **For Stall Operators:** A fat-finger-friendly tablet dashboard designed for greasy hands and fast kitchen turnover, featuring category filtering, live wait counts, and one-tap order calling and completion.

*Note: Staff authentication will be introduced in a future update. For MVP testing, the Staff Dashboard (`/staff`) is open.*

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

4. **Run the development server:**
   ```bash
   flask --app app run --debug
   ```
   Open `http://127.0.0.1:5000` in your browser.
