
from flask import Flask, render_template, request
from src.calculator import add, subtract, multiply, divide

app = Flask(__name__)

OPERATIONS = {
    'add': add,
    'subtract': subtract,
    'multiply': multiply,
    'divide': divide
}


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    operation_label = None

    if request.method == 'POST':
        try:
            type = request.form.get('type')
            num1 = float(request.form.get('num1'))
            num2 = float(request.form.get('num2'))
            
            if type == 'add':
                result = add(num1, num2)
            elif type == 'subtract':
                result = subtract(num1, num2)
            elif type == 'multiply':
                result = multiply(num1, num2)
            elif type == 'divide':
                result = divide(num1, num2)

        except ValueError:
            result = "Invalid input"


    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
