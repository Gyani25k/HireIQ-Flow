from flask import Flask,render_template,request,redirect,url_for,jsonify
from flask_cors import CORS
import datetime
import hashlib
import pymongo
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import pickle
import cv2
from datetime import datetime


app = Flask(__name__,template_folder="template")

CORS(app)

app.secret_key = 'HIREIQ@2023'



client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["HIREIQ"]
collection=db['USER_MASTER']
collection1=db['LOGIN_TRACK']
collection2=db['CONTACT_US']
