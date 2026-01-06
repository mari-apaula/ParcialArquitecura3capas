# app.py (Actualizar)
from flask import Flask
from presentation.routes import web_bp

app = Flask(__name__)
app.secret_key = 'super_secreto_examen' # Necesario para session

app.register_blueprint(web_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)