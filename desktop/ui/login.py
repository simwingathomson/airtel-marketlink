import customtkinter as ctk
from tkinter import messagebox
from config import APP_NAME, TAGLINE

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, api, on_login):
        super().__init__(master, fg_color="#ffffff")
        self.api = api
        self.on_login = on_login
        card = ctk.CTkFrame(self, width=420, corner_radius=8)
        card.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(card, text=APP_NAME.upper(), text_color="#e41f26", font=("Segoe UI", 28, "bold")).pack(pady=(28, 4))
        ctk.CTkLabel(card, text=TAGLINE, font=("Segoe UI", 13)).pack(pady=(0, 24))
        self.username = ctk.CTkEntry(card, placeholder_text="Username")
        self.username.pack(fill="x", padx=30, pady=8)
        self.password = ctk.CTkEntry(card, placeholder_text="Password", show="*")
        self.password.pack(fill="x", padx=30, pady=8)
        ctk.CTkButton(card, text="Sign In", fg_color="#e41f26", command=self.login).pack(fill="x", padx=30, pady=18)
        ctk.CTkLabel(card, text="Demo: admin / admin123", text_color="#666").pack(pady=(0, 24))

    def login(self):
        try:
            self.api.login(self.username.get(), self.password.get())
            self.on_login()
        except Exception as exc:
            messagebox.showerror("Login failed", str(exc))
