from hashlib import sha256
import base58

def hash(d):
	h = sha256()
	h.update(d)
	return h.hexdigest()

def hash_file(fname):
	with open(fname,'rb') as f:
		h = sha256()
		for chunk in iter(lambda: f.read(4096),b''):
			h.update(chunk)
	return h.hexdigest()
