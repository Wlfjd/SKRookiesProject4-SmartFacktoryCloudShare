from flask import Flask

def create_app():
    app = Flask(__name__)
    init_environment( app )
    init_blueprint( app )   

    return app
    
def init_environment( app ):
    app.config['SECRET_KEY']     = 'higaluctc4841'
    
def init_blueprint( app ):
    from controller import db_controller
    from controller import main_controller
    
    from controller import bp_db
    from controller import bp_main

    app.register_blueprint(bp_db)
    app.register_blueprint(bp_main)
