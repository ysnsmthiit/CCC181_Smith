# angOrderQ Requirements

**Setting:** Local food stalls, kiosks, and pop-up food vendors
**People who wait:** Customers seeking quick meals after work or class without inhaling grill smoke or crowding around busy fryers (see [Marco in docs/week3/personas.md](week3/personas.md#marco-the-person-waiting-customer)).  
**People who serve:** Stall operators and cooks working fast-paced turnover with greasy hands in noisy kitchen environments (see [Ate Gina in docs/week3/personas.md](week3/personas.md#ate-gina-the-staff-member-stall-operator)).  

**Problem statement:** A customer visiting a busy local food stall needs a reliable way to track their order status remotely from their phone, because standing in dense crowds beside smoky fryers is uncomfortable and leads to missed shouted order numbers.

---

## Functional Requirements

| ID | Requirement | Priority | Stores data? | Status |
| --- | --- | --- | --- | --- |
| FR-01 | A customer can join the queue by selecting a food service category and entering their name, optional email, and order type. | Must | **Yes** | Built (Week 3) |
| FR-02 | A customer can view their ticket number, live status, and count of orders ahead of them. | Must | **Yes** | Built (Week 3) |
| FR-03 | A customer can cancel their order and leave the queue before being called. | Must | **Yes** | Built (Week 3) |
| FR-04 | A customer can see a live two-column claim board (*Preparing* vs *Now Serving*) with their ticket highlighted. | Should | **Yes** | Built (Week 3) |
| FR-05 | A stall operator can view active tickets grouped or filtered by food category (*Meals & Combos*, *Drinks*, *Snacks*). | Must | **Yes** | Built (Week 3) |
| FR-06 | A stall operator can call the next waiting order, transitioning its status to `called` with a recorded timestamp. | Must | **Yes** | Built (Week 3) |
| FR-07 | A stall operator can mark a called ticket as `served` or flag it as `no-show` with a recorded timestamp. | Must | **Yes** | Built (Week 3) |
| FR-08 ★ | A customer can specify an `Order Type` (*Dine-in* vs *Take-out*) so kitchen staff package the food appropriately. | Must | **Yes** | Built (Week 3) |
| FR-09 ★ | A stall operator can view live count pills showing active waiting orders per food category. | Should | **Yes** | Built (Week 3) |
| FR-10 ★ | A customer's contact profile (name and email) is preserved in a user/customer record, linking multiple ticket orders to the same customer. | Must | **Yes** | This week |
| FR-11 ★ | A stall operator can re-call a ticket with an audio/visual pulse if the customer did not hear their number in noisy stall conditions. | Could | **Yes** | Later |
| FR-12 | A stall operator can add, rename, or toggle availability of a food service category. | Could | **Yes** | Later |

---

## Non-Functional Requirements

| ID | Requirement | Category | Priority |
| --- | --- | --- | --- |
| NFR-01 | No ticket is lost when the Flask app or PostgreSQL database container restarts. | Reliability | Must |
| NFR-02 | Two customers can never be assigned the same ticket number for a given service day, even under concurrent submissions. | Data integrity | Must |
| NFR-03 | The My Place ticket screen loads in under 2 seconds on a 4G mobile connection. | Performance | Should |
| NFR-04 | Every application screen scores 90 or higher in Google Lighthouse accessibility audits. | Accessibility | Must |
| NFR-05 | No database passwords, secret keys, or environment files are tracked in the Git repository. | Security | Must |

---

## MVP & Out of Scope

### MVP Definition
The Minimum Viable Product consists of requirements **FR-01, FR-02, FR-03, FR-05, FR-06, FR-07, FR-08, FR-10**, and **NFR-01, NFR-02, NFR-04, NFR-05**.  
*Rationale:* This represents the smallest functional slice that replaces noisy shouting and paper order slips with a reliable digital queue: customers can order and step away, staff can track and call orders, customer records are preserved, and data safely persists across server restarts.

### Out of Scope (This Semester)
1. **In-app Digital Payments (GCash/Maya/Cards):** angOrderQ focuses strictly on order queuing and pickup flow; customers pay cash or scan vendor QR stands directly at the stall.
2. **Multi-vendor Tenant SaaS Authentication:** The app is configured for a dedicated single food stall rather than a multi-vendor platform with tenant billing.

---

## Requirements Feedback (Real Person Check)

| Who (role only) | What they said | What I changed |
| --- | --- | --- |
| Frequent food stall customer (student diner) | "I eat at the same food stalls regularly after evening classes. It would be convenient if entering my email recognized me instead of treating me like a brand new visitor every single time, so all my receipts stay connected." | Added FR-10 (Customer profile entity linked to ticket orders). |
