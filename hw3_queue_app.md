# Start Your Own Queue App

| | |
| --- | --- |
| **Topic** | User-centered interface development |
| **Common application** | Queue Management System |
| **Course learning outcomes** | CLO 1, CLO 2 |
| **Points** | 100 |
| **Format** | Self-paced and asynchronous. Work through Parts 0 to 10 in order, at your own pace. |
| **Released** | Monday, October 19, 2026 |
| **Due** | **TBD** |
| **Type** | Individual |

## Overview

In Week 1 you chose a real setting, interviewed people who wait and people who serve, and wrote your requirements. In Week 2 you learned Flask with the ClinicQ starter. **This week you start your own app.** By the end of this activity your repository holds the first working version of *your* queue system, with three real screens:

1. **Join the queue** (for the person waiting): a form that gives them a ticket.
2. **My place** (for the person waiting): their ticket number, status and position in line.
3. **Staff dashboard** (for the staff member): the waiting list in order, with buttons to call, serve, or mark a no-show.

You will write personas for your app, design the screens for them, then build them with Flask, Jinja and Bootstrap so they work on a phone and on a laptop, check them for accessibility, add one small JavaScript behavior, and test them with a real user.

Everything you build this week is the base for the rest of the semester. In Week 4 the tickets move from a Python list into PostgreSQL, in Week 6 the same data is served by a REST API, and from Week 8 your Flutter app talks to it. Build it for your setting, not for ClinicQ.

**How to use this activity.** Each part ends with a **Checkpoint**. Do not move on until every box in the checkpoint is true, and commit your work at each one. ClinicQ appears in the examples only to show the idea; replace every ClinicQ name, service and field with your own.

### What you need

- Your Week 1 proposal and interview notes (your profiles, research and requirement IDs, such as FR-01)
- Your individual GitHub repository from Week 2
- Python 3.11 or newer, VS Code, Git, and Google Chrome (for Lighthouse)
- The Week 2 starter app (`my-app` with the join-queue demo), from the Week 2 materials
- About 9 to 11 hours spread across the week

### Time plan

| Part | What you do | Time |
| --- | --- | --- |
| 0 | Turn the starter into your own app | 45 min |
| 1 | Build the personas for your app | 1 h |
| 2 | Wireframe your three screens | 1 h |
| 3 | Self-review of personas and wireframes | 45 min |
| 4 | Bootstrap layout and navigation | 1 h |
| 5 | Join form with validation | 1.5 h |
| 6 | My place page | 45 min |
| 7 | Staff dashboard | 1.5 h |
| 8 | A small JavaScript behavior | 45 min |
| 9 | Accessibility check | 45 min |
| 10 | Usability test, one fix, and submission | 1.5 h |

---

## Part 0: Turn the starter into your own app

**Goal:** your repository runs a Flask app with **your** system's name, **your** services, and the fields **your** requirements need.

1. In your repository, create a GitHub issue:
   - **Title:** `Week 3: first interface (join, my place, staff dashboard)`
   - **Description:** list the Week 1 requirement IDs this week covers (at least your join, queue-position and staff requirements, for example FR-01, FR-02, FR-04).
   - **Labels:** `feature`, `Must` · **Milestone:** MVP
2. Branch from an up-to-date `main`:

   ```
   git switch main
   git pull origin main
   git switch -c feature/week3-interface
   ```

3. Copy the Week 2 starter files (`app.py`, `requirements.txt`, `.gitignore`, `templates/`, `static/`) into the root of your repository, if they are not there already. Keep your `docs/week1/` folder.
4. Create and activate a virtual environment, install the packages, and run the app:

   ```
   python -m venv .venv
   # Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   flask --app app run --debug
   ```

