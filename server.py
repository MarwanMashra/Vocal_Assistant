from flask import Flask
import pprint,json
from os.path import join,dirname
from sys import platform

path_volume= abspath(__file__)+"_data/"

#créer une application flask    
app= Flask(__name__)
app.config.from_mapping(SECRET_KEY='mysecret')

#importer l'application Webservice dans app
app.register_blueprint(Webservice)

if __name__ == '__main__' :
    #démarer app via WSGI
    with make_server('127.0.0.1',5000,app) as server:   
        if(platform.startswith('win')):
            print("Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)")
        else:
            print("Running on http://127.0.0.1:5000/ (Press CTRL+Z to quit)")
        server.serve_forever()

        
        