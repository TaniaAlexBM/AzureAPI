from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# limita las peticiones al servidor para que no truene

# Sólo permite una solicitud por día
@app.route("/slow")
@limiter.limit("1 per day")
def slow():
    return ":("

# Sólo permite una solicitud por segundo
@app.route("/medium")
@limiter.limit("1/second", override_defaults=False)
def medium():
    return ":|"

@app.route("/fast")
def fast():
    return ":)"

@app.route("/ping")
@limiter.exempt
def ping():
    return "PONG"

# Actualiza automáticamente el servidor con los cambios
# Sólo se usa en desarrollo con True
# En producción se declara con False
if __name__ == '__main__':
    app.run(debug=True)