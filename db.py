import sqlite3
import os

class DB(object):
	def __init__(self, file, init=False):
		self.file = file
		k = not os.path.exists(self.file)
		if k:	
			open(self.file, 'a').close()
		self.conn = sqlite3.connect(self.file, check_same_thread=False)
		self.c    = self.conn.cursor()

		if k:
			self._init()

	def _init(self):
		self.c.execute('''CREATE TABLE folders
					  (token text, files text)''')
		self.conn.commit()

	def register_token(self, token):
		files = ''
		self.c.execute('SELECT * FROM folders WHERE token=?', (token,))
		if not self.c.fetchone():
			self.c.execute('INSERT INTO folders values (?,?)', (token, files))
			self.conn.commit()
			return True
		return False

	def add_file(self, token, hash):
		self.c.execute('SELECT * FROM folders WHERE token=?',(token,))
		x=self.c.fetchone()

		if x:
			cur = x[-1]
			if hash not in cur:
				cur += '{}|'.format(hash)

				self.c.execute('UPDATE folders SET files=? WHERE token=?', (cur,token))
			self.conn.commit()

	def get_files(self, token):
		self.c.execute('SELECT * FROM folders WHERE token=?',(token,))
		x=self.c.fetchone()
		if x:
			if x[-1]:
				return {'files': [i for i in x[-1][:-1].split('|')], 'status': 0}
			return {'files': [], 'status': 0}
		return {'status': 1}

	def check_token(self, token):
		self.c.execute('SELECT * FROM folders WHERE token=?',(token,))
		x=self.c.fetchone()

		if not x:
			return True
		return False

