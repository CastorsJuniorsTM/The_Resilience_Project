import os
import psycopg2

# Connection settings, read from the environment so that no credential is stored in the code.
# Set RESILIENCE_DB_HOST, RESILIENCE_DB_NAME, RESILIENCE_DB_USER and RESILIENCE_DB_PASSWORD.
HOST = os.environ.get("RESILIENCE_DB_HOST", "localhost")
DATABASE = os.environ.get("RESILIENCE_DB_NAME", "dbedXXXXXX")
USER = os.environ.get("RESILIENCE_DB_USER", "edXXXXXX")
PASSWORD = os.environ.get("RESILIENCE_DB_PASSWORD", "password")

def get_connection():
    try:
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
        return conn
    except Exception as e:
        print("Error :", e)
        return None

def add_individual(name, email, public_key=None):
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        
        sql_entity = "INSERT INTO Connectable_Entity (name, public_key_G1) VALUES (%s, %s) RETURNING idEntity;"
        cur.execute(sql_entity, (name, public_key))

        generated_id = cur.fetchone()[0]

        sql_individual = "INSERT INTO Individual (idIndividual, email) VALUES (%s, %s)"
        cur.execute(sql_individual, (generated_id, email))

        conn.commit()
        print(f"Success : The individual '{name}' has been added with ID {generated_id}.")

    except psycopg2.Error as e:
        conn.rollback()
        print("Error while adding an individual :", e)
    
    finally:
        conn.close()

def add_community(name, public_key=None):
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
   
        sql_entity = "INSERT INTO Connectable_Entity (name, public_key_G1) VALUES (%s, %s) RETURNING idEntity"
        cur.execute(sql_entity, (name, public_key))
        
        generated_id = cur.fetchone()[0]

        sql_community = "INSERT INTO Community (idCommunity) VALUES (%s)"
        cur.execute(sql_community, (generated_id,))

        conn.commit()
        print(f"Success : The Community '{name}' has been created with ID {generated_id}.")

    except psycopg2.Error as e:
        conn.rollback()
        print("Error while creating a Community :", e)
    
    finally:
        conn.close()

def join_community(id_individual, id_community, is_creator=False):
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        
        sql = "INSERT INTO BelongTo (idIndividual, idCommunity, isCreator) VALUES (%s, %s, %s)"
        
        cur.execute(sql, (id_individual, id_community, is_creator))
        
        conn.commit()
        print("Success : Individual %s joined Community %s." % (id_individual, id_community))

    except psycopg2.Error as e:
        conn.rollback()
        print("Error while joining community :", e)
    
    finally:
        conn.close()

def create_link(id_source, id_target, description):
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        
        sql = "INSERT INTO Link (idSource, idTarget, description) VALUES (%s, %s, %s)"
        
        cur.execute(sql, (id_source, id_target, description))
        
        conn.commit()
        print("Success : Link created from %s to %s." % (id_source, id_target))

    except psycopg2.Error as e:
        conn.rollback()
        print("Error while creating link :", e)
    
    finally:
        conn.close()

def update_geolocation(id_individual, latitude, longitude):
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        sql_geo = "INSERT INTO GeoLocation (latitude, longitude) VALUES (%s, %s) RETURNING idGeolocation"
        cur.execute(sql_geo, (latitude, longitude))
        
        generated_id = cur.fetchone()[0]

        sql_update = "UPDATE Individual SET idGeolocation = %s WHERE idIndividual = %s"
        cur.execute(sql_update, (generated_id, id_individual))

        conn.commit()
        print(f"Success : Geolocation updated for individual '{id_individual}' with ID {generated_id}.")

    except psycopg2.Error as e:
        conn.rollback()
        print("Error while updating geolocation :", e)
    
    finally:
        conn.close()

def send_message(content, id_sender, id_receiver, id_reference=None):
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        sql = "INSERT INTO Message (content, idSender, idReceiver, idReference) VALUES (%s, %s, %s, %s)"
        
        cur.execute(sql, (content, id_sender, id_receiver, id_reference))
        
        conn.commit()
        if id_reference:
            print("Success : Reply sent from %s to %s (Ref: %s). " % (id_sender, id_receiver, id_reference))
        else:
            print("Success : Message sent from %s to %s." % (id_sender, id_receiver))

    except psycopg2.Error as e:
        conn.rollback()
        print("Error while sending message :", e)
    finally:
        conn.close()

def add_skill(skill_name):
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        sql = "INSERT INTO Skill (name) VALUES (%s)"
        cur.execute(sql, (skill_name,))
        conn.commit()
        print("Success : Skill '%s' added to repository." % skill_name)
    except psycopg2.Error as e:
        conn.rollback()
        print("Error while adding skill :", e)
    finally:
        conn.close()

def declare_skill(id_individual, skill_name, level):
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        sql = "INSERT INTO Master (idIndividual, idSkill, proficiency_level) VALUES (%s, %s, %s)"
        cur.execute(sql, (id_individual, skill_name, level))
        conn.commit()
        print("Success : Individual %s mastered '%s' at level %s." % (id_individual, skill_name, level))
    except psycopg2.Error as e:
        conn.rollback()
        print("Error while declaring skill :", e)
    finally:
        conn.close()

def propose_service(title, description, id_provider, type_service, price=None, expectation=None):
    
    conn = get_connection()
    if conn is None:
        return
    
    if type_service == 1:
        price = None
        expectation = None 
    elif type_service == 2:
        price = None      
    elif type_service == 3:  
        expectation = None      

    try:
        cur = conn.cursor()
        
        sql = """INSERT INTO Service 
                 (title, description_service, idProvider, type, price, description_expectation) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
                 
        cur.execute(sql, (title, description, id_provider, type_service, price, expectation))
        
        conn.commit()
        print(f"Success : Service '{title}' proposed by Individual {id_provider}.")

    except psycopg2.Error as e:
        conn.rollback()
        print("Error while proposing service :", e)
    finally:
        conn.close()

def vote_opposition(id_voter, id_target, id_community, reason):
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        
        sql = "INSERT INTO Opposition (idVoter, idTarget, idCommunity, reason) VALUES (%s, %s, %s, %s)"
        
        cur.execute(sql, (id_voter, id_target, id_community, reason))
        
        conn.commit()
        print("Success : Individual %s voted against %s in Community %s." % (id_voter, id_target, id_community))

    except psycopg2.Error as e:
        conn.rollback()
        print("Error while voting :", e)
    finally:
        conn.close()

def check_community_status(id_individual, id_community):
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        
        sql = "SELECT individual_name, community_name, is_excluded FROM Community_View WHERE idIndividual = %s AND idCommunity = %s"
        
        cur.execute(sql, (id_individual, id_community))
        result = cur.fetchone()
        
        if result:
            name, comm, excluded = result
            status = "EXCLUDED" if excluded else "ACTIVE"
            print("Status for %s in %s : [%s]" % (name, comm, status))
        else:
            print("No membership found for this individual or community.")

    except psycopg2.Error as e:
        print("Error reading view :", e)
    finally:
        conn.close()