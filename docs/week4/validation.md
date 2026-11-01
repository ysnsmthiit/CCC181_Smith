# Validation in Three Layers: angOrderQ

## Validation Architecture

1. **Browser Layer (Client):** HTML attributes (`required`, `type="email"`, `maxlength`) provide instant visual feedback to users directly within the browser interface.
2. **Flask Layer (Application Server):** Server-side route validation sanitizes input (`strip()`, length limits, whitelist checking) and issues `400 Bad Request` if rules are violated.
3. **Database Layer (PostgreSQL Engine):** Schema constraints (`PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`, `CHECK`, `RESTRICT`) guarantee data integrity even if client and server validations are bypassed.

---

## Validation Test Results

| Rule | Layer | Constraint Type | How I Tested It | Result / Exact Database Output |
| --- | --- | --- | --- | --- |
| Name length limit | Browser | `maxlength="80"` | Inspected `<input id="name">` | Browser prevents typing beyond 80 characters |
| Email format | Browser | `type="email"` | Typed `not-an-email` in form | Browser warning: "Please include an '@' in the email address" |
| Empty name rejection | Flask | Python condition | `curl.exe` with `name=""` | `HTTP/1.1 400 BAD REQUEST`, row not saved |
| Invalid email rejection | Flask | Python condition | `curl.exe` with `email="not-an-email"` | `HTTP/1.1 400 BAD REQUEST`, row not saved |
| Name over 80 chars | Flask | Python length check | `curl.exe` with 95-char name | `HTTP/1.1 400 BAD REQUEST`, row not saved |
| Invalid order type | Flask | Python whitelist | `curl.exe` with `order_type="Delivery"` | `HTTP/1.1 400 BAD REQUEST`, row not saved |
| Inactive category rejection | Flask | Python active check | `curl.exe` referencing disabled service | `HTTP/1.1 400 BAD REQUEST`, row not saved |
| Service must exist | Database | FOREIGN KEY | `INSERT INTO tickets (number, user_id, service_id, order_type) VALUES (999, 1, 999, 'Dine-in');` | `ERROR: insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` |
| Valid queue status | Database | CHECK | `UPDATE tickets SET status = 'lost' WHERE id = 1;` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| Unique customer email | Database | UNIQUE | `INSERT INTO users (name, email) VALUES ('Duplicate', 'marco@gmail.com');` | `ERROR: duplicate key value violates unique constraint "users_email_key"` |
| Prep time > 0 | Database | CHECK | `INSERT INTO services (name, avg_minutes) VALUES ('Zero Time', 0);` | `ERROR: new row for relation "services" violates check constraint "ck_services_avg_minutes"` |
| Mandatory fields | Database | NOT NULL | `INSERT INTO tickets (number, user_id) VALUES (999, 1);` | `ERROR: null value in column "service_id" of relation "tickets" violates not-null constraint` |
| Cascade protection | Database | ON DELETE RESTRICT | `DELETE FROM services WHERE id = 1;` | `ERROR: update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets"` |
| Valid insert & defaults | Database | Server defaults | `INSERT INTO tickets (number, user_id, service_id, order_type) VALUES (999, 1, 1, 'Take-out') RETURNING id, number, status, created_at;` | Returned auto-generated `id = 6`, `status = 'waiting'`, and UTC `created_at` timestamp |

---

## SQL Injection Audit

Audit performed using:
```bash
git grep -nE "f[\"'].*(SELECT|INSERT|UPDATE|DELETE)" -- "*.py"
```

**Result:** Zero matches found. All database operations strictly utilize SQLAlchemy 2.0 type-safe expressions and parameterized statements.

