#!/usr/bin/python

import MySQLdb
from optparse import OptionParser

def get_opts():
	"""
	Get the options from the command line params
	"""

	parser = OptionParser(usage="usage: %prog [options] hostname",version="%prog 0.0.1")
	parser.add_option("-c",dest="defaults_file", default='~/.my.cnf',help="local MySQL config file")
	parser.add_option("--execute",action="store_true", dest="execute", help="Execute the purge")
	parser.add_option("-m",dest="master", help="ip address of the master host to connect to")
	parser.add_option("-r",dest="replicas", help="ip address of the replicas host to connect to")
	(options, args) = parser.parse_args()

	return parser.parse_args()

def open_connect(server):
    """
    Open a mysql connection to the server passed into the function.

    @param server: hostname for the mysql connection
    """
    if options.defaults_file:
        conn = MySQLdb.connect(read_default_file = options.defaults_file, host = server)
    else:
        if options.prompt_password:
            password=getpass.getpass()
        else:
            password=options.password
        conn = MySQLdb.connect(
            host = server,
            user =  options.user,
            passwd = password,
            port = '3306',
			connection_timeout='10') # options.port,
            # unix_socket = options.socket)
    return conn;

def get_coordinates(server, role):

	conn = open_connect(server)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	if role == 'master':
		sql = "show binary logs"
	elif role == 'replica':
		sql = "show slave status"

	try:
		cursor.execute(sql)
		res = cursor.fetchall()
		if role == 'replica':
			relaylog = res[0]['Relay_Master_Log_File']
			return relaylog	
		else:
			master_status = res
			if not options.execute:
				print "Binary logs from Master: %s" %(server)
			
				for i in master_status:
					print "\t %s" %(i['Log_name'])
			
			return master_status

	except MySQLdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	
def master_log_purge(master, Log_name):
	conn = open_connect(master)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	sql = 'purge binary logs to "%s"' % (Log_name)
	try:
		cursor.execute(sql)
		print 'Binlogs purged up to %s' % (Log_name)
	except MySQLdb.Error, e:
		print "MySQL Error [%d]: %s" (e.args[0], e.args[1])
		sys.exit(1)

def main():
	global options

	(options, args) = get_opts()
	replica_files = []

	master = options.master
	master_status = get_coordinates(master,'master')

	if options.replicas:
		replicas = options.replicas.split(',')
		for replica in replicas:
			try:
				mfile = get_coordinates(replica,'replica')
				replica_files.append(mfile)
				if not options.execute:
					print "Replica: %s, File: %s" %(replica, mfile)
			except ValueError, e:
				print "error! %s" %(e)
		oldest_file = sorted(replica_files)[0]
		if not options.execute:
			print "Logs will be purged to %s. Supply --execute to perform the purge" %(oldest_file)
	else:
		print "no replica supplied, no purge will be made"

	if options.execute:
		try:
			master_log_purge(master, oldest_file)
		except ValueError, e:
			print "error! %s" %(e)

if __name__ == '__main__':
	main()