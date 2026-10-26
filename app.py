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


@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"


@app.route("/hello")
def hello():
    return "Hello, CCC181!"


if __name__ == "__main__":
    app.run(debug=True)
