# Wireframe & Persona Self-Review (angOrderQ)

---

## 1. Join Screen (`join.html` / `FR-01`)

### Primary Persona: Marco (Customer waiting at night market)

| Works well | Problem | Change |
| --- | --- | --- |
| Single-column stacked form (`join-phone.jpg`) makes inputting details simple with one hand in a crowded market. | The email field could cause friction for hungry customers wanting a 10-second ticket. | Labeled as `(optional for receipt)` in the wireframe and made optional in server validation. |
| Clear radio buttons for `Dine-in` vs `Take-out` provide large touch targets for quick selection. | Adding optional fields like `Special Notes / Allergies` increases form length on narrow mobile viewports. | Simplified for MVP by prioritizing core selections (`Category`, `Name`, `Order Type`). |

---

## 2. My Place Screen (`ticket.html` / `FR-02`, `FR-03`)

### Primary Persona: Marco (Customer waiting at night market)

| Works well | Problem | Change |
| --- | --- | --- |
| Prominently displays the personal ticket card (`#102`) alongside the Jollibee-inspited Claim Monitor (`Preparing` vs `Now Serving`). | Looking only at the Claim Monitor list below might leave users uncertain about their exact status without scrolling. | Added a high-contrast state badge (`Preparing` / `Ready`) directly inside Marco's primary ticket card above the board. |
| Large, clear `X Cancel Order` button gives users instant control to leave the queue (`FR-03`). | Small text details on mobile screens (`ticket-phone.jpg`) could look cluttered under dim night lighting. | Formatted the main ticket number in extra-large bold font to remain readable from an arm's length. |

---

## 3. Staff Dashboard (`staff.html` / `FR-04`, `FR-05`, `FR-06`)

### Primary Persona: Ate Gina (Stall Operator with greasy hands)

| Works well | Problem | Change |
| --- | --- | --- |
| The oversized `Call next order` button at the top allows Ate Gina to call orders with a single tap without searching the list. | The initial sketch (`staff-laptop.jpg`) is too wordy—mixing order metrics, multi-tag filters (`Dessert`, `Dine-in`), and secondary buttons (`Re-call`, `Cancelled`) creates visual clutter. | Streamlined the filter bar to strictly match the 3 core menu categories (`Meals & Combos`, `Drinks & Beverages`, `Snacks & Sides`) and reduced card buttons to primary actions (`Call`, `Serve`). |
| Card-based active queue items (`#103 Called`, `#102 Waiting`) separate ticket status clearly. | Greasy hands make tapping small text buttons difficult during peak dinner rush. | Formatted primary action triggers (`Call` and `Serve`) into solid, high-contrast buttons with a minimum target height of 48px. |