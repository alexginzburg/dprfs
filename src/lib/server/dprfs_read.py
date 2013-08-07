import os
import sys
import json
import ConfigParser
import xattr
import binascii

config = ConfigParser.ConfigParser()
config.read( 'server.conf' )

buffer_size	= config.getint( 'general', 'buffer_size' )
meta_root	= config.get( 'status', 'meta_root' )
data_root	= config.get( 'data', 'data_root' )

def _read( fd ):
	request = fd['r']['next']
	filename = fd['r']['fn']

	base = os.path.join(
		meta_root,
		filename,
		'base'
	)
	c = {
		'base': os.readlink('base'),
		'top':	os.readlink('top'),
		'data':	None,
		'next':	None,
		'fn':	fd['r']['fn'],
	} 

	if request is None:
		return c
	
	filename = os.path.join( data_root, request[:4], request ) 
	df = open(filename, "rb")
	data = []
	chunk = df.read( buffer_size * 2 )
	c['data'] = binascii.b2a_base64( chunk )
	try:
		c['next'] = xattr.getxattr(df, 'dprfs.next')
	except KeyError, ex:
		c['next'] = None

	finally:
		df.close()

	return c
