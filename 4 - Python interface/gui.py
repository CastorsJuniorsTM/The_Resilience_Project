import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import psycopg2
from main import *

class ResilienceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resilience Project - Manager")
        self.root.geometry("900x700")

        style = ttk.Style()
        style.theme_use('clam')

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.tab_create = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_create, text="1. Creation")
        self.setup_creation_tab()

        self.tab_actions = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_actions, text="2. Actions")
        self.setup_actions_tab()

        self.tab_services = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_services, text="3. Services/Skills")
        self.setup_services_tab()

        self.tab_messages = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_messages, text="4. Mail box")
        self.setup_messages_tab()

        self.tab_views = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_views, text="5. Browse Database")
        self.setup_views_tab()

    def setup_creation_tab(self):
        frame = ttk.LabelFrame(self.tab_create, text="Add an entity", padding=20)
        frame.pack(padx=20, pady=20, fill="x")

        ttk.Label(frame, text="Type:").grid(row=0, column=0, sticky="w")
        self.type_var = tk.StringVar(value="1")
        ttk.Radiobutton(frame, text="Individual", variable=self.type_var, value="1").grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(frame, text="Community", variable=self.type_var, value="2").grid(row=0, column=2, sticky="w")


        ttk.Label(frame, text="Name:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_name = ttk.Entry(frame)
        self.entry_name.grid(row=2, column=1, columnspan=2, sticky="we")

        ttk.Label(frame, text="Email (Indiv):").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_email = ttk.Entry(frame)
        self.entry_email.grid(row=3, column=1, columnspan=2, sticky="we")

        ttk.Button(frame, text="Create entity", command=self.create_entity).grid(row=4, column=1, pady=20)

    def create_entity(self):
        try:
            eid = int(self.entry_id.get())
            name = self.entry_name.get()
            email = self.entry_email.get()
            
            if self.type_var.get() == "1": 
                add_individual(eid, name, email)
                messagebox.showinfo("Success", f"Individual {name} has been added !")
            else: 
                add_community(eid, name)
                messagebox.showinfo("Success", f"Community {name} has been added !")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def setup_actions_tab(self):
        f1 = ttk.LabelFrame(self.tab_actions, text="Rejoindre Communauté", padding=10)
        f1.pack(fill="x", padx=10, pady=5)
        ttk.Label(f1, text="ID Individual:").pack(side="left")
        self.act_join_uid = ttk.Entry(f1, width=10); self.act_join_uid.pack(side="left", padx=5)
        ttk.Label(f1, text="ID Community:").pack(side="left")
        self.act_join_cid = ttk.Entry(f1, width=10); self.act_join_cid.pack(side="left", padx=5)
        ttk.Button(f1, text="Join", command=self.action_join).pack(side="left", padx=10)

        f2 = ttk.LabelFrame(self.tab_actions, text="Create a Link", padding=10)
        f2.pack(fill="x", padx=10, pady=5)
        ttk.Label(f2, text="Source ID:").pack(side="left")
        self.act_link_src = ttk.Entry(f2, width=8); self.act_link_src.pack(side="left", padx=5)
        ttk.Label(f2, text="Target ID:").pack(side="left")
        self.act_link_dst = ttk.Entry(f2, width=8); self.act_link_dst.pack(side="left", padx=5)
        ttk.Label(f2, text="Description:").pack(side="left")
        self.act_link_desc = ttk.Entry(f2, width=15); self.act_link_desc.pack(side="left", padx=5)
        ttk.Button(f2, text="Link", command=self.action_link).pack(side="left", padx=10)

        # Frame 3: Geo
        f3 = ttk.LabelFrame(self.tab_actions, text="Geolocation", padding=10)
        f3.pack(fill="x", padx=10, pady=5)
        ttk.Label(f3, text="ID Individual:").pack(side="left")
        self.act_geo_uid = ttk.Entry(f3, width=8); self.act_geo_uid.pack(side="left", padx=5)
        ttk.Label(f3, text="Geolocation ID:").pack(side="left")
        self.act_geo_gid = ttk.Entry(f3, width=8); self.act_geo_gid.pack(side="left", padx=5)
        ttk.Label(f3, text="Latitude:").pack(side="left")
        self.act_geo_lat = ttk.Entry(f3, width=10); self.act_geo_lat.pack(side="left", padx=5)
        ttk.Label(f3, text="Longitude:").pack(side="left")
        self.act_geo_lon = ttk.Entry(f3, width=10); self.act_geo_lon.pack(side="left", padx=5)
        ttk.Button(f3, text="Update", command=self.action_geo).pack(side="left", padx=10)

        f4 = ttk.LabelFrame(self.tab_actions, text="Opposition Vote ", padding=10)
        f4.pack(fill="x", padx=10, pady=5)
        
        grid_f4 = ttk.Frame(f4)
        grid_f4.pack()
        ttk.Label(grid_f4, text="Vote ID:").grid(row=0, column=0)
        self.act_vote_oid = ttk.Entry(grid_f4, width=5)
        self.act_vote_oid.grid(row=0, column=1)

        ttk.Label(grid_f4, text="Voter ID:").grid(row=0, column=2)
        self.act_vote_vid = ttk.Entry(grid_f4, width=5)
        self.act_vote_vid.grid(row=0, column=3)
        
        ttk.Label(grid_f4, text="Target ID:").grid(row=0, column=4)
        self.act_vote_tid = ttk.Entry(grid_f4, width=5)
        self.act_vote_tid.grid(row=0, column=5)

        ttk.Label(grid_f4, text="Community ID:").grid(row=0, column=6)
        self.act_vote_cid = ttk.Entry(grid_f4, width=5)
        self.act_vote_cid.grid(row=0, column=7)

        ttk.Label(grid_f4, text="Reason:").grid(row=1, column=0)
        self.act_vote_reason = ttk.Entry(grid_f4, width=30)
        self.act_vote_reason.grid(row=1, column=1, columnspan=4)
        
        ttk.Button(grid_f4, text="Vote", command=self.action_vote).grid(row=1, column=6)

    def action_join(self):
        try: join_community(int(self.act_join_uid.get()), int(self.act_join_cid.get()))
        except Exception as e: messagebox.showerror("Error", str(e))
        else: messagebox.showinfo("Success", "Community joined!")

    def action_link(self):
        try: create_link(int(self.act_link_src.get()), int(self.act_link_dst.get()), self.act_link_desc.get())
        except Exception as e: messagebox.showerror("Error", str(e))
        else: messagebox.showinfo("Success", "Link created !")

    def action_geo(self):
        try: update_geolocation(int(self.act_geo_uid.get()), int(self.act_geo_gid.get()), float(self.act_geo_lat.get()), float(self.act_geo_lon.get()))
        except Exception as e: messagebox.showerror("Error", str(e))
        else: messagebox.showinfo("Success", "Geolocation updated !")

    def action_vote(self):
        try: vote_opposition(int(self.act_vote_oid.get()), int(self.act_vote_vid.get()), int(self.act_vote_tid.get()), int(self.act_vote_cid.get()), self.act_vote_reason.get())
        except Exception as e: messagebox.showerror("Error", str(e))
        else: messagebox.showinfo("Success", "Vote saved !")


    def setup_services_tab(self):
        # Skills
        f1 = ttk.LabelFrame(self.tab_services, text="Declare a Skill", padding=10)
        f1.pack(fill="x", padx=10, pady=5)
        ttk.Label(f1, text="ID Individual:").pack(side="left")
        self.sk_uid = ttk.Entry(f1, width=5); self.sk_uid.pack(side="left")
        ttk.Label(f1, text="Skill:").pack(side="left")
        self.sk_name = ttk.Entry(f1, width=15); self.sk_name.pack(side="left")
        ttk.Label(f1, text="Level (1-5):").pack(side="left")
        self.sk_lvl = ttk.Entry(f1, width=5); self.sk_lvl.pack(side="left")
        ttk.Button(f1, text="Declare", command=self.do_skill).pack(side="left", padx=10)

        # Services
        f2 = ttk.LabelFrame(self.tab_services, text="Offer a Service", padding=10)
        f2.pack(fill="x", padx=10, pady=5)
        grid = ttk.Frame(f2); grid.pack()
        
        ttk.Label(grid, text="Service ID:").grid(row=0, column=0)
        self.sv_id = ttk.Entry(grid, width=5); self.sv_id.grid(row=0, column=1)
        
        ttk.Label(grid, text="Provider ID:").grid(row=0, column=2)
        self.sv_pid = ttk.Entry(grid, width=5); self.sv_pid.grid(row=0, column=3)

        ttk.Label(grid, text="Title:").grid(row=0, column=4)
        self.sv_titre = ttk.Entry(grid, width=15); self.sv_titre.grid(row=0, column=5)

        ttk.Label(grid, text="Type (1,2,3):").grid(row=1, column=0)
        self.sv_type = ttk.Entry(grid, width=5); self.sv_type.grid(row=1, column=1)

        ttk.Label(grid, text="Price:").grid(row=1, column=2)
        self.sv_price = ttk.Entry(grid, width=5); self.sv_price.grid(row=1, column=3)

        ttk.Label(grid, text="Description:").grid(row=1, column=4)
        self.sv_desc = ttk.Entry(grid, width=15); self.sv_desc.grid(row=1, column=5)

        ttk.Button(grid, text="Offer", command=self.do_service).grid(row=2, column=2)

    def do_skill(self):
        try:
            try: add_skill(self.sk_name.get())
            except: pass
            declare_skill(int(self.sk_uid.get()), self.sk_name.get(), int(self.sk_lvl.get()))
            messagebox.showinfo("Success", "Skill added")
        except Exception as e: messagebox.showerror("Error", str(e))

    def do_service(self):
        try:
            propose_service(int(self.sv_id.get()), self.sv_titre.get(), self.sv_desc.get(), int(self.sv_pid.get()), int(self.sv_type.get()), float(self.sv_price.get()))
            messagebox.showinfo("Success", "Service proposed")
        except Exception as e: messagebox.showerror("Error", str(e))

    def setup_messages_tab(self):
        f = ttk.Frame(self.tab_messages, padding=20)
        f.pack()
        
        ttk.Label(f, text="Message ID:").grid(row=0, column=0)
        self.msg_id = ttk.Entry(f); self.msg_id.grid(row=0, column=1)

        ttk.Label(f, text="Sender ID:").grid(row=1, column=0)
        self.msg_src = ttk.Entry(f); self.msg_src.grid(row=1, column=1)

        ttk.Label(f, text="Receiver ID:").grid(row=2, column=0)
        self.msg_dst = ttk.Entry(f); self.msg_dst.grid(row=2, column=1)

        ttk.Label(f, text="Answer to ID:").grid(row=3, column=0)
        self.msg_ref = ttk.Entry(f); self.msg_ref.grid(row=3, column=1)

        ttk.Label(f, text="Content:").grid(row=4, column=0)
        self.msg_content = ttk.Entry(f, width=50); self.msg_content.grid(row=4, column=1)

        ttk.Button(f, text="Send", command=self.do_msg).grid(row=5, column=1, pady=10)

    def do_msg(self):
        try:
            ref = self.msg_ref.get()
            rid = int(ref) if ref else None
            send_message(int(self.msg_id.get()), self.msg_content.get(), int(self.msg_src.get()), int(self.msg_dst.get()), rid)
            messagebox.showinfo("Success", "Message send")
        except Exception as e: messagebox.showerror("Error", str(e))


    def setup_views_tab(self):
        ctrl_frame = ttk.Frame(self.tab_views, padding=10)
        ctrl_frame.pack(fill="x")

        ttk.Label(ctrl_frame, text="ID / Keyword:").pack(side="left")
        self.view_input = ttk.Entry(ctrl_frame, width=20)
        self.view_input.pack(side="left", padx=5)

        ttk.Button(ctrl_frame, text="See Communities (ID)", command=self.view_comm).pack(side="left", padx=2)
        ttk.Button(ctrl_frame, text="See Messages (ID)", command=self.view_msg).pack(side="left", padx=2)
        ttk.Button(ctrl_frame, text="See Proximity (<1km)", command=self.view_prox).pack(side="left", padx=2)
        ttk.Button(ctrl_frame, text="Search (Txt)", command=self.view_search).pack(side="left", padx=2)

        self.display_area = scrolledtext.ScrolledText(self.tab_views, width=100, height=30)
        self.display_area.pack(padx=10, pady=10)

    def log(self, text):
        self.display_area.delete(1.0, tk.END)
        self.display_area.insert(tk.END, text)

    def view_comm(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT community_name, is_excluded FROM Community_View WHERE idIndividual = %s", (self.view_input.get(),))
            rows = cur.fetchall()
            out = f"--- Communitiess with ID {self.view_input.get()} ---\n"
            for r in rows:
                status = "EXCLUDED" if r[1] else "ACTIF"
                out += f"- {r[0]} [{status}]\n"
            self.log(out)
            conn.close()
        except Exception as e: self.log(f"Error: {e}")

    def view_msg(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT sender_name, receiver_name, content, parent_message_preview 
                FROM Message_View 
                WHERE sender_name = (SELECT name FROM Connectable_Entity WHERE idEntity=%s)
                OR receiver_name = (SELECT name FROM Connectable_Entity WHERE idEntity=%s)
            """, (self.view_input.get(), self.view_input.get()))
            out = f"--- Messages for ID {self.view_input.get()} ---\n"
            for r in cur.fetchall():
                fil = f"(Answer to: {r[3][:20]}...)" if r[3] else "(New discussion)"
                out += f"From {r[0]} to {r[1]} : {r[2]} {fil}\n"
            self.log(out)
            conn.close()
        except Exception as e: self.log(f"Error: {e}")

    def view_prox(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT name_person_A, name_person_B, distance_km FROM Proximity_View")
            out = "--- Proximity (< 1km) ---\n"
            for r in cur.fetchall():
                out += f"{r[0]} <--> {r[1]} : {round(r[2], 3)} km\n"
            self.log(out)
            conn.close()
        except Exception as e: self.log(f"Error: {e}")

    def view_search(self):
        try:
            kw = self.view_input.get()
            conn = get_connection()
            cur = conn.cursor()
            out = f"--- Search for '{kw}' ---\n"
            
            cur.execute("SELECT idEntity, name FROM Connectable_Entity JOIN Individual ON idEntity=idIndividual WHERE name ILIKE %s", ('%' + kw + '%',))
            for r in cur.fetchall(): out += f"[Individual] ID: {r[0]} | Name: {r[1]}\n"

            cur.execute("SELECT idEntity, name FROM Connectable_Entity JOIN Community ON idEntity=idCommunity WHERE name ILIKE %s", ('%' + kw + '%',))
            for r in cur.fetchall(): out += f"[Community] ID: {r[0]} | Name: {r[1]}\n"

            cur.execute("SELECT title, price, type FROM Service WHERE title ILIKE %s", ('%' + kw + '%',))
            for r in cur.fetchall(): out += f"[Service] {r[0]} (Price: {r[1]})\n"
            
            self.log(out)
            conn.close()
        except Exception as e: self.log(f"Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ResilienceApp(root)
    root.mainloop()