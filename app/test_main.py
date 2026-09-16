from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_product_16():
    response = client.get("/products/16")
    assert response.status_code == 200
    assert response.json() == {"message": "product 16 in stock"}