5. **Make it yours.** In `app.py`, replace the ClinicQ sample data with your setting's data. Add a `SERVICES` list with the real services from your proposal, and give each ticket the fields your requirements mention. ClinicQ's version, as an example:

   ```python
   SERVICES = [
       {"id": 1, "name": "Consultation"},
       {"id": 2, "name": "Medical certificate"},
   ]

   # Each ticket: number, name, email, service_id, status
   # status is one of: waiting, called, served, no-show
   TICKETS = [
       {"number": 1, "name": "Ana", "email": "ana@school.edu", "service_id": 1, "status": "waiting"},
       {"number": 2, "name": "Ben", "email": "ben@school.edu", "service_id": 2, "status": "waiting"},
   ]
   ```

   A barbershop might use services like *Haircut* and *Shave* and add a `preferred_barber` field. A registrar with a priority lane might add `priority: True/False`. Use what **your** Week 1 requirements say.

6. Rename the app everywhere a user can see it: the `<title>` and header in `templates/base.html`, and the README. Update `README.md` with one paragraph: your system's name, your setting, and how to run it.

**Checkpoint 0**

- [x] The app runs with `flask --app app run --debug` and shows your system's name, not ClinicQ.
- [x] `SERVICES` holds your real services, and tickets have a `status`.
- [x] You committed: `git commit -m "Set up <YourApp> from the Week 2 starter (#<issue>)"`

---

## Part 1: Build the personas for your app

**Goal:** two personas, based on your Week 1 research, that you will design for and test against for the rest of the week. Every later part refers back to them.

In Week 1 you wrote short profiles. This week you turn them into full personas for **your version of ClinicQ**: one for the **person waiting** and one for the **staff member**. A persona is not an invented user. Everything in it should come from what you heard or saw in your interviews and observation. If you need more detail, go back and talk to one more person in your setting.

Create `docs/week3/personas.md` and fill in this template **once for each persona**:

```markdown
## [Fictional name], the [person waiting | staff member]

> "[A real quote from your Week 1 interviews that sums up how this person feels]"

| | |
| --- | --- |
| **Photo or sketch** | [A drawing, an icon, or a free stock photo. Never a photo of the real person you interviewed.] |
| **Age, role and background** | [e.g. 19, 2nd-year IT student, commutes, has back-to-back classes] |
| **Goals** | [2–3 things they want to get done when they come to your setting] |
| **Frustrations** | [2–3 pain points with the current queue, from your research] |
| **Devices and context** | [Which device, where, and what else they are doing at the same time] |
| **Tech comfort** | [Low / Medium / High, with a short reason] |
| **Accessibility needs** | [e.g. older eyes need larger text, one hand busy, noisy room, shared PC, slow mobile data] |

### Scenario

[One short paragraph, a story of one real visit from arriving to being served, written in the present tense.
Show the moment when they would open your app and what they need from it.]

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| [e.g. Join the queue for ID release] | Join | FR-01 |
| [e.g. Check how many people are ahead] | My place | FR-02 |
| [ ... ] | | |

### What this means for my interface

1. [Because ..., my interface must ...]
2. [Because ..., my interface must ...]
3. [Because ..., my interface must ...]
```

A ClinicQ example of the last section, for the student persona:

> 1. Because Mika checks her phone while walking between classes, her ticket number and position must be the biggest thing on My place.
> 2. Because she uses mobile data that is often slow, pages must load fast and work without large images.
> 3. Because she may be called while still in class, the status must change by itself without her refreshing.

Rules for good personas:

- Use **at least one real quote** and **at least two details** from your Week 1 notes in each persona. Mark them with *(interview)* or *(observation)*.
- The two personas must be **clearly different from ClinicQ's** and from each other.
- Each persona needs **at least three** *"Because …, my interface must …"* statements. You will use them as your design rules in Parts 2, 5, 6 and 7, and check them in Part 10.
- If your setting has an important third user, such as a senior citizen in a priority lane or an office head who reads reports, you may add a third persona. It is optional.

**Checkpoint 1**

- [x] `docs/week3/personas.md` has two complete personas: the person waiting and the staff member.
- [x] Each persona has a real quote, a scenario, a top-tasks table with requirement IDs, and at least three *"Because …, my interface must …"* statements.
- [x] No photo of a real person you interviewed is used.
- [x] Committed: `git commit -m "Add Week 3 personas (#<issue>)"`

---

## Part 2: Wireframe your three screens

