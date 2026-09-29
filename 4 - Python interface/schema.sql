CREATE TABLE Connectable_Entity (
    idEntity        SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    public_key_G1   VARCHAR(128)
);

CREATE TABLE GeoLocation (
    idGeolocation   SERIAL PRIMARY KEY,
    statement_date  TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    latitude        DECIMAL(10,6) NOT NULL,
    longitude       DECIMAL(10,6) NOT NULL,
    link_osm        TEXT GENERATED ALWAYS AS (
        'https://www.openstreetmap.org/#map=17/' || CAST(latitude AS TEXT) || '/' || CAST(longitude AS TEXT)
    ) STORED,

    CONSTRAINT check_latitude CHECK (latitude BETWEEN -90 AND 90),
    CONSTRAINT check_longitude CHECK (longitude BETWEEN -180 AND 180)
);


CREATE TABLE Individual (
    idIndividual    INTEGER PRIMARY KEY REFERENCES Connectable_Entity(idEntity),
    email           VARCHAR(255) NOT NULL UNIQUE,
    idGeolocation   INTEGER REFERENCES GeoLocation(idGeolocation),

    CONSTRAINT check_email_format CHECK (email LIKE '%@%')
);

CREATE TABLE Community (
    idCommunity     INTEGER PRIMARY KEY REFERENCES Connectable_Entity(idEntity)
);

CREATE TABLE BelongTo (
    idIndividual    INTEGER REFERENCES Individual(IdIndividual),
    idCommunity     INTEGER REFERENCES Community(IdCommunity),
    isCreator       BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (idIndividual, idCommunity)
);


CREATE TABLE Link (
    idSource        INTEGER REFERENCES Connectable_Entity(idEntity),
    idTarget        INTEGER REFERENCES Connectable_Entity(idEntity),
    description     TEXT,
    PRIMARY KEY (idSource, idTarget),

    CONSTRAINT check_no_self_link CHECK (idSource <> idTarget)
);


CREATE TABLE Message (
    idMessage   SERIAL PRIMARY KEY,
    content     TEXT NOT NULL,
    send_date   TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    idSender    INTEGER NOT NULL REFERENCES Connectable_Entity(idEntity),
    idReceiver  INTEGER NOT NULL REFERENCES Connectable_Entity(idEntity),
    idReference INTEGER REFERENCES Message(idMessage),

    CONSTRAINT check_sender_receiver_diff CHECK (idSender <> idReceiver)
);

CREATE TABLE Skill (
    name VARCHAR(100) PRIMARY KEY
);

CREATE TABLE Master (
    idIndividual     INTEGER REFERENCES Individual(idIndividual),
    idSkill          VARCHAR(100) REFERENCES Skill(name),
    proficiency_level INTEGER NOT NULL,

    PRIMARY KEY (idIndividual, idSkill),

    CONSTRAINT check_proficiency CHECK (proficiency_level BETWEEN 1 AND 5)
);

CREATE TABLE Service (
    idService               SERIAL PRIMARY KEY,
    title                   VARCHAR(100) NOT NULL,
    description_service     TEXT NOT NULL,
    idProvider              INTEGER NOT NULL REFERENCES Individual(idIndividual),
    description_expectation TEXT,
    price                   FLOAT,
    type                    INTEGER NOT NULL,

    CONSTRAINT check_service_type CHECK (type IN (1, 2, 3)),
    CONSTRAINT chk_service_logic CHECK ((type = 1 AND price IS NULL AND description_expectation IS NULL)
    OR (type = 2 AND price IS NULL AND description_expectation IS NOT NULL)
    OR (type = 3 AND price IS NOT NULL AND description_expectation IS NULL))
);

CREATE TABLE Service_Requirement (
    idService   INTEGER REFERENCES Service(idService),
    idSkill     VARCHAR(100) REFERENCES Skill(name),
    PRIMARY KEY (idService, idSkill)
);

CREATE TABLE Opposition (
    idOpposition SERIAL PRIMARY KEY,
    vote_date    TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    reason       VARCHAR(100),
    idTarget     INTEGER NOT NULL REFERENCES Individual(idIndividual),
    idVoter      INTEGER NOT NULL REFERENCES Individual(idIndividual),
    idCommunity  INTEGER NOT NULL REFERENCES Community(idCommunity),

    CONSTRAINT unique_vote_per_user UNIQUE (idTarget, idVoter, idCommunity),
    CONSTRAINT check_voter_target_diff CHECK (idTarget <> idVoter)
);


CREATE OR REPLACE VIEW Individual_all AS
SELECT i.idIndividual,e.name, e.public_key_G1, i.email, i.idGeolocation
FROM Individual i
JOIN Connectable_Entity e ON e.idEntity = i.idIndividual;

