# app/app.py
"""Módulo app.py"""

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from .calculadora import sumar, restar, multiplicar, dividir

load_dotenv()

app = Flask(__name__)
secret_key = os.getenv("SECRET_KEY")

app.config["SECRET_KEY"] = secret_key  # nosec

csrf = CSRFProtect(app)


def _resultado_from_post() -> str | float | None:
    """Calcular el resultado del form POST."""
    try:
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        operacion = request.form["operacion"]
        operaciones = {
            "sumar": sumar,
            "restar": restar,
            "multiplicar": multiplicar,
            "dividir": dividir,
        }
        funcion = operaciones.get(operacion)
        if funcion is None:
            return "Operación no válida"
        return funcion(num1, num2)
    except ValueError:
        return "Error: Introduce números válidos"
    except ZeroDivisionError:
        return "Error: No se puede dividir por cero"


@app.get("/")
def index_get():
    """Mostrar el formulario de la calculadora."""
    return render_template("index.html", resultado=None)


@app.post("/")
def index_post():
    """Procesar el envío del formulario y mostrar el resultado."""
    return render_template("index.html", resultado=_resultado_from_post())


if __name__ == "__main__":  # pragma: no cover
    debug_mode = os.getenv("FLASK_DEBUG", "False") == "True"

    app.run(debug=debug_mode, port=5000, host="127.0.0.1")
    # Quita debug=True para producción
