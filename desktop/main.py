import customtkinter as ctk
from api_client import ApiClient
from config import APP_NAME
from ui.login import LoginFrame
from ui.dashboard import DashboardFrame

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class AirtelMarketLink(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1180x760")
        self.minsize(980, 640)
        self.api = ApiClient()
        self.frame = None
        self.show_login()

    def swap(self, frame):
        if self.frame:
            self.frame.destroy()
        self.frame = frame
        self.frame.pack(fill="both", expand=True)

    def show_login(self):
        self.swap(LoginFrame(self, self.api, self.show_dashboard))

    def show_dashboard(self):
        self.swap(DashboardFrame(self, self.api, self.show_login))

if __name__ == "__main__":
    AirtelMarketLink().mainloop()
