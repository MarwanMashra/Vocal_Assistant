from flask import Flask, Blueprint, render_template, request, jsonify, redirect, session, url_for
import pprint,json


Webservice = Blueprint('url',__name__)

@Webservice.route('/')
def index():
	return "index"