CREATE OR REPLACE VIEW Community_all AS
SELECT c.idCommunity,e.name, e.public_key_G1
FROM Community c
JOIN Connectable_Entity e ON e.idEntity = c.idCommunity;

CREATE OR REPLACE VIEW Free_Service AS
SELECT idService, title, description_service, idProvider
FROM Service;

CREATE OR REPLACE VIEW Commercial_Service AS
SELECT idService, title, description_service, idProvider, price
FROM Service;

CREATE OR REPLACE VIEW Exchange_Service AS
SELECT idService, title, description_service, idProvider, description_expectation
FROM Service;

CREATE OR REPLACE VIEW Community_View AS
SELECT 
    bt.idIndividual,
    ind_ent.name AS individual_name,
    bt.idCommunity,
    com_ent.name AS community_name,
    bt.isCreator,
    
    CASE 
        WHEN (

            SELECT COUNT(*) 
            FROM Opposition o 
            WHERE o.idTarget = bt.idIndividual 
            AND o.idCommunity = bt.idCommunity
        ) > (

            (SELECT COUNT(*) FROM BelongTo members WHERE members.idCommunity = bt.idCommunity) / 2
        ) 
        THEN TRUE 
        ELSE FALSE 
    END AS is_excluded
FROM BelongTo bt
JOIN Connectable_Entity ind_ent ON ind_ent.idEntity = bt.idIndividual
JOIN Connectable_Entity com_ent ON com_ent.idEntity = bt.idCommunity;


CREATE OR REPLACE VIEW Message_View AS
SELECT 
    m.idMessage,
    m.content,
    m.send_date,
    sender.name AS sender_name,
    receiver.name AS receiver_name,

    m.idReference AS parent_message_id,
    parent.content AS parent_message_preview,
    parent_sender.name AS parent_sender_name
FROM Message m
JOIN Connectable_Entity sender ON m.idSender = sender.idEntity
JOIN Connectable_Entity receiver ON m.idReceiver = receiver.idEntity

LEFT JOIN Message parent ON m.idReference = parent.idMessage
LEFT JOIN Connectable_Entity parent_sender ON parent.idSender = parent_sender.idEntity;



CREATE OR REPLACE VIEW Proximity_View AS
SELECT 
    i1.idIndividual AS id_person_A,
    ent1.name AS name_person_A,
    i2.idIndividual AS id_person_B,
    ent2.name AS name_person_B,
    (
        6371 * ACOS(
            COS(RADIANS(geo1.latitude)) * COS(RADIANS(geo2.latitude)) *
            COS(RADIANS(geo2.longitude) - RADIANS(geo1.longitude)) +
            SIN(RADIANS(geo1.latitude)) * SIN(RADIANS(geo2.latitude))
        )
    ) AS distance_km
FROM Individual i1
JOIN GeoLocation geo1 ON i1.idGeolocation = geo1.idGeolocation
JOIN Connectable_Entity ent1 ON i1.idIndividual = ent1.idEntity

JOIN Individual i2 ON i1.idIndividual < i2.idIndividual -- Avoid duplicates (A–B and B–A) and self-comparison
JOIN GeoLocation geo2 ON i2.idGeolocation = geo2.idGeolocation
JOIN Connectable_Entity ent2 ON i2.idIndividual = ent2.idEntity

WHERE (
    6371 * ACOS(
        COS(RADIANS(geo1.latitude)) * COS(RADIANS(geo2.latitude)) *
        COS(RADIANS(geo2.longitude) - RADIANS(geo1.longitude)) +
        SIN(RADIANS(geo1.latitude)) * SIN(RADIANS(geo2.latitude))
    )
) <= 1.0;

CREATE OR REPLACE VIEW View_Individuals AS
SELECT 
    e.idEntity AS id,
    e.name,
    e.public_key_G1,
    i.email,
    g.latitude,
    g.longitude
FROM Individual i
JOIN Connectable_Entity e ON i.idIndividual = e.idEntity
LEFT JOIN GeoLocation g ON i.idGeolocation = g.idGeolocation;

CREATE OR REPLACE VIEW View_Communities AS
SELECT 
    e.idEntity AS id,
    e.name,
    e.public_key_G1
FROM Community c
JOIN Connectable_Entity e ON c.idCommunity = e.idEntity;

DROP TABLE IF EXISTS 
    Opposition,
    Service_Requirement,
    Service,
    Master,
    Skill,
    Message,
    Link,
    BelongTo,
    Community,
    Individual,
    GeoLocation,
    Connectable_Entity
CASCADE;

