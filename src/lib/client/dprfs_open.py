import sys
import socket
import json
import time
import uuid
import hashlib
import ConfigParser

config = ConfigParser.ConfigParser()
config.read( 'client.conf' )

network_address	= config.get( 'client', 'network_address' )
network_port	= config.getint( 'client', 'network_port' )
status_timeout	= config.getfloat( 'client', 'status_timeout' )
data_timeout	= config.getfloat( 'client', 'data_timeout' )
buffer_size	= config.getint( 'client', 'buffer_size' )

def dprfs_open( s, filename ):

	id = uuid.uuid4().hex
	
	message = {
		'id':	id,
		'cmd':	'open',
		'fn':	filename,
	}
	msg = {
		'id':	id,
		'fn':	filename,
		'h':	[],
		'r':	{
		   'base':	None,
		   'top':	None, 
		}
	}

	print "=== %s msg_out='%s'" % ( __name__, message )
	sent = s.sendto( json.dumps(message), ( network_address, network_port ) )
	s.settimeout( status_timeout )
	start = time.time()

	while True:
		try:
			msg_in, sender_addr = s.recvfrom( buffer_size * 2 )
			msg_in = json.loads(msg_in)
			if msg['id'] == msg_in['id']:
				msg['id'] = msg_in['id']
				msg['fn'] = msg_in['r']['fn']
				if msg['r']['top'] is None:
					msg['r']['base'] = msg_in['r']['base']
					msg['r']['top'] = msg_in['r']['top']
				if msg['r']['top'] == msg_in['r']['top']:
					#host = msg['h']
					#host.append( msg_in['h'] )
					msg['h'] = msg_in['h']
				
			
		except socket.timeout, ex:
			print >> sys.stderr, "socket.timeout %s" % ex
			s.settimeout( 0 )
			break
	print "=== %s msg='%s'" % ( __name__, msg )

	return json.dumps(msg)
