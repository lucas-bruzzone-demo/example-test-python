from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

class Calculator:
    """Classe simples para demonstrar testes de coverage"""
    
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Divisão por zero não é permitida")
        return a / b

calculator = Calculator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        operation = data.get('operation')
        num1 = float(data.get('num1', 0))
        num2 = float(data.get('num2', 0))
        
        if operation == 'add':
            result = calculator.add(num1, num2)
        elif operation == 'subtract':
            result = calculator.subtract(num1, num2)
        elif operation == 'multiply':
            result = calculator.multiply(num1, num2)
        elif operation == 'divide':
            result = calculator.divide(num1, num2)
        else:
            return jsonify({'error': 'Operação inválida'}), 400
        
        return jsonify({'result': result})
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno'}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'app': 'Flask Demo'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)