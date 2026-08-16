import customtkinter as ctk
from tkinter import filedialog, messagebox
from ui.components import TableView, RecordDialog, RED
from config import APP_NAME, TAGLINE, VERSION

MODULES = {
    "People": ("employees", ["id", "employee_code", "full_name", "role", "employment_status"], [("employee_code","Employee ID"),("full_name","Full name"),("role","Role"),("phone","Phone"),("email","Email")]),
    "Districts": ("districts", ["id", "district_code", "name", "region", "status"], [("district_code","District ID"),("name","District name"),("region","Region"),("status","Status")]),
    "Territories": ("territories", ["id", "territory_code", "name", "district_id", "status"], [("territory_code","Territory ID"),("name","Territory name"),("district_id","District ID"),("status","Status")]),
    "Markets": ("markets", ["id", "market_code", "name", "territory_id", "status"], [("market_code","Market ID"),("name","Market name"),("district_id","District ID"),("territory_id","Territory ID"),("location","Physical location")]),
    "Booths": ("booths", ["id", "booth_code", "market_id", "location", "status"], [("booth_code","Booth ID"),("market_id","Market ID"),("location","Location"),("status","Status")]),
    "Partners": ("channel-partners", ["id", "partner_code", "business_name", "market_id", "status"], [("partner_code","Partner ID"),("business_name","Business name"),("contact_person","Owner/contact"),("market_id","Market ID"),("phone","Phone")]),
    "Resources": ("resources", ["id", "resource_code", "name", "condition", "status"], [("resource_code","Resource ID"),("name","Name"),("category_id","Category ID"),("condition","Condition"),("status","Status")]),
    "Assignments": ("resource-assignments", ["id", "resource_id", "employee_id", "market_id", "date_assigned"], [("resource_id","Resource ID"),("employee_id","Employee ID"),("market_id","Market ID"),("booth_id","Booth ID"),("partner_id","Partner ID"),("condition","Condition"),("notes","Notes")]),
    "Transfers": ("resource-transfers", ["id", "resource_id", "from_employee_id", "to_employee_id", "date"], [("resource_id","Resource ID"),("to_employee_id","To employee ID"),("to_market_id","To market ID"),("reason","Reason"),("date","Date YYYY-MM-DD")]),
    "Returns": ("resource-returns", ["id", "resource_id", "employee_id", "condition", "date"], [("resource_id","Resource ID"),("employee_id","Employee ID"),("condition","Condition"),("reason","Reason"),("notes","Notes")]),
    "Requests": ("resource-requests", ["id", "requested_by_id", "category_id", "required_date", "status"], [("requested_by_id","Requested by employee ID"),("category_id","Category ID"),("reason","Reason"),("market_id","Market ID"),("required_date","Required date YYYY-MM-DD")]),
    "Incidents": ("resource-incidents", ["id", "resource_id", "incident_type", "status", "date"], [("resource_id","Resource ID"),("incident_type","Lost/Damaged/Stolen/Faulty"),("description","Description"),("location","Location")]),
    "Tasks": ("tasks", ["id", "title", "assigned_employee_id", "priority", "status"], [("title","Task title"),("description","Description"),("assigned_employee_id","Assigned employee ID"),("priority","Priority"),("due_date","Due date YYYY-MM-DD")]),
    "Audits": ("audits", ["id", "market_id", "auditor_id", "audit_date", "status"], [("market_id","Market ID"),("auditor_id","Auditor employee ID"),("discrepancies","Discrepancies"),("status","Status")]),
    "Notifications": ("notifications", ["id", "title", "message", "unread", "created_at"], [("title","Title"),("message","Message"),("user_id","User ID")]),
}

