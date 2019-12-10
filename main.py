from flask import Flask, render_template,request
from defectos import get_objetos
import pickle
import os
app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route("/upload-image",methods=["POST"])
def subir():
    if request.method == "POST":
        # print("here22")
        # print(request.files)
        if request.files:
            # print("here")

            spec = request.files["spec"]
            impl = request.files["impl"]
            nombre = request.values["nombre"]

            spec_str = os.path.join("uploads", "spec_" + nombre + spec.filename[-4:])
            impl_str = os.path.join("uploads", "impl_" + nombre + impl.filename[-4:]) 

            spec.save(spec_str)
            impl.save(impl_str)

            objetos,cajas_impl,cajas_spec = get_objetos(spec_str,impl_str,nombre)
            with open("dump.pkl","wb+") as dp:
                pickle.dump( (objetos,cajas_impl,cajas_spec,nombre),dp)
                return render_template('index.html',objetos=objetos,folder=nombre)

    return "No se cargaron los archivos correctamente ?"     



@app.route('/demo')
def hello_world():
    objetos,cajas_impl,cajas_spec = get_objetos("mora_impl.png","mora_spec.png","mora")
    with open("dump.pkl","wb+") as dp:
        pickle.dump( (objetos,cajas_impl,cajas_spec,"mora"),dp)

    return render_template('index.html',objetos=objetos,folder="mora")

@app.route('/view/<defecto>')
def show_defecto(defecto):
    objetos,cajas_impl,cajas_spec = (None,None,None)
    with open("dump.pkl","rb") as dp:
        objetos,cajas_impl,cajas_spec ,folder = pickle.load(dp)
    
        dato = objetos[int(defecto)]
        impl_b = cajas_impl[int(defecto)]
        spec_b = cajas_spec[dato[1]]

    return render_template('defecto.html',defecto=defecto, dato=dato , impl_b = impl_b , spec_b = spec_b ,folder=folder )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


