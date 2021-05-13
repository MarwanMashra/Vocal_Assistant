from flask import Flask, request, jsonify
import os
import speech_recognition as sr
from sys import platform
from playsound import playsound
from utils import *
from wsgiref.simple_server import make_server 

path_volume= abspath(__file__)+"_data/"

#créer une application flask    
app= Flask(__name__)
app.config.from_mapping(SECRET_KEY='mysecret')

@app.route('/',methods=['POST', 'GET'])
def index():
	return jsonify(volume_content=os.listdir(path_volume))


@app.route('/test',methods=['POST', 'GET'])
def test():
	return "ceci est un test"

@app.route('/playsound',methods=['POST', 'GET'])
def play():
	# get data sent with the request
	_file= str(request.args.get('file'))
	try: 
		playsound(path_volume+_file)
	except Exception as error:
		return jsonify(status="fail",error=str(error))
	return jsonify(status="succes")


@app.route('/microphone',methods=['POST', 'GET'])
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
		with open(path_volume+file_name, "wb") as f:
			f.write(audio.get_wav_data())     
			
	except Exception as error:
		return jsonify(status="fail",error=str(error))
	return jsonify(status="succes")


def run_server():
    #démarer app via WSGI
    with make_server('127.0.0.1',5000,app) as server:   
        server.serve_forever()

if __name__ == '__main__':
	#démarer app via WSGI
    with make_server('127.0.0.1',5000,app) as server:   
        if(platform.startswith('win')):
            print("Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)")
        else:
            print("Running on http://127.0.0.1:5000/ (Press CTRL+Z to quit)")
        server.serve_forever()
        
        