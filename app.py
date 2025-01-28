from flask import Flask
from models import db
from routes import api_bp
from routes import create_first_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance1.db'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_first_user()
    app.run(debug=True)

    
