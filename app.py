"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

# Categories of items offered by the pop-up stall
SERVICES = [
    {"id": 1, "name": "Meals & Combos"},
    {"id": 2, "name": "Drinks & Beverages"},
    {"id": 3, "name": "Snacks & Sides"},
]

# Sample active tickets with custom 'order_type' field
# status must be one of: 'waiting', 'called', 'served', 'no-show'
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
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html", services=SERVICES, tickets=TICKETS)


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # Find the target ticket or 404
    target_ticket = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if not target_ticket:
        abort(404)

    # Calculate queue position among active waiting/called tickets
    active_queue = [t for t in TICKETS if t.get("status") in ("waiting", "called")]
    position = None
    for idx, t in enumerate(active_queue, start=1):
        if t["number"] == ticket_id:
            position = idx
            break

    # Look up the service name
    service = next((s for s in SERVICES if s["id"] == target_ticket.get("service_id")), None)

    return render_template(
        "ticket.html",
        ticket=target_ticket,
        position=position,
        service=service
    )


@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        order_type = request.form.get("order_type", "Dine-in").strip()
        service_id_raw = request.form.get("service_id", "").strip()

        errors = []
        if not name:
            errors.append("Please enter your name.")

        try:
            service_id = int(service_id_raw)
            if not any(s["id"] == service_id for s in SERVICES):
                errors.append("Please select a valid service category.")
        except (ValueError, TypeError):
            errors.append("Please select a service category.")

        if errors:
            return render_template(
                "join.html",
                errors=errors,
                services=SERVICES,
                form_data=request.form
            ), 400

        next_number = TICKETS[-1]["number"] + 1 if TICKETS else 101
        new_ticket = {
            "number": next_number,
            "name": name,
            "email": email,
            "service_id": service_id,
            "order_type": order_type if order_type in ("Dine-in", "Take-out") else "Dine-in",
            "status": "waiting",
        }
        TICKETS.append(new_ticket)
        # Redirect after POST to prevent duplicate submissions on refresh
        return redirect(url_for("ticket", ticket_id=next_number))

    return render_template("join.html", services=SERVICES, form_data={})


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