**Goal:** decide what each screen shows and where, **before** writing HTML.

Draw low-fidelity wireframes: boxes, labels and placeholder text, no colors or images. Use paper and a pen (take a clear photo), or a free tool such as Excalidraw, draw.io, Figma or Penpot.

Draw **each of the three screens twice**, once at **phone width** and once at **laptop width**, so six frames in total. For each frame:

- Write which **persona** from Part 1 uses it (by name) and on which device.
- Label every element: headings, inputs, buttons, the ticket number, status, and position.
- Number the main user flow with arrows: *open the site → join → see my place*, and *staff opens dashboard → calls next → marks served*.
- Next to the screen, write the **requirement IDs** it covers (for example "FR-01, FR-03").

Ask yourself, using your personas and their *"Because …, my interface must …"* statements:

- What is the **one thing** the person waiting must see first on My place? (Usually their number and position, large.)
- What does the staff member do **most often**? Put that button where it is easiest to reach.
- What will they be holding or doing while they use it? (A phone in one hand, a busy counter, a shared office PC.)

Save the files as `docs/week3/wireframes/` (PNG, JPG or PDF), for example `join-phone.png`, `join-laptop.png`, and so on.

**Checkpoint 2**

- [x] Six frames: three screens, each at phone and laptop width.
- [x] Every frame names the persona, the device, and the requirement IDs.
- [x] The main flow for each persona is marked with arrows.
- [x] Committed in `docs/week3/wireframes/`.

---

## Part 3: Self-review of your personas and wireframes

**Goal:** check your design against your personas before you build it.

Put your personas and wireframes away for at least an hour, then come back and review them as if they were someone else's. Answer these questions **for each screen**, looking at both the phone and the laptop frame:

1. Can my persona tell what to do on this screen within 5 seconds?
2. Is the ticket status always visible where the person needs it?
3. Do the words match what people in my setting actually say? (For example "window" or "counter", "number" or "ticket".)
4. Is the action the staff member does most often the easiest one to reach?
5. Does the phone version still show the most important thing first?
6. Which of my *"Because …, my interface must …"* rules does this screen follow, and which does it break?

Then write the review in `docs/week3/feedback.md` using this format, once per screen:

> **Works well:** one thing that works and why.
> **Problem:** one problem your persona would hit, linked to a usability principle (visibility of status, match with the real world, error prevention, consistency, or recognition rather than recall).
> **Change:** what you will change in the wireframe, or why you will keep it.

Update your wireframes with the changes before you start Part 4.

**Checkpoint 3**

- [x] `docs/week3/feedback.md` has a review of all three screens in the *Works well / Problem / Change* format.
- [x] Your wireframes are updated, or `feedback.md` explains why you kept them.
- [x] Committed.

---

## Part 4: Bootstrap layout and navigation

**Goal:** a shared layout that every page uses, with a navigation bar that collapses on a phone.

Replace the contents of `templates/base.html` with a Bootstrap 5 layout. Keep your own name and colors.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}YourApp{% endblock %}</title>
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body class="d-flex flex-column min-vh-100">
  <a class="visually-hidden-focusable" href="#main">Skip to main content</a>

  <nav class="navbar navbar-expand-md bg-primary" data-bs-theme="dark">
    <div class="container">
      <a class="navbar-brand" href="{{ url_for('index') }}">YourApp</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
              data-bs-target="#mainNav" aria-controls="mainNav"
              aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="mainNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link {% if request.endpoint == 'join_form' %}active{% endif %}"
               {% if request.endpoint == 'join_form' %}aria-current="page"{% endif %}
               href="{{ url_for('join_form') }}">Join the queue</a>
          </li>
          <li class="nav-item">
            <a class="nav-link {% if request.endpoint == 'staff_dashboard' %}active{% endif %}"
               {% if request.endpoint == 'staff_dashboard' %}aria-current="page"{% endif %}
               href="{{ url_for('staff_dashboard') }}">Staff</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <main id="main" class="container my-4 flex-grow-1">
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% for category, message in messages %}
        <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
          {{ message }}
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
      {% endfor %}
    {% endwith %}

    {% block content %}{% endblock %}
  </main>

  <footer class="border-top py-3 text-center text-body-secondary small">
    YourApp · CCC181
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <script src="{{ url_for('static', filename='js/main.js') }}"></script>
  {% block scripts %}{% endblock %}
