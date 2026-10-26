"""angOrderQ: Order Queue System for Local Stalls & Vendors.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Secret key for flash messages

SERVICES = [
    {"id": 1, "name": "Meals & Combos"},
    {"id": 2, "name": "Drinks & Beverages"},
    {"id": 3, "name": "Snacks & Sides"},
]

TICKETS = [
    {
        "number": 101,
        "name": "Marco",
        "email": "marco@gmail.com",
        "service_id": 1,
        "order_type": "Take-out",
        "status": "waiting",
    },
    {
        "number": 102,
        "name": "Bea",
        "email": "bea@yahoo.com",
        "service_id": 2,
        "order_type": "Dine-in",
        "status": "called",
    },
]


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


@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)

    t["status"] = "no-show"
    flash(f"Order #{ticket_id} was cancelled. You have left the queue.", "info")
    return redirect(url_for("index"))


@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES, form={}, errors={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)
    order_type = form.get("order_type", "").strip()

    errors = {}
    if not name:
        errors["name"] = "Enter your name or nickname."

    if not email or "@" not in email or "." not in email:
        errors["email"] = "Enter a valid email address (e.g. name@example.com)."

    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a food category."

    if order_type not in ["Dine-in", "Take-out"]:
        errors["order_type"] = "Select either Dine-in or Take-out."

    if errors:
        flash("Please fix the highlighted fields below.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400

    number = TICKETS[-1]["number"] + 1 if TICKETS else 101
    TICKETS.append({
        "number": number,
        "name": name,
        "email": email,
        "service_id": service_id,
        "order_type": order_type,
        "status": "waiting"
    })
    flash(f"You joined the queue! Your ticket number is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))


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
