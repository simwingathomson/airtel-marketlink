import requests
from config import API_BASE_URL

class ApiError(Exception):
    pass

class ApiClient:
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.token = None
        self.user = None

    def headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def request(self, method, path, **kwargs):
        try:
            response = requests.request(method, f"{self.base_url}{path}", headers=self.headers(), timeout=8, **kwargs)
        except requests.RequestException as exc:
            raise ApiError("Unable to connect to Airtel MarketLink server. Please check your internet connection.") from exc
        if response.status_code >= 400:
            try:
                message = response.json().get("error", response.text)
            except ValueError:
                message = response.text
            raise ApiError(message)
        return response.json() if response.content else None

    def login(self, username, password):
        data = self.request("POST", "/api/auth/login", json={"username": username, "password": password})
        self.token = data["token"]
        self.user = data["user"]
        return data

    def logout(self):
        if self.token:
            self.request("POST", "/api/auth/logout")
        self.token = None
        self.user = None

    def list(self, resource, search=None):
        return self.request("GET", f"/api/{resource}", params={"search": search} if search else None)

    def create(self, resource, payload):
        return self.request("POST", f"/api/{resource}", json=payload)

    def summary(self):
        return self.request("GET", "/api/reports/summary")

    def search(self, query):
        return self.request("GET", "/api/search", params={"q": query})

    def download_report(self, report_name, destination):
        try:
            response = requests.get(f"{self.base_url}/api/reports/{report_name}.csv", headers=self.headers(), timeout=15)
        except requests.RequestException as exc:
            raise ApiError("Unable to connect to Airtel MarketLink server. Please check your internet connection.") from exc
        if response.status_code >= 400:
            raise ApiError(response.text)
        with open(destination, "wb") as file:
            file.write(response.content)
        return destination
