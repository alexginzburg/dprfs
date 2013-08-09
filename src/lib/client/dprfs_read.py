import sys
import socket
import errno
import json
import time
import uuid
import random
import binascii
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

	h = fd['h']
	idx = random.randint( 0, len(h['host'])-1 )
	host = h['host'].pop(idx)
	request = fd['r']['next']
	if not isinstance( request, list ):
		request = [request]

	r_count = 0
	request_accounting = {}
	for r_chunk in request:
		fd = {
			'id':	uuid.uuid4().hex,
			'cmd':	'read',
			'h':	{
				'host': host,
			},
			'r':	{
			  'request':	r_chunk,
			  'fn':		fn,
			}
		}
		request_accounting[ fd['id'] ] = r_count
		r_count += 1

		s.sendto( json.dumps(fd), ( host, network_port ) )

	data = []
	while r_count:
		try:
			msg_in, sender_addr = s.recvfrom( buffer_size * 2 )
		except socket.error, ex:
			if ex.errno == errno.EAGAIN:
				continue
			else:
				break
		msg_in = json.loads(msg_in)
		idx = request_accounting[ msg_in['id'] ]
		data.insert( idx, binascii.a2b_base64( msg_in['r']['data'] ) )
		r_count -= 1
	
	msg_in['r']['data'] = binascii.b2a_base64( ''.join( data ) )
	msg_in['h'] = {
		'host': [host],
	}

	return msg_in
