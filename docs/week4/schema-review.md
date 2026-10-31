# angOrderQ Schema Self-Review

Review conducted against `docs/requirements.md` and the 6 self-review criteria outlined in Week 4:

---

### Entry 1: Data Integrity & Role Normalization
* **Criterion:** Coverage & Normalization (Questions 1 & 2)
* **Works well:** Separating customer identity into `users` and food categories into `services` ensures that customer details (`name`, `email`) and food types are never duplicated across tickets. A customer can visit the stall repeatedly, and each order links cleanly via foreign key.
* **Problem:** Initially, there was a risk that staff accounts and customer accounts might require disparate tables, which would complicate the MVP login/dashboard flow later.
* **Change:** Added a `role` column on `users` with a strict `CHECK (role IN ('customer', 'staff'))` constraint. This accommodates future staff authentication without requiring an extra table, while keeping `users` focused on single-stall operational access.

---

### Entry 2: Guarding Against Bad Input & Impossible States
* **Criterion:** Bad Data & Constraints (Question 4)
* **Works well:** The `CHECK` constraints on `order_type IN ('Dine-in', 'Take-out')` and `status IN ('waiting', 'called', 'served', 'no-show', 'cancelled')` completely prevent invalid lifecycle states from entering the database, even if a buggy client request bypasses the front-end form.
* **Problem:** If a stall operator configures an average preparation time of 0 or a negative number for a menu category, wait time calculations would produce nonsensical estimates.
* **Change:** Enforced `CHECK (avg_minutes > 0)` on `services.avg_minutes`. If invalid data is submitted, PostgreSQL immediately rejects the transaction at the database engine level.

---

### Entry 3: Historical Data Preservation on Deletion
* **Criterion:** Foreign Key Delete Rules (Question 5)
* **Works well:** Setting `ondelete="RESTRICT"` on both `tickets.user_id` and `tickets.service_id` prevents cascade deletion of past order history.
* **Problem:** If a stall operator removes an old seasonal food category (e.g. *Special Holiday Cooler*), using `CASCADE` would unintentionally delete all past customer tickets that ordered that category, corrupting historical stall sales and turnaround metrics.
* **Change:** Explicitly confirmed `ON DELETE RESTRICT` for both foreign keys in `schema.md` and SQLAlchemy models. Deleting a referenced category or user with active/past orders is blocked by the database engine; staff can deactivate categories without deleting rows.

---

### Entry 4: Timezone Safety for Outdoor Stall Operations
* **Criterion:** Data Types & Timestamps (Question 6)
* **Works well:** All temporal columns (`created_at`, `called_at`, `served_at`) use PostgreSQL's `timestamptz` (timestamp with time zone) rather than plain naive timestamps.
* **Problem:** Storing timestamps as naive strings or naive dates causes discrepancies between the local tablet time zone (e.g., Asia/Manila, UTC+8) and the Docker container's UTC system clock.
* **Change:** Enforced `DateTime(timezone=True)` with server-side `func.now()` default in SQLAlchemy, guaranteeing reliable queue sorting and turnaround calculations regardless of client clock differences.

