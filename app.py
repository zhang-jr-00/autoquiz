from flask import Flask
from autoquiz.extensions import db
from autoquiz.routes import register_routes
from dotenv import load_dotenv
import os

def create_app(testing=False):
    """Application factory pattern"""
    # Load environment variables
    load_dotenv()
    
    # Initialize Flask app
    app = Flask(__name__)
    
    # Configure the app to use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///autoquiz.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Register API routes with Swagger
    register_routes(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)