</body>
</html>
```

What to notice:

- **`navbar-expand-md`** shows the full menu from medium screens up and collapses it into the ☰ button on a phone.
- **`container`** keeps content at a readable width and adds side padding on small screens.
- **Flash messages** appear as Bootstrap alerts. You will use them in Part 5.
- The **skip link** and **`aria-current="page"`** help keyboard and screen-reader users. You will check these in Part 9.

Flash messages need a secret key. Add this to `app.py` right after `app = Flask(__name__)`, and import `flash`:

```python
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable
```

Until Parts 5 and 7 add the `join_form` and `staff_dashboard` routes, the links above will raise an error. **Delete the old Week 2 `join()` route**, and add two placeholder routes so the page loads:

```python
@app.route("/join")
def join_form():
    return render_template("join.html")

@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"
```

Make the home page (`index.html`) a short welcome for the person waiting: your app's name, one sentence on what it does, and a large **Join the queue** button (`class="btn btn-primary btn-lg"`). Remove the old ticket list from it; staff will see the list on their dashboard.

**Checkpoint 4**

- [x] Every page shows the navbar, flash area and footer from `base.html`.
- [x] In Chrome DevTools device mode (Ctrl+Shift+M), at 375 px wide the menu collapses into ☰ and opens when tapped.
- [x] The active page is highlighted in the menu.
- [x] Committed: `git commit -m "Add Bootstrap layout and navigation (#<issue>)"`

---

## Part 5: Join form with validation

**Goal:** the person waiting can join the queue for one of your services, and gets a clear message if something is wrong.

Replace the placeholder `join_form` route with two routes: one shows the form, one handles the submission.

```python
@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES, form={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)

    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    if "@" not in email:
        errors["email"] = "Enter a valid email address."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append({"number": number, "name": name, "email": email,
                    "service_id": service_id, "status": "waiting"})
    flash(f"You joined the queue. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))
```

**Never trust form input.** The server checks every field even if the browser already did, because anyone can send a request without your form.

Now write `templates/join.html` with Bootstrap form classes. One field is shown; build the others the same way.

```html
{% extends "base.html" %}
{% block title %}Join the queue · YourApp{% endblock %}

{% block content %}
<div class="row justify-content-center">
  <div class="col-12 col-md-8 col-lg-6">
    <h1 class="h3 mb-3">Join the queue</h1>

    <form method="post" action="{{ url_for('join') }}" novalidate id="join-form">
      <div class="mb-3">
        <label for="name" class="form-label">Your name</label>
        <input id="name" name="name" type="text" autocomplete="name" required
               class="form-control {% if errors and errors.name %}is-invalid{% endif %}"
               value="{{ form.get('name', '') }}"
               {% if errors and errors.name %}aria-describedby="name-error"{% endif %}>
        {% if errors and errors.name %}
          <div id="name-error" class="invalid-feedback">{{ errors.name }}</div>
        {% endif %}
      </div>

      {# Add the email field (type="email", autocomplete="email") the same way #}

      <div class="mb-3">
        <label for="service_id" class="form-label">Service</label>
        <select id="service_id" name="service_id" required
                class="form-select {% if errors and errors.service_id %}is-invalid{% endif %}">
          <option value="">Choose a service…</option>
          {% for s in services %}
            <option value="{{ s.id }}"
              {% if form.get('service_id') == s.id|string %}selected{% endif %}>{{ s.name }}</option>
          {% endfor %}
        </select>
        {% if errors and errors.service_id %}
          <div class="invalid-feedback">{{ errors.service_id }}</div>
        {% endif %}
      </div>

      <button type="submit" class="btn btn-primary w-100">Get a ticket</button>
    </form>
  </div>
</div>
{% endblock %}
```

What to notice:

- Every input has a **`<label for>`** that matches its **`id`**. Placeholder text is not a label.
- After an error, the form **keeps what the user typed**, so they fix one field instead of retyping everything.
- `col-12 col-md-8 col-lg-6` makes the form full width on a phone and narrower on a laptop.

**Make it yours:** add the fields your setting needs from your Week 1 requirements (for example a student ID, a priority-lane checkbox, a preferred barber), with server-side checks for each.

**Checkpoint 5**

- [x] Submitting an empty form shows a red alert and a message under each wrong field, and keeps the typed values.
- [x] A valid submission redirects to My place with a green success alert.
- [x] At least one field specific to your setting is in the form and validated on the server.
- [x] Committed.

---

## Part 6: My place page

**Goal:** the person waiting sees, at a glance, their number, status and position.

Update the `ticket` route so it only counts people **still waiting** ahead of this ticket for the same service:

```python
@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    ahead = [x for x in TICKETS
             if x["service_id"] == t["service_id"]
             and x["status"] == "waiting"
             and x["number"] < t["number"]]
    service = next(s for s in SERVICES if s["id"] == t["service_id"])
    return render_template("ticket.html", ticket=t, service=service, ahead=len(ahead))
```

In `templates/ticket.html`, use a Bootstrap **card**. Follow your wireframe, but include at least:

- The ticket number, **large** (for example `class="display-1 fw-bold"`)
- The service name
- A **status badge** whose text says the status (`waiting`, `called`, `served`, `no-show`), not only its color, for example `<span class="badge text-bg-warning">Waiting</span>`
- Position as a sentence: *"2 people ahead of you"*, or *"You're next!"* when it is 0
- A **Leave the queue** button, as a small POST form to `/queue/<id>/leave` that sets the status to `no-show` (or `left`, if your setting uses that) and redirects home with a flash message

Wrap the status and position in an element with an id, such as `<div id="live-status" aria-live="polite">`. Part 8 updates it automatically.

**Checkpoint 6**

- [x] My place shows number, service, status badge and position, and reads clearly at 375 px.
- [x] Visiting a ticket number that does not exist shows a 404.
- [x] Leave the queue works and shows a flash message.
- [x] Committed.

---

## Part 7: Staff dashboard

**Goal:** the staff member sees the waiting list in order and acts on it with one click.

Add the dashboard and one route for each staff action. Actions that **change data use POST**, never a plain link, so a browser prefetch or a refresh cannot serve someone by accident.

```python
@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    queue = [t for t in TICKETS if t["status"] in ("waiting", "called")]
    if service_id:
        queue = [t for t in queue if t["service_id"] == service_id]
    names = {s["id"]: s["name"] for s in SERVICES}
    return render_template("staff.html", queue=queue, services=SERVICES,
                           names=names, selected=service_id)


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = {"call": "called", "serve": "served", "no-show": "no-show"}.get(action)
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None or new_status is None:
        abort(404)
    t["status"] = new_status
    flash(f"Ticket #{ticket_id} marked {new_status}.", "info")
    return redirect(url_for("staff_dashboard"))
```

In `templates/staff.html`:

- A **service filter** (a `<select>` in a GET form, or Bootstrap nav pills) so staff can see one service at a time.
- A **Call next** button at the top that calls the first waiting ticket.
- The queue as a **`table`** wrapped in `<div class="table-responsive">`, with columns for number, name, service, status and actions. Use `<th scope="col">` for headers and a `<caption>` that says what the table is.
- Each row's actions as small POST forms with buttons (`btn btn-sm btn-success` for Serve, `btn-outline-danger` for No-show). Give each button an `aria-label` that names the ticket, such as `aria-label="Mark ticket 14 as served"`, because a screen reader hears many identical "Serve" buttons otherwise.
- A friendly empty state when no one is waiting.

Staff login comes in a later week. For now the dashboard is open; say so in your README.

**Make it yours:** add one staff feature from your Week 1 requirements marked ★ (for example a priority lane shown first, a counter number, or a count of how many are waiting per service).

**Checkpoint 7**

- [x] The dashboard lists waiting and called tickets in order and filters by service.
- [x] Call next, Serve and No-show change the status, and the change shows on that ticket's My place page.
- [x] At 375 px the table scrolls sideways inside its box instead of breaking the page.
- [x] One ★ requirement from your setting is visible on the dashboard.
- [x] Committed.

---

## Part 8: A small JavaScript behavior

**Goal:** two small improvements that make the screens feel responsive. Do both.

**8a. Stop double joining.** When the join form is submitted, disable its button and change the text, so an impatient tap does not create two tickets. In `static/js/main.js`:

```javascript
const joinForm = document.getElementById("join-form");
if (joinForm) {
  joinForm.addEventListener("submit", () => {
    const button = joinForm.querySelector("button[type=submit]");
    button.disabled = true;
    button.textContent = "Getting your ticket…";
  });
}
```

**8b. Keep My place up to date.** Add a JSON route in `app.py`:

```python
@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    ahead = sum(1 for x in TICKETS
                if x["service_id"] == t["service_id"]
                and x["status"] == "waiting" and x["number"] < t["number"])
    return {"status": t["status"], "ahead": ahead}
```

Then, at the bottom of `ticket.html`, fetch it every 10 seconds and update the page without a reload:

```html
{% block scripts %}
<script>
  const statusUrl = "{{ url_for('ticket_status', ticket_id=ticket.number) }}";
  async function refreshStatus() {
    try {
      const res = await fetch(statusUrl);
      if (!res.ok) return;
      const data = await res.json();
      // Update the badge text and the "people ahead" sentence here,
      // using the ids you gave them in Part 6.
    } catch (err) {
      console.warn("Could not refresh status", err);
    }
  }
  setInterval(refreshStatus, 10000);
</script>
{% endblock %}
```

Finish the two lines inside `refreshStatus` yourself. Test it with two browser windows side by side: My place in one, the staff dashboard in the other. Call the ticket from the dashboard, and within 10 seconds My place should show *Called* without you refreshing it. Week 6 turns this JSON route into a proper REST API.

**Checkpoint 8**

- [ ] Double-clicking Get a ticket creates only one ticket.
- [ ] My place updates its status and position within 10 seconds after a staff action, with no reload.
- [ ] Nothing in the browser console is red.
- [ ] Committed.

---

## Part 9: Accessibility check

**Goal:** make sure people using a keyboard, a screen reader, or a small screen can use every screen.

Do all three checks on **all three screens**, and record the results in `docs/week3/accessibility.md`.

**9a. Lighthouse.** In Chrome, open DevTools → **Lighthouse** → select **Accessibility** and **Mobile** → **Analyze page load**. Record the score for each screen. **Aim for 90 or higher.** Fix every issue it lists that you can, and run it again. Take a screenshot of each final score.

**9b. Keyboard only.** Put your mouse away. Using only Tab, Shift+Tab, Enter, Space and the arrow keys:

- Join the queue from the home page.
- On the staff dashboard, filter by a service, call a ticket, and serve it.

Can you see where the focus is at every step? Can you reach and use every control? Does the skip link appear on the first Tab? Write down anything that failed and how you fixed it.

**9c. Manual checklist.** Check each item and mark it ✅ or ❌ (with the fix):

| Check | Join | My place | Staff |
| --- | --- | --- | --- |
| Every input has a visible label | | | |
| Error messages say what to do, in text | | | |
| Status is shown in words, not only color | | | |
| Text and buttons are readable at 375 px with no sideways page scroll | | | |
| Buttons are at least about 44 × 44 px on a phone | | | |
| Page has one `<h1>` and headings in order | | | |
| `<html lang="en">` (or your language) is set | | | |

**Checkpoint 9**

- [ ] `docs/week3/accessibility.md` has a Lighthouse score and screenshot for each screen, the keyboard test notes, and the completed checklist.
- [ ] Each screen scores 90 or higher, or the file explains what is left and why.
- [ ] Committed.

---

## Part 10: Usability test, one fix, and submission

### 10a. Test with a real user (asynchronous)

Find **one person** to try your app who matches one of your personas, ideally someone from your Week 1 setting. Not a CCC181 classmate. You can meet in person, or do it over a video call where they share their screen, or ask them to record their screen on their own phone.

Run the app on your laptop and let them use it (or, for a phone test, open it on your phone on the same Wi-Fi with `flask --app app run --debug --host 0.0.0.0` and visit your laptop's IP address).

Give them these three tasks, one at a time, and **do not help**. Ask them to think aloud.

1. "You just arrived. Get in line for **[one of your services]**."
2. "How many people are ahead of you? What is your number?"
3. "Pretend you are the staff member. Call the next person and mark them as served."

For each task, note in `docs/week3/usability-test.md`:

- Did they finish it? (yes / with help / no)
- About how long it took
- Where they hesitated, what they said, and anything that surprised you
- Which of your persona's *"Because …, my interface must …"* rules held up, and which did not

Ask their permission before recording, and do not include their full name or face.

### 10b. Make one improvement

Pick the **most serious problem** you found, from the usability test, your self-review, or the accessibility check. Fix it, and in `usability-test.md` describe the problem, your fix, and a before-and-after screenshot.

### 10c. Write your report in your repository

Write a short report in Markdown at `docs/week3/report.md` on your `feature/week3-interface` branch, using the sections below. Put your screenshots in `docs/week3/screenshots/` and show them in the report with relative links, such as `![Join on a phone](screenshots/join-phone.png)`, so they display on GitHub.

Report sections, using `##` headings:

1. **Title details:** your app's name, setting, full name, student ID, section, date, and the **link to your pull request**
2. **Personas:** a short summary of your two personas (name, one quote, top tasks), with a link to `docs/week3/personas.md`
3. **Screens:** six screenshots (three screens, phone and laptop), each with one sentence on which persona uses it and which requirement IDs it covers
4. **Design decisions:** three decisions you made and why, each tied to your personas, your wireframes or your self-review (for example *"I put the ticket number at the top in very large text because the waiting student in my interview said they check their phone while walking."*)
5. **Self-review:** the main problems you found in your wireframes and what you changed (from `feedback.md`)
6. **Accessibility:** Lighthouse scores and the most important issue you fixed
7. **Usability test:** the results for each task and the one improvement you made, with before and after
8. **Reflection:** what was hardest this week, and what you will change in your interface when the data moves to a database in Week 4
9. **Declaration:** any AI tools or outside sources you used and what for. Write "None" if you used none.

Commit it: `git commit -m "Add Week 3 report (#<issue>)"`. Then open your branch on GitHub and check that every heading, table and screenshot displays correctly.

### 10d. Open and merge your pull request, then submit the link

1. Push your branch: `git push -u origin feature/week3-interface`
2. Open a pull request into `main`.
   - **Title:** `Week 3: first interface for <YourApp>`
   - **Description:** `Closes #<issue>`, the requirement IDs covered, and **six screenshots**: each screen at phone width and at laptop width.
3. Review your own diff on GitHub. Make sure there is no `.venv/` folder and no `__pycache__/`.
4. **Merge** the pull request into `main`, then tag it:

   ```
   git switch main
   git pull origin main
   git tag week3
   git push origin week3
   ```

5. **Submit on MOLE.** In the **Week 3 assignment on MOLE**, submit the link to your report at the `week3` tag:

   ```
   https://github.com/<your-username>/<your-repo>/blob/week3/docs/week3/report.md
   ```

   Linking to the tag means your instructor sees exactly the version you submitted, even if you keep working on `main` afterward. Open the link in a private browser window first to check that it works. If your repository is private, add your instructor as a collaborator so they can open it.

**Checkpoint 10 (submission)**

- [ ] Usability test notes and the improvement are in `docs/week3/usability-test.md`.
- [ ] `docs/week3/report.md` is in your repository and displays correctly on GitHub.
- [ ] Your pull request is **merged** into `main` and tagged `week3`.
- [ ] The link to your report at the `week3` tag is submitted to the **Week 3 assignment on MOLE** before the due date.

---

## What your repository should look like

```
your-repo/
├── app.py
├── requirements.txt
├── README.md                 # your app's name, setting, how to run it
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── join.html
│   ├── ticket.html
│   └── staff.html
├── static/
│   ├── css/style.css
│   └── js/main.js
└── docs/
    ├── week1/ proposal.md, proposal.pdf
    └── week3/
        ├── personas.md
        ├── wireframes/        # six frames
        ├── feedback.md
        ├── accessibility.md
        ├── usability-test.md
        ├── screenshots/
        └── report.md
```

## Rubric (100 points)

Each criterion is scored at one of four levels: **Exemplary** (100% of the points), **Proficient** (80%), **Developing** (60%), or **Beginning** (30% or less).

| Criterion | CLO | Points | Exemplary | Developing |
| --- | --- | --- | --- | --- |
| Personas | 1 | 10 | Two distinct personas grounded in real quotes and Week 1 research; scenario, top tasks with requirement IDs, and clear design rules | Generic or invented; copied from ClinicQ; no link to research or to the interface |
| Wireframes and design rationale | 1 | 10 | Six frames tied to named personas and requirement IDs; design decisions clearly traced to the personas and self-review | Missing frames or sizes; decisions not explained or not linked to users |
| Self-review | 1 | 10 | All three screens reviewed against the personas in the required format; problems linked to usability principles; wireframes updated | Vague or missing review; no changes made or explained |
| Responsive layout and navigation | 2 | 10 | Shared Bootstrap layout; collapsing navbar; all screens work at 375 px and laptop width | Layout breaks on a phone or pages do not share a layout |
| Forms and validation | 2 | 15 | Server-side validation of every field with clear messages; values kept on error; setting-specific field included | Validation only in the browser, or errors unclear |
| Queue screens for your setting | 2 | 15 | My place and staff dashboard work end to end with POST actions and service filter; a ★ requirement is visible; clearly built for your own setting | Only partly working, or still ClinicQ with names changed |
| JavaScript behavior | 2 | 5 | Double submit prevented and My place refreshes with fetch, no console errors | Only one behavior, or it errors |
| Accessibility check | 2 | 10 | Lighthouse 90+ on every screen with evidence; keyboard test done; checklist complete with fixes | Scores missing; keyboard test skipped |
| Usability test and improvement | 1 | 10 | Real user from or like the setting; notes for each task; most serious issue fixed with before and after | No real user, or no improvement made |
| GitHub workflow and report | 2 | 5 | Issue, branch, regular commits, merged PR with screenshots and tag; report complete in the repository and its link submitted | Single commit, unmerged PR, missing report, or a broken link |
| **Total** | | **100** | | |

**Proficient** work is complete with minor gaps. **Beginning** work is missing, not working, or not your own.

## Academic integrity

This is **individual work**. You may discuss ideas with classmates, but your personas, code, wireframes, test and report must be your own. Code copied from ClinicQ without changing it for your setting, or from a classmate, will be scored as Beginning. The code snippets in this activity are a starting point you are expected to adapt. Declare any AI tool or outside source you used in your report.

## Late submissions

Late work follows the late policy in the course syllabus.

## Checklist before you submit

- [x] My app shows my own system's name, services and fields, not ClinicQ's.
- [x] `docs/week3/personas.md` has my two personas, each with a real quote, scenario, top tasks and design rules.
- [ ] Six wireframes are in `docs/week3/wireframes/`, and `feedback.md` has my self-review of all three screens.
- [ ] Join, My place and Staff dashboard all work, on a phone width and a laptop width.
- [ ] The join form validates every field on the server and keeps the user's input on error.
- [ ] Staff actions use POST forms, and My place updates by itself within 10 seconds.
- [ ] `accessibility.md` has Lighthouse scores, keyboard notes and the checklist.
- [ ] `usability-test.md` has a real user's results and one improvement with before and after.
- [ ] My pull request is merged into `main` and tagged `week3`.
- [ ] `docs/week3/report.md` is in my repository with my PR link at the top, and I submitted its `week3` link on MOLE.