ROLE_MENUS = {
    "Administrator": list(MODULES) + ["Reports", "Search", "About"],
    "ZBM": ["People","Districts","Territories","Markets","Booths","Partners","Resources","Assignments","Transfers","Returns","Tasks","Audits","Reports","Search","Notifications","About"],
    "TSM": ["People","Markets","Booths","Partners","Resources","Assignments","Transfers","Returns","Requests","Incidents","Tasks","Audits","Reports","Search","Notifications","About"],
    "TL": ["People","Markets","Booths","Partners","Resources","Assignments","Transfers","Returns","Requests","Incidents","Tasks","Audits","Search","Notifications","About"],
    "TSE": ["Markets","Booths","Partners","Resources","Requests","Incidents","Tasks","Audits","Notifications","About"],
    "Chabeba": ["Markets","Booths","Partners","Resources","Tasks","Incidents","Notifications","About"],
}

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, api, on_logout):
        super().__init__(master)
        self.api = api
        self.on_logout = on_logout
        self.sidebar = ctk.CTkFrame(self, width=210, corner_radius=0, fg_color="#1f1f1f")
        self.sidebar.pack(side="left", fill="y")
        self.content = ctk.CTkFrame(self, fg_color="#f6f7f9")
        self.content.pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(self.sidebar, text=APP_NAME.upper(), text_color=RED, font=("Segoe UI", 18, "bold"), wraplength=170).pack(pady=(20, 4), padx=12)
        ctk.CTkLabel(self.sidebar, text=TAGLINE, text_color="#d0d0d0", wraplength=170).pack(pady=(0, 16), padx=12)
        role = api.user.get("role", "TSE")
        ctk.CTkLabel(self.sidebar, text=role, text_color="#ffffff").pack(pady=(0, 12))
        ctk.CTkButton(self.sidebar, text="Dashboard", fg_color=RED, command=self.show_dashboard).pack(fill="x", padx=12, pady=3)
        for name in ROLE_MENUS.get(role, ROLE_MENUS["TSE"]):
            ctk.CTkButton(self.sidebar, text=name, fg_color="#333333", command=lambda n=name: self.show_module(n)).pack(fill="x", padx=12, pady=3)
        ctk.CTkButton(self.sidebar, text="Logout", fg_color="#6b1115", command=self.logout).pack(fill="x", padx=12, pady=(18, 8))
        self.show_dashboard()

    def clear(self):
        for child in self.content.winfo_children():
            child.destroy()

    def title(self, text):
        ctk.CTkLabel(self.content, text=text, text_color="#161616", font=("Segoe UI", 24, "bold")).pack(anchor="w", padx=18, pady=(16, 8))

    def show_dashboard(self):
        self.clear(); self.title("Dashboard")
        try:
            data = self.api.summary()
        except Exception as exc:
            messagebox.showerror("Connection", str(exc)); data = {}
        grid = ctk.CTkFrame(self.content, fg_color="transparent")
        grid.pack(fill="x", padx=14)
        for i, (label, value) in enumerate(data.items()):
            card = ctk.CTkFrame(grid, corner_radius=8, fg_color="#ffffff")
            card.grid(row=i//4, column=i%4, sticky="ew", padx=6, pady=6)
            ctk.CTkLabel(card, text=label.replace("_"," ").upper(), text_color="#666").pack(anchor="w", padx=12, pady=(10, 0))
            ctk.CTkLabel(card, text=str(value), text_color=RED, font=("Segoe UI", 26, "bold")).pack(anchor="w", padx=12, pady=(0, 12))
            grid.grid_columnconfigure(i%4, weight=1)

    def show_module(self, name):
        self.clear(); self.title(name)
        if name == "About":
            ctk.CTkLabel(self.content, text=f"{APP_NAME}\n{TAGLINE}\nVersion: {VERSION}\n\nField Sales Resource & Operations Management Platform", font=("Segoe UI", 18), justify="left").pack(anchor="w", padx=22, pady=10)
            return
        if name == "Reports":
            self.reports_screen(); return
        if name == "Search":
            self.search_screen(); return
        resource, columns, fields = MODULES[name]
        bar = ctk.CTkFrame(self.content, fg_color="transparent")
        bar.pack(fill="x", padx=14)
        ctk.CTkButton(bar, text="Add", fg_color=RED, width=90, command=lambda: RecordDialog(self, f"Add {name}", fields, lambda data: self.add_record(resource, data))).pack(side="right", padx=4)
        table = TableView(self.content, columns, on_refresh=lambda q: self.load_table(table, resource, q))
        table.pack(fill="both", expand=True, padx=10, pady=8)
        self.load_table(table, resource, "")

    def load_table(self, table, resource, query):
        try:
            table.set_rows(self.api.list(resource, query))
        except Exception as exc:
            messagebox.showerror("Airtel MarketLink", str(exc))

    def add_record(self, resource, data):
        self.api.create(resource, data)
        messagebox.showinfo("Saved", "Record saved successfully.")


    def reports_screen(self):
        reports = ["resources", "assigned-resources", "lost-resources", "damaged-resources", "transfers", "returns", "markets", "booths", "channel-partners", "employees", "tasks", "audits"]
        ctk.CTkLabel(self.content, text="Export CSV reports", text_color="#444", font=("Segoe UI", 14)).pack(anchor="w", padx=22, pady=(0, 10))
        panel = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        panel.pack(fill="both", expand=True, padx=16, pady=8)
        for report in reports:
            row = ctk.CTkFrame(panel, fg_color="#ffffff", corner_radius=8)
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=report.replace("-", " ").title(), font=("Segoe UI", 14, "bold")).pack(side="left", padx=12, pady=12)
            ctk.CTkButton(row, text="Export", fg_color=RED, width=90, command=lambda r=report: self.export_report(r)).pack(side="right", padx=12, pady=8)

    def export_report(self, report):
        destination = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=f"{report}.csv", filetypes=[("CSV files", "*.csv")])
        if not destination:
            return
        try:
            self.api.download_report(report, destination)
            messagebox.showinfo("Export complete", f"Saved {report}.csv")
        except Exception as exc:
            messagebox.showerror("Airtel MarketLink", str(exc))
    def search_screen(self):
        q = ctk.StringVar()
        ctk.CTkEntry(self.content, textvariable=q, placeholder_text="Search employee, resource, market, booth, partner").pack(fill="x", padx=20, pady=8)
        output = ctk.CTkTextbox(self.content)
        output.pack(fill="both", expand=True, padx=20, pady=8)
        def run():
            output.delete("1.0", "end")
            output.insert("end", str(self.api.search(q.get())))
        ctk.CTkButton(self.content, text="Search", fg_color=RED, command=run).pack(padx=20, pady=8)

    def logout(self):
        try:
            self.api.logout()
        finally:
            self.on_logout()




