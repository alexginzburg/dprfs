#!/usr/bin/env python

import os
import sys
import hashlib
import ConfigParser
import xattr
import binascii

config = ConfigParser.ConfigParser()
config.read( 'server.conf' )

buffer_size	= config.getint( 'general', 'buffer_size' )
meta_root	= config.get( 'status', 'meta_root' )
data_root	= config.get( 'data', 'data_root' )


def _write( fd ):

# meta_root/<file_name>/{base,top}
# the data chunk has an attribute with
#	previous
#   and next
# data chunk hashes

	chunk = binascii.a2b_base64( fd['r']['data'] )
	try:
		previous = fd['r']['prev']
	except KeyError, ex:
		previous = 'none'

	top = fd['r']['top']

	filename = fd['fn']

	path = "%s/%s" % ( meta_root, filename )
	try:
	  os.mkdir(path)
	except os.error, ex:
	  pass

	if top:
		link_name = os.path.join( path, 'top' )
		try:
			os.symlink(
				top,
				link_name
			)
		except os.error, ex:
			pass

		return {
			'base': top,
			'fn':	fd['fn'],
		}

	current = hashlib.sha1(chunk).hexdigest()
	dirname = os.path.join( data_root, current[:4] )
	try:
	  os.mkdir(dirname)
	except os.error, ex:
	  pass

	filename = os.path.join( dirname, current )
	df = open(filename, "wb")
	print >> df, chunk,
	df.close()
	if previous:
		xattr.setxattr( os.path.join(
				data_root,
				previous[:4],
				previous
			),
			'dprfs.next',
			current
		)
	
	link_name = os.path.join( path, 'base' )
	try:
		os.symlink( current, link_name )
	except os.error, ex:
		pass

	return {
		'base': current,
		'fn':	fd['fn'],
	}
