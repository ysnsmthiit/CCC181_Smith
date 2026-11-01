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
from datetime import timedelta, timezone

PH_TIME = timezone(timedelta(hours=8))  # Philippine time has no daylight saving

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)


@app.template_filter("local")
def local_time(value):
    """Format a UTC timestamp in Philippine Time."""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""

def people_ahead(t):
    """Count tickets waiting for the same food category that joined before ticket t."""
    stmt = (
        db.select(func.count(Ticket.id))
        .where(
            Ticket.service_id == t.service_id,
            Ticket.status == "waiting",
            Ticket.created_at < t.created_at,
        )
    )
    return db.session.scalar(stmt) or 0


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
    t = db.get_or_404(Ticket, ticket_id)
    # Fetch active tickets for the live status board
    active_tickets = db.session.scalars(
        db.select(Ticket).where(Ticket.status.in_(["waiting", "called"])).order_by(Ticket.created_at)
    ).all()
    return render_template(
        "ticket.html",
        ticket=t,
        service=t.service,
        ahead=people_ahead(t),
        tickets=active_tickets,
    )


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    waiting_numbers = db.session.scalars(
        db.select(Ticket.number).where(Ticket.status == "waiting").order_by(Ticket.created_at)
    ).all()
    called_numbers = db.session.scalars(
        db.select(Ticket.number).where(Ticket.status == "called").order_by(Ticket.called_at)
    ).all()
    return {
        "status": t.status,
        "ahead": people_ahead(t),
        "waiting": waiting_numbers,
        "called": called_numbers,
    }


@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    """Soft delete: preserves the record for reporting with status cancelled."""
    t = db.get_or_404(Ticket, ticket_id)
    if t.status in ("waiting", "called"):
        t.status = "cancelled"
        db.session.commit()
    flash(f"Order #{t.number} was cancelled. You have left the queue.", "info")
    return redirect(url_for("index"))


@app.get("/join")
def join_form():
    return render_template("join.html", services=active_services(), form={}, errors={})


@app.post("/staff/tickets/<int:ticket_id>/delete")
def delete_ticket(ticket_id):
    """Hard delete: completely removes a mistaken or test ticket."""
    t = db.get_or_404(Ticket, ticket_id)
    ticket_num = t.number
    db.session.delete(t)
    db.session.commit()
    flash(f"Order #{ticket_num} was permanently deleted.", "warning")
    return redirect(url_for("staff_dashboard"))


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
    if service is None or not service.active:
        errors["service_id"] = "Choose an active food category."
    if order_type not in ["Dine-in", "Take-out"]:
        errors["order_type"] = "Select either Dine-in or Take-out."
    if errors:
        flash("Please fix the highlighted fields below.", "danger")
        return render_template("join.html", services=active_services(), form=form, errors=errors), 400
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
        return render_template("join.html", services=active_services(), form=form, errors={}), 409
    flash(f"You joined the queue! Your ticket number is #{ticket.number}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    stmt = (
        db.select(Ticket)
        .where(Ticket.status.in_(["waiting", "called"]))
        .order_by(Ticket.created_at)
    )
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    queue = db.session.scalars(stmt).all()
    services = all_services()
    counts = {
        s.id: db.session.scalar(
            db.select(func.count(Ticket.id)).where(
                Ticket.service_id == s.id, Ticket.status.in_(["waiting", "called"])
            )
        )
        for s in services
    }
    total_active = sum(counts.values())
    return render_template(
        "staff.html",
        queue=queue,
        services=services,
        selected=service_id,
        counts=counts,
        total_active=total_active,
    )


STAFF_ACTIONS = {"call": "called", "serve": "served", "no-show": "no-show"}
@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = STAFF_ACTIONS.get(action)
    if new_status is None:
        abort(404)
    t = db.get_or_404(Ticket, ticket_id)
    t.status = new_status
    if new_status == "called":
        t.called_at = func.now()
    elif new_status == "served":
        t.served_at = func.now()
    db.session.commit()
    flash(f"Order #{t.number} ({t.user.name}) marked as {new_status.title()}.", "info")
    service_id = request.args.get("service_id", type=int)
    if service_id:
        return redirect(url_for("staff_dashboard", service_id=service_id))
    return redirect(url_for("staff_dashboard"))


def all_services():
    """Fetch all food categories ordered by name (for staff management)."""
    return db.session.scalars(db.select(Service).order_by(Service.name)).all()


def active_services():
    """Fetch only active food categories for the customer join form."""
    stmt = db.select(Service).filter_by(active=True).order_by(Service.name)
    return db.session.scalars(stmt).all()


@app.get("/staff/services")
def services_list():
    services = all_services()
    return render_template("services.html", services=services)


@app.post("/staff/services")
def service_create():
    name = request.form.get("name", "").strip()
    minutes = request.form.get("avg_minutes", type=int)
    if not name or len(name) > 60 or not minutes or minutes <= 0:
        flash("Enter a category name (up to 60 chars) and prep time greater than 0.", "danger")
        return redirect(url_for("services_list"))
    db.session.add(Service(name=name, avg_minutes=minutes, active=True))
    try:
        db.session.commit()
        flash(f"Category '{name}' added successfully.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A food category named '{name}' already exists.", "danger")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>")
def service_edit(service_id):
    s = db.get_or_404(Service, service_id)
    name = request.form.get("name", "").strip()
    minutes = request.form.get("avg_minutes", type=int)
    s.active = request.form.get("active") == "on"

    if not name or len(name) > 60 or not minutes or minutes <= 0:
        flash("Enter a valid name (up to 60 chars) and prep time greater than 0.", "danger")
        return redirect(url_for("services_list"))

    s.name = name
    s.avg_minutes = minutes
    try:
        db.session.commit()
        flash(f"Category '{name}' updated.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A food category named '{name}' already exists.", "danger")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>/delete")
def service_delete(service_id):
    s = db.get_or_404(Service, service_id)
    if s.tickets:
        flash(f"'{s.name}' has existing ticket orders and cannot be deleted. Toggle it inactive instead.", "danger")
        return redirect(url_for("services_list"))
    db.session.delete(s)
    db.session.commit()
    flash(f"Category '{s.name}' was deleted.", "warning")
    return redirect(url_for("services_list"))


@app.route("/hello")
def hello():
    return "Hello, CCC181!"


if __name__ == "__main__":
    app.run(debug=True)
