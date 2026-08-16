import customtkinter as ctk
from tkinter import ttk, messagebox

RED = "#e41f26"

class TableView(ctk.CTkFrame):
    def __init__(self, master, columns, on_refresh=None, **kwargs):
        super().__init__(master, **kwargs)
        self.columns = columns
        self.on_refresh = on_refresh
        self.search_var = ctk.StringVar()
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=8, pady=8)
        ctk.CTkEntry(top, textvariable=self.search_var, placeholder_text="Search").pack(side="left", fill="x", expand=True)
        ctk.CTkButton(top, text="Search", width=90, command=self.refresh).pack(side="left", padx=6)
        ctk.CTkButton(top, text="Refresh", width=90, command=self.refresh).pack(side="left")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=18)
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title(), command=lambda c=col: self.sort(c))
            self.tree.column(col, width=130, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def set_rows(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in rows:
            self.tree.insert("", "end", values=[row.get(c, "") for c in self.columns])

    def refresh(self):
        if self.on_refresh:
            self.on_refresh(self.search_var.get().strip())

    def sort(self, column):
        rows = [(self.tree.set(k, column), k) for k in self.tree.get_children("")]
        rows.sort()
        for index, (_, key) in enumerate(rows):
            self.tree.move(key, "", index)

class RecordDialog(ctk.CTkToplevel):
    def __init__(self, master, title, fields, on_submit):
        super().__init__(master)
        self.title(title)
        self.geometry("460x520")
        self.entries = {}
        self.on_submit = on_submit
        ctk.CTkLabel(self, text=title, font=("Segoe UI", 20, "bold")).pack(pady=14)
        body = ctk.CTkScrollableFrame(self)
        body.pack(fill="both", expand=True, padx=14)
        for key, label in fields:
            ctk.CTkLabel(body, text=label, anchor="w").pack(fill="x", pady=(8, 2))
            entry = ctk.CTkEntry(body)
            entry.pack(fill="x")
            self.entries[key] = entry
        ctk.CTkButton(self, text="Save", fg_color=RED, command=self.submit).pack(fill="x", padx=14, pady=14)

    def submit(self):
        data = {k: e.get().strip() for k, e in self.entries.items() if e.get().strip()}
        try:
            self.on_submit(data)
            self.destroy()
        except Exception as exc:
            messagebox.showerror("Airtel MarketLink", str(exc))
