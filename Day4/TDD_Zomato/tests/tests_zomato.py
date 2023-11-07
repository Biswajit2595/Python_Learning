import pytest
from project.zomato import app,menu,order
import json
@pytest.fixture

def client():
    # return app.test_client()
    app.config['TESTING'] = True
    client = app.test_client()
    yield client
    
def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b"Welcome to Zesty Zomato"

def test_get_menu_invalid(client):
    res=client.get("/menu/invalid")
    assert res.status_code==404
    data=json.loads(res.data)
    assert data['error']=="Item Not Found"

def test_delete_menu_invalid(client):
    res=client.get("/menu/invalid")
    assert res.status_code==404
    data=json.loads(res.data)
    assert data['error']=="Item Not Found"
    
def test_patch_order_status_invalid(client):
    status={'status':"ready"}
    res=client.patch("/order/103",json=status)
    assert res.status_code==404
    data=json.loads(res.data)
    assert data['msg']=="Order 103 not found"
    
def test_delete_order_invalid(client):
    res=client.delete("/order/100")
    assert res.status_code==404
    data=json.loads(res.data)
    assert data['msg']=="Order 100 not found"

def test_get_order_invalid(client):
    res=client.delete("/order/101")
    assert res.status_code==404
    data=json.loads(res.data)
    assert data['msg']=="Order 101 not found"

    
def test_get_menu(client):
    response = client.get('/menu')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert len(data)==len(menu)
    
def test_get_menu_valid(client):
    item="Veg Pakora"
    res=client.get(f'/menu/{item}')
    assert res.status_code==200
    data=json.loads(res.data)
    assert item in data
    assert data[item]=={"availability":True,"name":item,"price":50}

def test_post_menu(client):
    data={"name":"Chole Bhature","availability":True,"price":80}
    res=client.post("/menu",json=data)
    assert res.status_code==201
    data=json.loads(res.data)
    assert data['msg']=="New Item added"
    assert data['item']=={"name":"Chole Bhature","availability":True,"price":80}
    
def test_delete_menu(client):
    item="Chole Bhature"
    res=client.delete(f"/menu/{item}")
    assert res.status_code==200
    data=json.loads(res.data)
    assert data['msg']==f"{item} has been deleted"

def test_get_order(client):
    res=client.get("/order")
    assert res.status_code == 200
    data = json.loads(res.data.decode('utf-8'))
    assert len(data)==len(order)
    
def test_post_order(client):
    data={"name":"Biswa","items":[{"name":"Maggie","price":35}]}
    res=client.post("/order",json=data)
    assert res.status_code==201
    data=json.loads(res.data)
    assert data['msg']=="New order added"

def test_patch_order_status(client):
    status={'status':"ready"}
    res=client.patch("/order/3",json=status)
    assert res.status_code==200
    data=json.loads(res.data)
    assert data['msg']=="Order ID: 3 has been updated"

def test_get_order_single(client):
    res=client.get("/order/1")
    assert res.status_code == 200
    
def test_delete_order(client):
    res=client.delete("/order/1")
    assert res.status_code==200
    data=json.loads(res.data)
    assert data['msg']=="order ID:1 has been deleted"