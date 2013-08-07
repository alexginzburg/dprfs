import os
import sys
import ConfigParser

config = ConfigParser.ConfigParser()
config.read( 'server.conf' )

meta_root	= config.get( 'status', 'meta_root' )

def _open( fd ):

	filename = fd['fn']
	r = None

	try:
		os.chdir(os.path.join(meta_root, filename))
		r = {
			'base': os.readlink('base'),
			'top':	os.readlink('top'),
			'fn':	filename,
		}
	except Exception, ex:
		r = {
			'id':	None,
			'fn':	filename,
		}
	return r
