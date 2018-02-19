from flask import Flask, request, flash, session, render_template
from datetime import timedelta
import bd
import calc


app = Flask(__name__)
"""
La Interfaz es bastante sencilla, es una sola ruta, la cual a medida que se
hacen operaciones se refresca e imprime la sesion entera sobre la cual esta
trabajando. Cuando se limpia se borra la sesion, cuando se guarda se almacena
la sesion en una base de datos, y por ultimo cuando se recupera se trae la
sesion desde la base de datos.
La aplicacion en si parsea el input y se fija que comando se ingreso,
si para guardar, recuperar o limpiar. Si no es ninguno de esto se manda el
comando a to_rpn para ser convertido a RPN y luego a calculate para ser
calculado el resultado, si hubiese un error en este punto significa que el
comando esta mal redactado, entonces se imprime un Alert para hacercelo saber
al usuario
"""

@app.route('/')
def my_form():
    return render_template("my-form.html")

@app.route('/', methods=['POST'])
def my_form_post():
    command = request.form['command']
    if command.startswith("guardar "):
        commandlist = command.split(' ')
        if len(commandlist)==2:
            name = commandlist[1]
            if database.add_bd(name, session['calculos']):
                flash("Sesion guardada")
            else:
                flash("Nombre ya existente, Pruebe con otro")
        else:
            flash("Comando invalido, intentelo de nuevo")
    elif command.startswith("recuperar "):
        commandlist = command.split(' ')
        if len(commandlist)==2:
            name = commandlist[1]
            if database.from_bd(name) == "":
                flash("sesion no registrada con ese nombre")
            else:
                session['calculos'] = database.from_bd(name)
        else:
            flash("Comando invalido, intentelo de nuevo")
    elif command == "limpiar":
        session['calculos'] = ""
    else:
        try:
            calculadora = calc.Calculator(command)
            rpn = calculadora.to_rpn()
            resultado = str(calculadora.calculate())
            session['calculos'] += command + " = " + resultado + "\n"
        except Exception:
            flash("Comando invalido, intentelo de nuevo")
    strs = session['calculos']
    return render_template("my-form.html", session_var=strs)


if __name__ == '__main__':
    database = bd.database()
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
    app.debug = True
