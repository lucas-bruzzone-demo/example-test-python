import pytest
import json
from app import app, Calculator

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def calculator():
    return Calculator()

class TestCalculator:
    """Testes para a classe Calculator"""
    
    def test_add(self, calculator):
        assert calculator.add(2, 3) == 5
        assert calculator.add(-1, 1) == 0
        assert calculator.add(0, 0) == 0
    
    def test_subtract(self, calculator):
        assert calculator.subtract(5, 3) == 2
        assert calculator.subtract(0, 5) == -5
        assert calculator.subtract(-1, -1) == 0
    
    def test_multiply(self, calculator):
        assert calculator.multiply(3, 4) == 12
        assert calculator.multiply(-2, 3) == -6
        assert calculator.multiply(0, 100) == 0
    
    def test_divide(self, calculator):
        assert calculator.divide(10, 2) == 5
        assert calculator.divide(7, 2) == 3.5
        assert calculator.divide(-6, 3) == -2
    
    def test_divide_by_zero(self, calculator):
        with pytest.raises(ValueError, match="Divisão por zero não é permitida"):
            calculator.divide(5, 0)

class TestRoutes:
    """Testes para as rotas da aplicação"""
    
    def test_home_route(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert 'Demonstração Flask' in response.data.decode('utf-8')
    
    def test_about_route(self, client):
        response = client.get('/about')
        assert response.status_code == 200
        assert 'Sobre esta aplicação' in response.data.decode('utf-8')
    
    def test_health_route(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['app'] == 'Flask Demo'

class TestCalculateEndpoint:
    """Testes para o endpoint de cálculo"""
    
    def test_calculate_add(self, client):
        response = client.post('/calculate', 
                             json={'operation': 'add', 'num1': 5, 'num2': 3})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 8
    
    def test_calculate_subtract(self, client):
        response = client.post('/calculate', 
                             json={'operation': 'subtract', 'num1': 10, 'num2': 4})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 6
    
    def test_calculate_multiply(self, client):
        response = client.post('/calculate', 
                             json={'operation': 'multiply', 'num1': 3, 'num2': 7})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 21
    
    def test_calculate_divide(self, client):
        response = client.post('/calculate', 
                             json={'operation': 'divide', 'num1': 15, 'num2': 3})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 5
    
    def test_calculate_divide_by_zero(self, client):
        response = client.post('/calculate', 
                             json={'operation': 'divide', 'num1': 5, 'num2': 0})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Divisão por zero' in data['error']
    
    def test_calculate_invalid_operation(self, client):
        response = client.post('/calculate', 
                             json={'operation': 'invalid', 'num1': 5, 'num2': 3})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Operação inválida' in data['error']
    
    def test_calculate_missing_data(self, client):
        response = client.post('/calculate', json={})
        assert response.status_code == 400
    
    def test_calculate_invalid_json(self, client):
        response = client.post('/calculate', 
                             data='invalid json', 
                             content_type='application/json')
        assert response.status_code == 500

class TestEdgeCases:
    """Testes para casos extremos"""
    
    def test_large_numbers(self, client):
        response = client.post('/calculate', 
                             json={'operation': 'add', 'num1': 999999, 'num2': 1})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 1000000
    
    def test_decimal_numbers(self, client):
        response = client.post('/calculate', 
                             json={'operation': 'multiply', 'num1': 2.5, 'num2': 4})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == 10.0
    
    def test_negative_numbers(self, client):
        response = client.post('/calculate', 
                             json={'operation': 'add', 'num1': -5, 'num2': -3})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == -8