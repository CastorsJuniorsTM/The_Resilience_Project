from main import *

def search_database(keyword):
    conn = get_connection()
    if conn is None: return
    try:
        cur = conn.cursor()
        print(f"\n--- Search results for '{keyword}' ---")
        
        cur.execute("SELECT idEntity, name FROM Connectable_Entity JOIN Individual ON idEntity=idIndividual WHERE name ILIKE %s", ('%' + keyword + '%',))
        rows = cur.fetchall()
        for r in rows: print(f"[Individual] ID: {r[0]} | Name: {r[1]}")

        cur.execute("SELECT idEntity, name FROM Connectable_Entity JOIN Community ON idEntity=idCommunity WHERE name ILIKE %s", ('%' + keyword + '%',))
        rows = cur.fetchall()
        for r in rows: print(f"[Community] ID: {r[0]} | Name: {r[1]}")

        cur.execute("SELECT * FROM Service WHERE title ILIKE %s", ('%' + keyword + '%',))
        rows = cur.fetchall()
        for r in rows:
            print(f"""
            [ID Service]: {r[0]}
            Title       : {r[1]}
            Description : {r[2]}
            Provider ID : {r[3]}
            Type        : {r[4]} (1=Free, 2=Exchange, 3=Commercial)
            Price       : {r[5]}
            Expectation : {r[6]}
            """)

    except psycopg2.Error as e:
        print("Search error:", e)
    finally:
        conn.close()

def show_community_view(id_person):
    conn = get_connection()
    if conn is None: return
    try:
        cur = conn.cursor()
        cur.execute("SELECT community_name, is_excluded FROM Community_View WHERE idIndividual = %s", (id_person,))
        rows = cur.fetchall()
        print(f"\n--- Communities for ID {id_person} ---")
        if not rows: print("No community found.")
        for r in rows:
            status = "EXCLUDED" if r[1] else "ACTIVE"
            print(f"- {r[0]} [{status}]")
    except psycopg2.Error as e:
        print("Community View error:", e)
    finally:
        conn.close()

