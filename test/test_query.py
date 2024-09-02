from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_query_yields_10_results():
    response = client.get("/query?query=sushi")
    json_response = response.json()
    
    assert response.status_code == 200
    assert len(json_response["results"]) == 10
    assert json_response["message"] == "OK"

def test_query_yields_few_results():
    response = client.get("/query?query=hambúrguer")
    json_response = response.json()
    
    assert response.status_code == 200
    assert 1 < len(json_response["results"]) < 10
    assert json_response["message"] == "OK"

def test_query_yields_non_obvious_results():
    response = client.get("/query?query=maravilhoso")
    json_response = response.json()
    
    assert response.status_code == 200
    assert len(json_response["results"]) > 0
    assert json_response["results"][0]["title"] == "Aguzzo Cucina Italiana - Jardins"
    assert json_response["results"][1]["title"] == "GaraGer Montevideo Parrillada Uruguaia"
    assert json_response["results"][2]["title"] == "Djapa"
    assert json_response["results"][3]["title"] == "I Love Burger"
    assert json_response["results"][4]["title"] == "Bistrot De Paris"
    assert json_response["message"] == "OK"
