from crypto import hash_file
import threading
import requests
import ipfshttpclient
import json
import time
import sys
import os

config_file = 'config.json'
SERVER = 'http://127.0.0.1:5000/'
TOKEN_PATH = '/home/karu/hackathon/tokens/'

config = json.load(open(config_file, 'r'))
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')

tokens = config['tokens']

def list_files():
	files = os.listdir()
	d={}
	for f in files:
		d[hash_file(f)] = f
	return d

def diff_files(l1, l2):
	x=[]
	for i in l1:
		k=i.split('+')
		if k[0] not in l2:
			x.append(k[1]+'|'+k[2])
	y=[]
	for i in l2:
		if i not in [i.split('+')[0] for i in l1]:
			y.append(i)
	return x,y

def manage_token(token):
	if not os.path.exists(TOKEN_PATH+token):
		os.mkdir(TOKEN_PATH+token)

	os.chdir(TOKEN_PATH+token)
	
	while True:
		local_files = list_files()
		files = requests.get(SERVER+'get_files', params={'token': token}).json()
		if files['status'] == 1:
			print('no such token .... ' + token)
			sys.exit(1)

		new_files, n_local = diff_files(files['files'], [i for i in local_files.keys()])
		for i in new_files:
			h,f = i.split('|')
			tmp=client.get(h)
			os.rename(h,f)

		for i in n_local:
			h=client.add(local_files[i])['Hash']
			requests.post(SERVER+'add_file', data={'token': token, 'hash': i+'+'+h+'+'+local_files[i]})

		time.sleep(1)

for i in tokens:
	threading.Thread(target=manage_token, args=(i,)).start()