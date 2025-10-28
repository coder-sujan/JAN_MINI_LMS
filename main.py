from flask import Flask

from init import db
import os
# from dotenv import load_dotenv

# load_dotenv()

#run developmnet phase 


def create_app(developmnet):
    app = Flask(__name__)
    print("Flask Server Started.")
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    #or
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
    
    
    db.init_app(app)
    return app




#testing phase



#deploymnet phase


