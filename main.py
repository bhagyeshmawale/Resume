from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
# from flask_mail import Mail



with open('config.json','r') as c:
	params=json.load(c)["params"]

local_Server = True

app = Flask (__name__)


# app.config.update(
# 	MAIL_SERVER = 'smtp.gmail.com',
# 	MAIL_PORT = '465',
# 	MAIL_USE_SSL = True,
# 	MAIL_USERNAME = params["gmail-user"] ,
# 	MAIL_PASSWORD = params["gmail-password"]

# 	)

# mail = Mail(app)

if (local_Server):
	app.config ['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/bhagyesh"
else:
	app.config ['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/bhagyesh"


db = SQLAlchemy(app)

class Contacts(db.Model):
   sno = db.Column( db.Integer, primary_key = True)
   name = db.Column(db.String(50),nullable=False)
   phone = db.Column(db.String(500),nullable=False)  
   message = db.Column(db.String(500),nullable=False)
   date = db.Column(db.String(12),nullable=False)
   email = db.Column(db.String(10),nullable=False)


@app.route("/")
def about():
	return render_template('index.html')


@app.route("/",methods = ['POST', 'GET'])
def contact():
	if request.method == 'POST':
		name = request.form.get('name')
		phone = request.form.get('phone')
		message = request.form.get('message')
		date = request.form.get('date')
		email = request.form.get('email')

		entry = Contacts(name = name ,phone = phone,message = message,date=datetime.now(),email=email)
		db.session.add(entry)
		db.session.commit()
		mail.send_message("New Message from " + name,sender = email,
			recipients = [params['gmail-user']],
			body = message + "\n" + phone +"\n" + name

			)


	return render_template('index.html',params = params)

app.run()