import sys
import socket
import json
import time
import uuid
import binascii
import ConfigParser

config = ConfigParser.ConfigParser()
config.read( 'client.conf' )

network_address	= config.get( 'client', 'network_address' )
network_port	= config.getint( 'client', 'network_port' )
status_timeout	= config.getfloat( 'client', 'status_timeout' )
data_timeout	= config.getfloat( 'client', 'data_timeout' )
buffer_size	= config.getint( 'client', 'buffer_size' )


def dprfs_write ( s, fd, sys_fd ):

	host = fd['h']['host']
	port = fd['h']['port']

	host = host.pop()
	port = port.pop()

	previous = None
	top = None

	while top is None:
		r = sys_fd.read( buffer_size )
		if r == '':
			top = previous

		r = binascii.b2a_base64( r )

		p = {
			'id':	uuid.uuid4().hex,
			'cmd':	'write',
			'fn':	fd['fn'],
			'r':	{
				'data': r,
				'prev': previous,
				'top':	top,
			},
		}

		s.settimeout( data_timeout )
		s.sendto( json.dumps(p), ( host, port ) )

		start = time.time()
		try:
			msg_in, sender_addr = s.recvfrom( buffer_size )
			s.settimeout( 0 )
			msg_in = json.loads( msg_in )
			if previous == msg_in['r']['base']:
				return None
			previous = msg_in['r']['base']
		except socket.timeout, ex:
			print >> sys.stderr, "=== %s socket.timeout '%s'" % ( __name, ex )
			return None
