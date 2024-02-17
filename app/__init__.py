from flask import Flask

def create_app(debug:bool = True, db_uri: str = "sqlite:///db.sqlite") -> Flask:

    #config 
    app = Flask(__name__, static_url_path="/")
    app.config["DEBUG"] = debug
    app.config["SECRET_KEY"] = "thisismyverysecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

    #extensions
    from app.extensions import db, jwt, bcrypt
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    #create database
    from app import models
    with app.app_context():
        db.create_all()
    
    #register blueprints
    from app.routes import routesBP
    app.register_blueprint(routesBP)

    return app