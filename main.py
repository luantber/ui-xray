from flask import Flask, render_template
from detect import detect
app = Flask(__name__)

@app.route('/')
def hello_world():
    cajas = detect("static/demo/1.png","static/demo/1_i.png")
    return render_template('index.html',cajas=cajas)

@app.route('/view/<defecto>')
def show_defecto(defecto):
    return render_template('defecto.html',defecto=defecto)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')