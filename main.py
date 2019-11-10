from flask import Flask, render_template, request, send_from_directory
from db import DB
import os

app = Flask(__name__)
DataBase = DB('db')

#DataBase.register_token('oi')
#DataBase.check_token('oi')
#DataBase.add_file('oi', 'x+c')
#print(DataBase.get_files('oi'))

@app.route('/register', methods=['POST'])
def register():
	token = request.form['token']
	if DataBase.check_token(token):
		DataBase.add_token(token)
		return {'status': 0}
	return {'status': 1}

@app.route('/add_file', methods=['POST'])
def add_file():
	token = request.form['token']
	_hash = request.form['hash']
	if not DataBase.check_token(token):
		DataBase.add_file(token, _hash)
		return {'status': 0}
	return {'status': 1}

@app.route('/get_files', methods=['GET'])
def get_files():
	token = request.args.get('token')
	if not DataBase.check_token(token):
		return DataBase.get_files(token)
	return {'status': 1}

if __name__ == '__main__':
	app.run()