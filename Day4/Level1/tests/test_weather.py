import pytest
import json
from project.weather import app
@pytest.fixture
def client():
    return app.test_client()

def test_get_all(client):
    res=client.get("/get")
    assert res.status_code==200
    data=json.loads(res.data)
    assert len(data)==5
    
def test_get_weather_invalid(client):
    res=client.get('/weather/City')
    assert res.status_code==404
    data=json.loads(res.data)
    assert "error" in data
    assert data['error']=="City not found"
    
def test_get_weather_valid(client):
    city='Austin'
    res=client.get(f'weather/{city}')
    assert res.status_code==200
    data=json.loads(res.data)
    assert city in data
    assert data[city]=={'temperature':32,'weather':"Hot"}
    
def test_post_weather(client):
    new_city={'city':'Chicago','temperature':20,'weather':'Cloudy'}
    res=client.post('/weather/',json=new_city)
    assert res.status_code==201
    data=json.loads(res.data)
    assert data['city']==new_city['city']
    assert data['data']=={'temperature':20,'weather':'Cloudy'}
    
def test_put_city_invalid(client):
    city="Nevada"
    new_data={'temperature':37,'weather':'Hot'}
    res=client.put(f'/weather/{city}',json=new_data)
    assert res.status_code==404
    data=json.loads(res.data)
    assert data['error']=="City not found"
    
def test_put_city_valid(client):
    city='Austin'
    new_data={'temperature':15,'weather':'Partly Cloudy'}
    res=client.put(f'/weather/{city}',json=new_data)
    assert res.status_code==201
    data=json.loads(res.data)
    assert data['city']==city
    assert data['data']=={'temperature':15,'weather':'Partly Cloudy'}
    
def test_delete_city_invalid(client):
    city="Texas"
    res=client.delete(f'/weather/{city}')
    assert res.status_code==404
    data=json.loads(res.data)
    assert 'error' in data
    assert data['error']=="City not found"
    
def test_delete_city_valid(client):
    city='Austin'
    res=client.delete(f'/weather/{city}')
    assert res.status_code==200
    data=json.loads(res.data)
    assert data['data']=="City has been deleted"