# The Resilience Project - Community Management System

Academic project carried out as part of the **Databases** course (Fall 2025) taught by **Insaf Setitra** at **UTC** (Université de Technologie de Compiègne).

The Resilience Project aims to connect individuals and communities in a collaborative network of mutual assistance. This repository contains the data model (UML, logical model), the PostgreSQL schema and a Python application that works on top of it. 

## Team

| Member | Contribution |
|---|---|
| **Thibaud Fievet** | Co-author |
| **Maxence Hervé** | Co-author |

## Table of contents

1. [Project guidelines](#project-guidelines)
2. [Final project process](#final-project-process)
3. [Project architecture](#project-architecture)
4. [Features and specialized views](#features-and-specialized-views)
5. [Testing](#testing)
6. [Known limitations](#known-limitations)
7. [Credits](#credits)

---

## Project guidelines

Key business rules and required specialized views:

- **Entities & Links**: Individuals and communities inherit from `Connectable_Entity` (with [Ğ1 cryptocurrency](https://fr.wikipedia.org/wiki/%C4%9E1) public keys). Links are unidirectional with a description.
- **Governance & Exclusion**: Any member can manage community data. A member is excluded if > 50% of community members vote against them.
- **Skills & Services**: Skills are rated 1 to 5. Services can be **Free**, **Exchange** (barter description), or **Commercial** (priced in Ğ1).
- **Messaging**: Unidirectional, sender-owned, with support for conversation threads (`idReference`).
- **Specialized Views**:
  - **Community View**: Lists communities of a person with an `is_excluded` flag.
  - **Message View**: Displays messages along with referenced parent messages.
  - **Proximity View**: Finds individuals located within 1 km (using coordinates and OpenStreetMap links).

---

## Final project process

As documented in [`Processus finalproject.txt`](Processus%20finalproject.txt), the design evolved incrementally:
- **UML to MLD**: Unified individual and community under `Connectable_Entity`, simplified association classes, and mapped inheritance into relational tables.
- **SQL Implementation**: Enforced business rules directly via PostgreSQL constraints (valid coordinates, email format, no self-messaging, service pricing logic, unique vote per voter).
- **Python Layer**: Focused on clean execution and interface separation; business validation is handled natively by the database schema.

---

## Project architecture

### Deliverables & Files
- **UML & Design**: [PlantUML](1%20-%20UML/PlantUML.txt) · [Diagram PNG](1%20-%20UML/Capture_d_%C3%A9cran_2025-11-24_162723.png) · [Clarification Note](1%20-%20UML/Clarification_Note.txt) · [MLD](2%20-%20MLD/MLD_V4.txt)
- **Database**: [schema.sql](4%20-%20Python%20interface/schema.sql) (PostgreSQL schema, constraints, and views)
- **Application**:
  - [`main.py`](4%20-%20Python%20interface/main.py) — Database connection and parameterized CRUD transactions.
  - [`User_Interface.py`](4%20-%20Python%20interface/User_Interface.py) — Interactive console CLI interface.
  - [`gui.py`](4%20-%20Python%20interface/gui.py) — Tkinter graphical interface prototype.

### Core Database Tables
- `Connectable_Entity`, `Individual`, `Community`: Entity hierarchy and contact info.
- `BelongTo`, `Opposition`: Community membership and exclusion voting.
- `Link`, `Message`: Unidirectional relationships and threaded messages.
- `Skill`, `Master`, `Service`, `Service_Requirement`: Skill repository and service listings.
- `GeoLocation`: Coordinates and generated OpenStreetMap URLs.

---

## Features and specialized views

The CLI (`User_Interface.py`) provides 12 options to interact with the system:
- **Entities & Network**: Create individuals/communities (1), join communities or establish links (2), update coordinates (4).
- **Services & Skills**: Declare skills (level 1–5) and propose services (free, exchange, commercial) (5).
- **Messaging**: Send messages and thread replies (3).
- **Governance**: Vote to oppose/exclude a community member (6).
- **Specialized & Search Views**:
  - Option 7: **Community View** (membership status: `ACTIVE` or `EXCLUDED`).
  - Option 8: **Message View** (threads with parent message references).
  - Option 9: **Proximity View** (pairs within 1 km computed via coordinates).
  - Options 10–12: Browse all entities and keyword search across names and service titles.

---

## Testing

Manual validation scenarios using `User_Interface.py` on an empty database loaded with the schema:
1. **Exclusion**: Create 3 members in a community. 1 opposition vote leaves the target `ACTIVE`; a 2nd vote (> 50%) flags them as `EXCLUDED`. Duplicate votes are rejected.
2. **Services & Skills**: Propose free, exchange, and commercial services. Levels outside 1–5 or invalid pricing combinations are rejected.
3. **Threading & Self-messaging**: Send message A, reply B to A, and C to B. Message View displays parent references. Self-messaging is blocked.
4. **Proximity**: Insert close coordinates (`49.41957, 2.82377` and `49.41957, 2.82243`) and distant ones; verify only the pair within 1 km is returned.
5. **Integrity**: Schema constraints automatically reject invalid emails, self-links, and unauthorized duplicate records.

---

## Known limitations

- `gui.py` is a prototype out of sync with `main.py`; use `User_Interface.py` as the primary interface.
- OpenStreetMap zoom level is fixed at 17 (the specification requested configurable zoom).
- Message View displays direct parent references rather than recursive full-thread chains.
- Proximity View only includes individuals (communities lack coordinate fields).
- Search queries individuals, communities, and services, but excludes skill tags.
- Identical coordinates between two individuals may cause proximity calculation edge cases.
- Sample dataset scripts are not yet packaged.

---

## Credits

- **Python interface** (`main.py`, `User_Interface.py`, `gui.py`): **Maxence Hervé**.
- **UML, logical model, SQL schema and documentation**: team work by both of us, as described in [`Processus finalproject.txt`](Processus%20finalproject.txt).