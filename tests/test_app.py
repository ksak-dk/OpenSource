import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Recipe" in response.data  # 检查页面包含“Recipe”字样，具体可按实际填

def test_add_recipe(client):
    data = {
        "title": "蛋炒饭",
        "ingredients": "蛋, 米饭",
        "instructions": "炒熟"
    }
    response = client.post('/add', data=data, follow_redirects=True)
    assert response.status_code == 200 or response.status_code == 302
    assert b'蛋炒饭' in response.data  # 假设添加后自动跳转展示  

    def test_recipe_detail(client):
        # 首先添加一条食谱
        data = {
            "title": "番茄炒蛋",
            "ingredients": "鸡蛋, 番茄",
            "instructions": "炒"
        }
        client.post('/add', data=data)
        # 假设详情页 id 从 1 开始
        response = client.get('/recipe/1')
        assert response.status_code == 200
        assert b'番茄炒蛋' in response.data