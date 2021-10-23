import os
from flask import Flask

def create_app (test_config=None): #app factory function - handles config, regis, and setup, then returns the app **READ MORE LATER
    #create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping( #sets some default config
        SECRET_KEY = 'dev', #used by Flask to keep data sade **SET TO RANDOM VALUE WHEN DEPLOYING
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'), #path where SQLite db will be saved **for now it's in instance folder
    )

    if test_config is None:
        # Load the instance config, if it exists, whennot testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        #Load the test config if passed in
        app.config.from_mapping(test_config) #used instead of instance config
    
    try:
        os.makedirs(app.instance_path) #ensures instance_path exists **FLASK doesnt create instance folder automatically!!!!
    except OSError:
        pass

    #a page that says get a job
    @app.route('/jawb')
    def jawb():
        return 'Get a jawb foo!'

    #wow route makes things easy fo sure
    @app.route('/hello')
    def hello():
        return 'Hello there!'
    
    from . import db #from flaskr import db script
    db.init_app(app) #pass app as args

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index') #READ MORE about endpoints and URLs

    return app
