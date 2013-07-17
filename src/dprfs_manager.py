#!/usr/bin/env python

import os
import sys

# read the configuration to find out
 1. how many services need to be managed
 2. what concurrency level it needs to be at

concurrency = os.ENVIRON.get( 'dprfs_concurrency', 1 )
concurrency = os.ENVIRON.get( 'dprfs_concurrency', 1 )
concurrency = os.ENVIRON.get( 'dprfs_concurrency', 1 )

# spawn a asked number of processes for each service
# record pid+service name combination
# restart service if it died
# restart specific services when asked
#  ex. dprfs_manager service <fsync_manager> restart
