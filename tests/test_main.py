import fastapi.testclient
from app.main import app

client = fastapi.testclient.TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Career Compass AI running"
    }
def test_invalid_file_type():

    response = client.post(
        "/upload-resume",
        files={"file": ("image.jpg", b"fake", "image/jpeg")}
    )

    assert response.status_code == 400