def show_message_view(id_person):
    conn = get_connection()
    if conn is None: return
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT sender_name, receiver_name, content, parent_message_preview 
            FROM Message_View 
            WHERE sender_name = (SELECT name FROM Connectable_Entity WHERE idEntity=%s)
            OR receiver_name = (SELECT name FROM Connectable_Entity WHERE idEntity=%s)
        """, (id_person, id_person))
        
        print(f"\n--- Messages for ID {id_person} ---")
        rows = cur.fetchall()
        for r in rows:
            fil = f"(Reply to: {r[3][:20]}...)" if r[3] else "(New thread)"
            print(f"From {r[0]} to {r[1]} : {r[2]} {fil}")
    except psycopg2.Error as e:
        print("Message View error:", e)
    finally:
        conn.close()

def show_proximity_view():
    conn = get_connection()
    if conn is None: return
    try:
        cur = conn.cursor()
        cur.execute("SELECT name_person_A, name_person_B, distance_km FROM Proximity_View")
        rows = cur.fetchall()
        print("\n--- People within 1 km ---")
        if not rows: print("No one nearby.")
        for r in rows:
            print(f"{r[0]} <--> {r[1]} : {round(r[2], 3)} km")
    except psycopg2.Error as e:
        print("Proximity View error:", e)
    finally:
        conn.close()

def show_individuals_view():
    conn = get_connection()
    if conn is None: return
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, latitude, longitude FROM View_Individuals")
        rows = cur.fetchall()
        
        print("\n--- List of All Individuals ---")
        if not rows: print("No individuals found.")
        
        for r in rows:
            loc_display = f"[{r[3]}, {r[4]}]" if r[3] is not None and r[4] is not None else "No Geo"
            
            print(f"ID {r[0]} : {r[1]} ({r[2]}) - Loc: {loc_display}")
            
    except psycopg2.Error as e:
        print("Individuals View error:", e)
    finally:
        conn.close()

def show_communities_view():
    conn = get_connection()
    if conn is None: return
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, public_key_G1 FROM View_Communities")
        rows = cur.fetchall()
        
        print("\n--- List of All Communities ---")
        if not rows: print("No communities found.")
        
        for r in rows:
            pub_key_display = f" (Key: {r[2]})" if r[2] else ""
            print(f"ID {r[0]} : {r[1]}{pub_key_display}")
            
    except psycopg2.Error as e:
        print("Communities View error:", e)
    finally:
        conn.close()

def main_menu():
    while True:
        print("\n" + "="*30)
        print("   RESILIENCE PROJECT - MENU")
        print("="*30)
        print("1. Entity Management (Add Individual/Community)")
        print("2. Join a Community / Create Link")
        print("3. Messaging (Send/Reply)")
        print("4. Geolocation (Update)")
        print("5. Skills & Services")
        print("6. Vote (Opposition)")
        print("-" * 30)
        print("7. [VIEW] My Communities (Excluded/Active Status)")
        print("8. [VIEW] My Messages (Threads)")
        print("9. [VIEW] Proximité (Who is < 1km?)")
        print("10. [VIEW] List of every Individuals")
        print("11. [VIEW] List of every Communities")
        print("12. [SEARCH] Search for a person/service")
        print("0. Exit")
        
        choice = input("\nYour choice: ")

        if choice == "1":
            type_e = input("Type (1=Individual, 2=Community): ")
            nom = input("Name: ")
            if type_e == "1":
                email = input("Email: ")
                add_individual(nom, email)
            else:
                add_community(nom)

        elif choice == "2":
            sub = input("1=Join Community, 2=Create Link: ")
            if sub == "1":
                u = int(input("Individual ID: "))
                c = int(input("Community ID: "))
                join_community(u, c)
            else:
                s = int(input("Source ID: "))
                t = int(input("Target ID: "))
                desc = input("Description: ")
                create_link(s, t, desc)

        elif choice == "3":
            src = int(input("Sender ID: "))
            dst = int(input("Receiver ID: "))
            msg = input("Message: ")
            ref = input("Reply ID (leave empty if new): ")
            ref_id = int(ref) if ref else None
            send_message(msg, src, dst, ref_id)

        elif choice == "4":
            uid = int(input("Individual ID: "))
            lat = float(input("Latitude: "))
            lon = float(input("Longitude: "))
            update_geolocation(uid, lat, lon)

        elif choice == "5":
            sub = input("1=Declare Skill, 2=Propose Service: ")
            if sub == "1":
                u = int(input("Individual ID: "))
                skill = input("Skill Name: ")
                lvl = int(input("Level (1-5): "))
                try:
                    add_skill(skill) 
                except: pass
                declare_skill(u, skill, lvl)
            else:
                p = int(input("Provider ID: "))
                titre = input("Title: ")
                desc = input("Description: ")
                typ = int(input("Type (1=Free, 2=Exchange, 3=G1): "))
                
                prix = None
                attente = None

                if typ == 2:
                    attente = input("Expectation (what in return?): ")
                elif typ == 3:
                    p_input = input("Price: ")
                    prix = float(p_input) if p_input else 0

                propose_service(titre, desc, p, typ, prix, attente)

        elif choice == "6":
            v = int(input("Voter ID: "))
            t = int(input("Target ID: "))
            c = int(input("Community ID: "))
            r = input("Reason: ")
            vote_opposition(v, t, c, r)

        elif choice == "7":
            u = int(input("Individual ID to consult: "))
            show_community_view(u)

        elif choice == "8":
            u = int(input("Individual ID to consult: "))
            show_message_view(u)

        elif choice == "9":
            show_proximity_view()

        elif choice =="10":
            show_individuals_view()

        elif choice =="11":
            show_communities_view() 

        elif choice == "12":
            k = input("Keyword to search: ")
            search_database(k)

        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()