from flask import Flask, Blueprint, render_template, request, jsonify, redirect, session, url_for
import pprint,json,os

from playsound import playsound

VOLUME_PATH=os.getcwd()+"/_data/"

Webservice = Blueprint('Webservice',__name__)

@Webservice.route('/',methods=['POST', 'GET'])
@Webservice.route('/index',methods=['POST', 'GET'])
def index():
	return jsonify(val="val",xyz="xyz",num=5)

@Webservice.route('/playsound',methods=['POST', 'GET'])
def play():
	_file= str(request.args.get('file'))
	try: 
		playsound("_data/"+_file)
	except Exception as error:
		return jsonify(status="fail",error=str(error))
	return jsonify(status="succes")


