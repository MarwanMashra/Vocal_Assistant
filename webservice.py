from flask import Flask, Blueprint, render_template, request, jsonify, redirect, session, url_for
import pprint,json


Webservice = Blueprint('Webservice',__name__)

@Webservice.route('/')
def index():
	return "index"


