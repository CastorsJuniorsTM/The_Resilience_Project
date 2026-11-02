# The Resilience Project — Community Management System

Database project, **Databases — Fall 2025** (EDHEC × UTC).

The Resilience Project aims to connect individuals and communities in a collaborative network of mutual assistance. This repository contains the data model (UML, logical model), the PostgreSQL schema and a Python application that works on top of it.

## Team

| Member | Contribution |
|---|---|
| **Thibaud Fievet** | Co-author |
| **Maxence Hervé** | Co-author, author of the whole Python interface |

## Table of contents

1. [Project guidelines](#project-guidelines)
2. [Final project process](#final-project-process)
3. [Project architecture](#project-architecture)
4. [Installation and launch](#installation-and-launch)
5. [Features and specialized views](#features-and-specialized-views)
6. [Testing](#testing)
7. [Known limitations](#known-limitations)
8. [Credits](#credits)

---

## Project guidelines

This section restates the two documents given by the course: the project description (`Project_description.pdf`) and the project directives (`project_directives.pdf`).

### Overview and business rules

- The system lets anyone freely add themselves to the database and create communities.
- Individuals can declare membership in communities and/or relationships with other individuals. Communities can also declare links to other communities.
- **Links are unidirectional and include a description** (e.g., Alice declares a link to Bob with the description "Bob is my neighbor").
- **Any member of a community can manage all the information of that community** and may act in the database on behalf of the community.
- **Exclusion:** members can oppose the presence of another person in the community. If more than half of the community's members vote against the presence of a person, that person is removed from the community.
- **Skills:** users declare a skill with a proficiency level from **1 to 5**, and can propose services based on these skills. The system manages a repository of skills; individuals and communities can add new skills.
- **Services** may be:
  - free of charge;
  - in exchange for another service (identified or to be negotiated);
  - commercial (paid in the [Ğ1 cryptocurrency](https://fr.wikipedia.org/wiki/%C4%9E1)).
- **Ğ1 accounts:** users and communities can hold Ğ1 accounts, and their **public keys are stored** in the database.
- **Messaging:** users and communities can exchange messages. A message is the full property of its sender, is addressed to one recipient, and may reference another message (conversation threads).
- **Geolocation:** individuals share their location through geographic coordinates (e.g., `49.41957, 2.82377`). The system must generate links to OpenStreetMap for visualization (e.g., `https://www.openstreetmap.org/#map=17/49.41957/2.82243`, where `17` is the zoom level), **with configurable zoom levels**.

### Required specialized views

The application must provide at least three specialized views:

| View | Requirement |
|---|---|
| **Community View** | Displays all communities a person claims to belong to, with a boolean flag indicating whether they are excluded. |
| **Message View** | Displays messages with references to original messages when they are part of a thread (e.g., if C → B → A, viewing C should show its link back to A). |
| **Proximity View** | Displays communities and individuals located within 1 km of each other. |

### Expected deliverables

1. **System architecture and UML model** — UML class diagrams covering individuals, communities, skills, services, messages and relationships (PlantUML format **and** a PNG image).
2. **Database design** — a relational SQL schema based on the UML model, implementing membership rules, skill declarations, service types and message threading.
3. **Functional application (Python)** — user and community management; adding skills, services and geolocation; sending and receiving messages; logic for exclusions and voting in communities.
4. **User interface** — a simple UI with the specialized views (Community, Message, Proximity), and search for people, communities, skills and services.
5. **Testing and documentation** — document the architecture, setup and test procedures; provide test data (sample users, communities, skills, services and messages).

The description also asks to submit the project on the GitLab of the institution, with a `README.md` containing the names of the team members and a description of the project, the UML model (PlantUML + PNG), the database schema (SQL), the Python application and the test data.

### Course directives and constraints

- The project is to be completed by a team of three members.
- Deliverables must be submitted on time: "better to submit incomplete but high-quality work than a larger quantity of substandard or late work".
- The code must run correctly, be readable, and include well-documented testing and execution conditions. Non-functional code is unacceptable.
- Documentation is written in French or English.
- Relational databases must use **PostgreSQL**, and the code must be compatible with the version installed on the UTC servers.
- The application must be implemented in **Python**.
- The `README.md` must contain the author names and the project architecture information. The submission also includes a detailed model with a clarification note, the UML diagram in PlantUML format with a PNG, the logical model in plain text, and the relevant code files (SQL, Python, etc.).
- The project is defended during the last class of the semester, **December 2nd, 2025**.
- Academic integrity: any proven case of plagiarism results in exclusion from the course and is reported to the disciplinary council.

Deadlines, as written in the directives:

| Deliverable | Deadline |
|---|---|
| Clarification note + first version of the conceptual data model (class diagram) | Week 3 tutorial session [October 10th, 2025] + 2 days before 23:59 |
| Corrected conceptual model + logical data model | Week 4 tutorial session [November 4th, 2025] + 2 days before 23:59 |
| SQL implementation | Week 5 tutorial session [November 18th, 2025] + 2 days before 23:59 |
| Python application | Week 6 tutorial session [November 25th, 2025] + 2 days before 23:59 |
| Project defense | Last class [December 2nd, 2025] |

### Assessment criteria

- **Correctness** — implementation of all specified rules, including membership exclusion, service types and message referencing.
- **Design** — clear and scalable UML model and database schema.
- **Code quality** — clean, maintainable Python code.
- **Documentation** — well-structured documentation and test coverage.
- **Functionality** — working specialized views and a user-friendly interface.

---

## Final project process

The file [`Processus finalproject.txt`](Processus%20finalproject.txt) describes the process followed for the project, from the UML to the Python application. In short:

- **Approach:** the team started from the description and the clarification notes to get an overall view of the model before writing the UML.
- **UML:** the business objects were listed first. `Individual` and `Community` share attributes and can both send messages, so they inherit from a superclass `Connectable_Entity` (id, name, Ğ1 public key). The three service types (free, exchange, commercial) inherit from `Service`. Association classes were created for the exclusion vote (`Opposition`), skills with proficiency level (`Master`), links between entities (`Link`) and membership with the creator status (`BelongTo`).
- **MLD:** classes are connected through foreign keys. Versions were simplified: the `Opposition`/`Vote_Opposition` split and the `Message`/`Message recipient`/`Message references` split were dropped, and the inheritance attributes were gathered into the parent classes (`Entity` and `Service`).
- **SQL:** written almost the same way as the MLD, with tables and constraints. PostgreSQL specifics are `TIMESTAMP` for DateTime, `CAST` for concatenation and `REFERENCES` for foreign keys. Constraints include valid latitude and longitude, an `@` in the email, no message to oneself, consistency between service type and its fields (`price` / `description_expectation`), and a single vote per voter against the same target in the same community.
- **Python:** three files. `main.py` has one function per action (parameterized queries, one transaction each, connection settings read from environment variables), `User_Interface.py` is a console menu with the specialized views and the search, and `gui.py` is a Tkinter window (see Known limitations). The rules of the project are enforced by the constraints of the schema, not repeated in Python.

---

## Project architecture

```
.
├── 1 - UML/
│   ├── PlantUML.txt                                    UML class diagram (PlantUML source)
│   ├── Capture_d_écran_2025-11-24_162723.png           UML diagram (PNG image)
│   ├── UML_v2.pdf, UML_V3.pdf                          Earlier and later versions of the diagram
│   └── Clarification_Note.txt                          Clarification note for the UML
├── 2 - MLD/
│   ├── MLD_v1.txt, MLD_V3.txt, MLD_V4.txt              Logical data model (plain text), V4 is the latest
│   ├── MLD_v2.pdf                                      MLD v2
│   ├── Clarifications_notes_MLD_MLD_v2_.txt            Clarification notes (written for MLD v2)
│   └── Questions_MLD+UML.txt                           Open questions raised during modelling
├── 3 - SQL Implementation/
│   └── SQL_V1.txt                                      First version of the SQL schema
├── 4 - Python interface/
│   ├── schema.sql                                      PostgreSQL schema (tables and views)
│   ├── main.py                                         Database access layer (psycopg2)
│   ├── User_Interface.py                               Console menu application (with the views and the search)
│   └── gui.py                                          Tkinter interface (see Known limitations)
├── Processus finalproject.txt                          Description of the project process
├── requirements.txt                                    Python dependency (psycopg2-binary)
├── .gitignore
└── README.md
```

### Data model

- **UML:** [PlantUML source](1%20-%20UML/PlantUML.txt) · [PNG image](1%20-%20UML/Capture_d_%C3%A9cran_2025-11-24_162723.png) · [clarification note](1%20-%20UML/Clarification_Note.txt).
- **Logical model:** [MLD_V4.txt](2%20-%20MLD/MLD_V4.txt).
- **SQL schema:** [schema.sql](4%20-%20Python%20interface/schema.sql).

Tables of the schema:

| Table | Role |
|---|---|
| `Connectable_Entity` | Parent of individuals and communities: id, name, Ğ1 public key |
| `Individual` | Person: email, optional geolocation |
| `Community` | Community (id only) |
| `BelongTo` | Membership of an individual in a community, with `isCreator` |
| `Link` | Unidirectional link between two entities, with a description |
| `Message` | Message with sender, receiver and optional referenced message (`idReference`) |
| `Skill`, `Master` | Skill repository (name is the key) and skills declared by individuals (level 1 to 5) |
| `Service`, `Service_Requirement` | Services (`type` 1 = free, 2 = exchange, 3 = commercial in Ğ1) and skills they require |
| `GeoLocation` | Coordinates, with a generated OpenStreetMap link `link_osm` |
| `Opposition` | Exclusion vote of a voter against a target in a community |

Views: `Community_View`, `Message_View`, `Proximity_View` (specialized views), `View_Individuals`, `View_Communities`, `Individual_all`, `Community_all`, `Free_Service`, `Commercial_Service`, `Exchange_Service`.

### Python application

- [`main.py`](4%20-%20Python%20interface/main.py) — connection to PostgreSQL and one function per action: `add_individual`, `add_community`, `join_community`, `create_link`, `update_geolocation`, `send_message`, `add_skill`, `declare_skill`, `propose_service`, `vote_opposition`, `check_community_status`.
- [`User_Interface.py`](4%20-%20Python%20interface/User_Interface.py) — console menu using these functions, the specialized views and the search.
- [`gui.py`](4%20-%20Python%20interface/gui.py) — Tkinter window (tabs: creation, actions, services/skills, mailbox, database browsing).

---

## Installation and launch

### Prerequisites

- **PostgreSQL 12 or later** — the schema uses a `GENERATED ALWAYS AS (...) STORED` column (`GeoLocation.link_osm`). The version installed on the UTC servers must be checked by the team.
- **Python 3** with the package listed in [`requirements.txt`](requirements.txt) (`psycopg2-binary`).
- Tkinter (bundled with most Python distributions) is only needed for `gui.py`.

### 1. Create the database

Create an empty PostgreSQL database, then load the schema:

```bash
psql -h <host> -U <user> -d <database> -f "4 - Python interface/schema.sql"
```

The file starts by dropping the existing tables (and the views that depend on them), so it can be reloaded on a database that already contains the schema.

### 2. Install the dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the connection

[`main.py`](4%20-%20Python%20interface/main.py) reads the connection settings from environment variables, so no password is stored in the code:

| Variable | Default |
|---|---|
| `RESILIENCE_DB_HOST` | `localhost` |
| `RESILIENCE_DB_NAME` | `dbedXXXXXX` |
| `RESILIENCE_DB_USER` | `edXXXXXX` |
| `RESILIENCE_DB_PASSWORD` | `password` |

```bash
# bash
export RESILIENCE_DB_HOST=<host> RESILIENCE_DB_NAME=<database> RESILIENCE_DB_USER=<user> RESILIENCE_DB_PASSWORD=<password>
```

```powershell
# PowerShell
$env:RESILIENCE_DB_HOST = "<host>"; $env:RESILIENCE_DB_NAME = "<database>"
$env:RESILIENCE_DB_USER = "<user>"; $env:RESILIENCE_DB_PASSWORD = "<password>"
```

### 4. Launch the application

```bash
cd "4 - Python interface"
python User_Interface.py
```

This opens the console menu (options 1 to 12, `0` to quit).

---

## Features and specialized views

Menu of `User_Interface.py`:

| Option | Feature |
|---|---|
| 1 | Add an individual (name, email) or a community (name) |
| 2 | Join a community, or create a unidirectional link with a description |
| 3 | Send a message, optionally as a reply to an existing message (id) |
| 4 | Register geographic coordinates for an individual |
| 5 | Declare a skill with a level from 1 to 5 (the skill is added to the repository if needed), or propose a service (1 = free, 2 = exchange, 3 = commercial in Ğ1) |
| 6 | Vote against the presence of a person in a community, with a reason |
| 7 | **Community View**: communities of a person, each marked `ACTIVE` or `EXCLUDED` |
| 8 | **Message View**: messages sent or received by an entity, each with the beginning of the message it replies to |
| 9 | **Proximity View**: pairs of individuals located within 1 km, with their distance |
| 10 / 11 | List all individuals / all communities |
| 12 | **Search** by keyword in the names of individuals and communities and in the titles of services |

How the rules are implemented in the schema:

- **Exclusion:** `Community_View.is_excluded` is true when the number of votes against a member (`Opposition`) is strictly greater than half of the members of the community. The member's row in `BelongTo` is not deleted; the view flags them.
- **Service types:** the `chk_service_logic` constraint accepts free services without price nor expectation, exchange services with a description of the expectation, and commercial services with a price.
- **Threads:** `Message.idReference` points to the message being answered; `Message_View` returns the parent message of each message.
- **Proximity:** `Proximity_View` computes the distance in kilometres from the latitudes and longitudes of two individuals and keeps pairs at 1 km or less.
- **OpenStreetMap:** each `GeoLocation` row stores a link `https://www.openstreetmap.org/#map=17/<latitude>/<longitude>` (zoom fixed at 17).

---

## Testing

Test data for the sample users, communities, skills, services and messages is not part of the repository yet. Until it is added, the key rules can be checked by hand from the console menu, on an empty database loaded with the schema. Ids are assigned by the database (starting at 1, shared by individuals and communities).

1. **Exclusion by vote** — create three individuals and a community (options 1), make the three individuals join it (option 2). One vote against the same person (option 6): option 7 shows `ACTIVE`. A second vote by another member: option 7 shows `EXCLUDED` (2 votes out of 3 members is more than half). A second vote by the same voter against the same target is rejected (unique constraint).
2. **Service types** — propose a free, an exchange and a commercial service (option 5): each is accepted. Search (option 12) shows the service. Skills with a level outside 1 to 5 are rejected.
3. **Message threads** — send a message A, then B as a reply to A, then C as a reply to B (option 3, "Reply ID"). Option 8 shows the beginning of the message that each one replies to. A message from an entity to itself is rejected.
4. **Proximity** — register the coordinates `49.41957, 2.82377` for one individual and `49.41957, 2.82243` for another (option 4, values taken from the project description), and coordinates far away for a third one. Option 9 lists only the close pair. Avoid giving two individuals strictly identical coordinates (see below).
5. **Links** — create a link with a description (option 2); linking an entity to itself is rejected.

The outcome of each rule is enforced by PostgreSQL constraints, so a rejected operation prints an `Error while ...` message from the database.

---

## Known limitations

This list reflects the state of the code at the time of writing.

- `gui.py` is not synchronized with `main.py`: several calls use arguments that the functions of `main.py` no longer take (for example `add_individual`, `update_geolocation`, `vote_opposition`, `propose_service`, `send_message`). The console application `User_Interface.py` is the functional interface.
- The OpenStreetMap zoom is fixed at 17, whereas the description asks for configurable zoom levels.
- The Message View shows the direct parent of a message, not the whole chain (C → B → A).
- The Proximity View only covers individuals (communities have no location in the schema).
- The search covers individuals, communities and service titles, not skills.
- Only individuals can declare skills.
- Two individuals with strictly identical coordinates may make the distance formula of `Proximity_View` fail.
- No test data yet.

---

## Credits

- **Python interface** (`main.py`, `User_Interface.py`, `gui.py`): **Maxence Hervé**.
- **UML, logical model, SQL schema and documentation**: team work by the authors, as described in [`Processus finalproject.txt`](Processus%20finalproject.txt).
