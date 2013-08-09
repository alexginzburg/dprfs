import os
import sys
import json
import ConfigParser
import xattr
import binascii

config = ConfigParser.ConfigParser()
config.read( 'server.conf' )

buffer_size	= config.getint( 'general', 'buffer_size' )
data_root	= config.get( 'data', 'data_root' )

def _read( fd ):

	r = fd['r']
	request = r.get( 'request', None )
	filename = r.get( 'fn', None )

	step = skip = r.get( 'step', 1 )

	c = {
		'data':	None,
		'next':	None,
		'fn':	fd['r']['fn'],
	} 

	if request is None:
		return c

	dprfs_next = []
	
	while step and skip:

		if skip > 0:
			skip -= 1

		filename = os.path.join( data_root, request[:4], request ) 

		if not skip:
			df = open(filename, "rb")
			data = []
			chunk = df.read( buffer_size * 2 )
			c['data'] = binascii.b2a_base64( chunk )
			df.close()

		try:
			request = xattr.getxattr(filename, 'dprfs.next')
		except KeyError, ex:
			request = None
			break

		if not skip and step:
			dprfs_next.append( request )
			step -= 1

	c['next'] = dprfs_next

	return c
