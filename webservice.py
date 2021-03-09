from flask import Flask, Blueprint, render_template, request, jsonify, redirect, session, url_for
import pprint,json,os
import speech_recognition as sr
from playsound import playsound

VOLUME_PATH=os.getcwd()+"/_data/"

Webservice = Blueprint('Webservice',__name__)

@Webservice.route('/',methods=['POST', 'GET'])
@Webservice.route('/index',methods=['POST', 'GET'])
def index():
	return jsonify(val="val",xyz="xyz",num=5)

@Webservice.route('/playsound',methods=['POST', 'GET'])
def play():
	# get data sent with the request
	_file= str(request.args.get('file'))
	try: 
		playsound("_data/"+_file)
	except Exception as error:
		return jsonify(status="fail",error=str(error))
	return jsonify(status="succes")


@Webservice.route('/microphone',methods=['POST', 'GET'])
def microphone():
	# get data sent with the request
	file_name= str(request.args.get('file'))
	try: 
		r = sr.Recognizer()
		mic = sr.Microphone()
		with mic as source:
			# start recording voice
			print("##### start #####")
			audio = r.listen(source)
			print("###### end ######")
		# save audio file in format wav
		with open("_data/"+file_name, "wb") as f:
			f.write(audio.get_wav_data())     
			
	except Exception as error:
		return jsonify(status="fail",error=str(error))
	return jsonify(status="succes")


