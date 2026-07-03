# Architectural Decisions

## ADR-001

Decision:
Store money as integer paise.

Reason:
Avoid floating-point precision errors.

---

## ADR-002

Decision:
Use sqlite3 instead of SQLAlchemy.

Reason:
Gain experience writing SQL and designing schemas directly.

---

## ADR-003

Decision:
Categories are predefined.

Reason:
Simplifies the data model and removes category CRUD from the MVP.

---

## ADR-004

Decision:
"Others" is a normal category stored in the database.

Reason:
Avoid special-case application logic.

---

## ADR-005

Decision:
Budget periods are calendar months.

Reason:
Simpler reporting and aligns with user expectations.