from flask import Flask, request, jsonify
import os
import speech_recognition as sr
from sys import platform
from playsound import playsound
from utils import *
from wsgiref.simple_server import make_server 



if get_os()=="pi":
	from ctypes import *
	# Define our error handler type
	ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
	def py_error_handler(filename, line, function, err, fmt):
		return
	c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

	asound = cdll.LoadLibrary('libasound.so')
	# Set error handler
	asound.snd_lib_error_set_handler(c_error_handler)


path_volume= abspath(__file__)+"_data/"
start_rec_effect= path_volume+'effects/start_rec_effect.wav'
end_rec_effect= path_volume+'effects/end_rec_effect.wav'

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
	play_effect= str_to_bool(str(request.args.get('play_effect')))

	if os.path.exists(path_volume+file_name):
		os.remove(path_volume+file_name)

	try: 
		# print(sr.Microphone.list_microphone_names())
		r = sr.Recognizer()
		mic = sr.Microphone()
		with mic as source:
			# start recording voice
			if play_effect and os.path.isfile(start_rec_effect):
				playsound(start_rec_effect)
			print("##### start #####")
			audio = r.listen(source)
			print("###### end ######")
			if play_effect and os.path.isfile(end_rec_effect):
				playsound(end_rec_effect)
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
        
        