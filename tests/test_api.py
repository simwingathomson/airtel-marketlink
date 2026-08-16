import pytest
from backend.app import create_app, seed
from backend.app.extensions import db
from backend.app.models import User, Resource

@pytest.fixture()
def client():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
        seed(app)
    return app.test_client()

def auth(client):
    res = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert res.status_code == 200
    return {"Authorization": "Bearer " + res.get_json()["token"]}

def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}

def test_auth_and_password_hashing(client):
    headers = auth(client)
    assert client.get("/api/reports/summary", headers=headers).status_code == 200
    with client.application.app_context():
        assert User.query.filter_by(username="admin").first().password_hash != "admin123"

def test_role_permissions(client):
    assert client.get("/api/employees").status_code == 401

def test_employee_market_booth_partner_resource_creation(client):
    headers = auth(client)
    employee = client.post("/api/employees", headers=headers, json={"employee_code":"EMP-X","full_name":"Test User","role":"TSE"})
    assert employee.status_code == 201
    district = client.post("/api/districts", headers=headers, json={"district_code":"DST-X","name":"Test District"}).get_json()
    territory = client.post("/api/territories", headers=headers, json={"territory_code":"TER-X","name":"Test Territory","district_id":district["id"]}).get_json()
    market = client.post("/api/markets", headers=headers, json={"market_code":"MKT-X","name":"Test Market","district_id":district["id"],"territory_id":territory["id"]})
    assert market.status_code == 201
    booth = client.post("/api/booths", headers=headers, json={"booth_code":"BTH-X","market_id":market.get_json()["id"]})
    assert booth.status_code == 201
    partner = client.post("/api/channel-partners", headers=headers, json={"partner_code":"CP-X","business_name":"Test Partner","market_id":market.get_json()["id"]})
    assert partner.status_code == 201
    resource = client.post("/api/resources", headers=headers, json={"resource_code":"PH-X","name":"Phone X","condition":"Good"})
    assert resource.status_code == 201

def test_assignment_transfer_return_incident_task_audit(client):
    headers = auth(client)
    resources = client.get("/api/resources", headers=headers).get_json()
    employees = client.get("/api/employees", headers=headers).get_json()
    markets = client.get("/api/markets", headers=headers).get_json()
    booths = client.get("/api/booths", headers=headers).get_json()
    partners = client.get("/api/channel-partners", headers=headers).get_json()
    chabebas = [employee for employee in employees if employee["role"] == "Chabeba"]
    rid = resources[0]["id"]
    e1, e2 = chabebas[0]["id"], chabebas[1]["id"]
    mid, bid, pid = markets[0]["id"], booths[0]["id"], partners[0]["id"]
    assert client.post("/api/resource-assignments", headers=headers, json={"resource_id":rid,"employee_id":e1,"market_id":mid,"booth_id":bid,"partner_id":pid,"condition":"Good"}).status_code == 201
    assert client.post("/api/resource-transfers", headers=headers, json={"resource_id":rid,"to_employee_id":e2,"to_market_id":mid,"booth_id":bid,"partner_id":pid,"reason":"Employee transfer"}).status_code == 201
    assert client.post("/api/resource-returns", headers=headers, json={"resource_id":rid,"employee_id":e2,"condition":"Good","reason":"Store return"}).status_code == 201
    assert client.post("/api/resource-incidents", headers=headers, json={"resource_id":rid,"incident_type":"Damaged","description":"Screen cracked"}).status_code == 201
    assert client.post("/api/resource-incidents", headers=headers, json={"resource_id":rid,"incident_type":"Lost","description":"Missing in market"}).status_code == 201
    assert client.post("/api/tasks", headers=headers, json={"title":"Inspect booth","assigned_employee_id":e1,"market_id":mid}).status_code == 201
    assert client.post("/api/audits", headers=headers, json={"market_id":mid,"auditor_id":e1,"discrepancies":"None"}).status_code == 201
    history = client.get(f"/api/resources/{rid}/history", headers=headers).get_json()
    assert len(history["assignments"]) >= 1

def test_search_report_csv_and_upload_validation(client):
    headers = auth(client)
    search = client.get("/api/search?q=City", headers=headers)
    assert search.status_code == 200
    assert search.get_json()["markets"]
    csv_response = client.get("/api/reports/resources.csv", headers=headers)
    assert csv_response.status_code == 200
    assert csv_response.mimetype == "text/csv"
    assert b"resource_code" in csv_response.data
    bad_upload = client.post(
        "/api/uploads",
        headers=headers,
        data={"file": (b"not allowed", "danger.exe")},
        content_type="multipart/form-data",
    )
    assert bad_upload.status_code == 400

def web_login(client):
    return client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)

def test_web_login_dashboard_module_and_reports(client):
    login = web_login(client)
    assert login.status_code == 200
    assert b'Dashboard' in login.data
    people = client.get('/modules/people')
    assert people.status_code == 200
    assert b'People' in people.data
    new_page = client.get('/modules/resources/new')
    assert new_page.status_code == 200
    assert b'Add Resources' in new_page.data
    reports = client.get('/reports')
    assert reports.status_code == 200
    assert b'CSV Reports' in reports.data
    csv_response = client.get('/reports/employees.csv')
    assert csv_response.status_code == 200
    assert csv_response.mimetype == 'text/csv'

