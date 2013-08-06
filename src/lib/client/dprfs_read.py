import sys
import socket
import json
import time
import uuid
import ConfigParser

config = ConfigParser.ConfigParser()
config.read( 'client.conf' )

network_address	= config.get( 'client', 'network_address' )
network_port	= config.getint( 'client', 'network_port' )
status_timeout	= config.getfloat( 'client', 'status_timeout' )
data_timeout	= config.getfloat( 'client', 'data_timeout' )
buffer_size	= config.getint( 'client', 'buffer_size' )


def dprfs_read ( s, fd ):

	fn = fd.get('fn', None)
	if not fn:
		fn = fd['r'].get('fn', None)

	host = fd['h'][0]
	port = fd['h'][1]

	fd = {
		'id':	uuid.uuid4().hex,
		'cmd':	'read',
		'h':	( host, port ),
		'r':	{
		  'next':	fd['r']['next'],
		  'fn':		fn,
		}
	}

	print >> sys.stderr, "=== %s out='%s'" % ( __name__, json.dumps(fd) )

	s.settimeout( data_timeout )

	s.sendto( json.dumps(fd), ( host, port ) )

	start = time.time()
	try:
		msg_in, sender_addr = s.recvfrom( buffer_size * 2 )
		s.settimeout( 0 )
	except socket.timeout, ex:
		print >> sys.stderr, "=== socket.timeout '%s'" % ex
		return None
	
	return json.loads(msg_in)
