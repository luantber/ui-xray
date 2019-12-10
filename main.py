from flask import Flask, render_template
from defectos import get_objetos
import pickle

app = Flask(__name__)

@app.route('/')
def hello_world():
    objetos,cajas_impl,cajas_spec = get_objetos("mora_impl.png","mora_spec.png","mora")
    with open("dump.pkl","wb+") as dp:
        pickle.dump( (objetos,cajas_impl,cajas_spec),dp)

    return render_template('index.html',objetos=objetos)

@app.route('/view/<defecto>')
def show_defecto(defecto):
    objetos,cajas_impl,cajas_spec = (None,None,None)
    with open("dump.pkl","rb") as dp:
        objetos,cajas_impl,cajas_spec  = pickle.load(dp)
    
        dato = objetos[int(defecto)]
        impl_b = cajas_impl[int(defecto)]
        spec_b = cajas_spec[dato[1]]

    return render_template('defecto.html',defecto=defecto, dato=dato , impl_b = impl_b , spec_b = spec_b  )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


