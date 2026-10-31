"""angOrderQ: Order Queue System for Local Stalls & Vendors.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
import os
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import Service, Ticket, User, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)

@app.cli.command("seed")
def seed():
    """Add the starting food categories if they are not there yet."""
    starting = [
        ("Meals & Combos", 10),
        ("Drinks & Beverages", 5),
        ("Snacks & Sides", 5),
    ]
    for name, minutes in starting:
        exists = db.session.scalar(db.select(Service).filter_by(name=name))
        if exists is None:
            db.session.add(Service(name=name, avg_minutes=minutes))
    db.session.commit()
    print("Services are ready.")

@app.route("/")
def index():
    return render_template("index.html")


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)

    # Count how many tickets for the same service are still waiting ahead of this one
    ahead = [
        x for x in TICKETS
        if x["service_id"] == t["service_id"]
        and x["status"] == "waiting"
        and x["number"] < t["number"]
    ]
    service = next((s for s in SERVICES if s["id"] == t["service_id"]), None)

    return render_template(
        "ticket.html",
        ticket=t,
        service=service,
        ahead=len(ahead),
        tickets=TICKETS  # Passed for the live claim board
    )


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
        
    ahead = sum(
        1 for x in TICKETS
        if x["service_id"] == t["service_id"]
        and x["status"] == "waiting"
        and x["number"] < t["number"]
    )
    
    # Active ticket numbers for the live claim board
    waiting_numbers = [x["number"] for x in TICKETS if x["status"] == "waiting"]
    called_numbers = [x["number"] for x in TICKETS if x["status"] == "called"]

    return {
        "status": t["status"],
        "ahead": ahead,
        "waiting": waiting_numbers,
        "called": called_numbers,
    }


@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)

    t["status"] = "no-show"
    flash(f"Order #{ticket_id} was cancelled. You have left the queue.", "info")
    return redirect(url_for("index"))

def all_services():
    """Fetch all food categories ordered by name."""
    return db.session.scalars(db.select(Service).order_by(Service.name)).all()

@app.get("/join")
def join_form():
    return render_template("join.html", services=all_services(), form={}, errors={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)
    order_type = form.get("order_type", "").strip()
    service = db.session.get(Service, service_id) if service_id else None
    errors = {}
    if not name or len(name) > 80:
        errors["name"] = "Enter your name or nickname (up to 80 characters)."
    if not email or "@" not in email or "." not in email or len(email) > 120:
        errors["email"] = "Enter a valid email address (e.g. name@example.com)."
    if service is None:
        errors["service_id"] = "Choose a food category."
    if order_type not in ["Dine-in", "Take-out"]:
        errors["order_type"] = "Select either Dine-in or Take-out."
    if errors:
        flash("Please fix the highlighted fields below.", "danger")
        return render_template("join.html", services=all_services(), form=form, errors=errors), 400
    # Find existing customer or create new one
    user = db.session.scalar(db.select(User).filter_by(email=email))
    if user is None:
        user = User(name=name, email=email, role="customer")
        db.session.add(user)
    else:
        user.name = name  # Update name in case customer updated their preferred nickname
    # Assign ticket sequence number (starts at 101)
    max_num = db.session.scalar(db.select(func.max(Ticket.number)))
    next_num = (max_num + 1) if max_num else 101
    ticket = Ticket(
        number=next_num,
        user=user,
        service=service,
        order_type=order_type,
        status="waiting",
    )
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Something went wrong saving your ticket. Please try again.", "danger")
        return render_template("join.html", services=all_services(), form=form, errors={}), 409
    flash(f"You joined the queue! Your ticket number is #{ticket.number}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    
    # Active orders only: 'waiting' or 'called'
    queue = [t for t in TICKETS if t["status"] in ("waiting", "called")]
    if service_id:
        queue = [t for t in queue if t["service_id"] == service_id]
        
    names = {s["id"]: s["name"] for s in SERVICES}

    # ★ Feature: Live waiting counts per food category for kitchen staff
    counts = {
        s["id"]: sum(1 for t in TICKETS if t["service_id"] == s["id"] and t["status"] in ("waiting", "called"))
        for s in SERVICES
    }
    total_active = sum(1 for t in TICKETS if t["status"] in ("waiting", "called"))

    return render_template(
        "staff.html",
        queue=queue,
        services=SERVICES,
        names=names,
        selected=service_id,
        counts=counts,
        total_active=total_active,
    )


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    action_map = {
        "call": "called",
        "serve": "served",
        "no-show": "no-show"
    }
    new_status = action_map.get(action)
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    
    if t is None or new_status is None:
        abort(404)
        
    t["status"] = new_status
    flash(f"Order #{ticket_id} ({t['name']}) marked as {new_status.title()}.", "info")

    # Retain the active category filter if staff was viewing one
    service_id = request.args.get("service_id", type=int)
    if service_id:
        return redirect(url_for("staff_dashboard", service_id=service_id))
    return redirect(url_for("staff_dashboard"))


@app.route("/hello")
def hello():
    return "Hello, CCC181!"


if __name__ == "__main__":
    app.run(debug=True)
