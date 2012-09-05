#!/usr/bin/env python
"""
    Ibervicis Furnivall is an open source framework for distributed user science.
    It helps to organize batches of tasks, collect them form users and do all the related housekeeping.

"""
import os, sys
import tornado.httpserver, tornado.database, tornado.ioloop, tornado.web
from tornado.options import define, options
from pymongo import Connection
from yapsy.PluginManager import PluginManager
from libs.route import Route
from Furnivall import data_dir
from Furnivall.Core.handlers import *
from Furnivall.Core.handlers.api import *

# import daemon

# Default options for the server
define("port", default=8888, help="run on the given port", type=int)
define("daemonize", default=False, help="Run as daemon")

class FurnivallApplication(tornado.web.Application):
	def __init__(self):
		"""
		Sets up the Tornado web server and loads all the init data
		"""

		# Init mongodb database
		self.dbconnection = Connection()
		self.db = self.dbconnection['furnivall']

		# Init plugins
		self.plugin_manager = PluginManager()
		self.plugin_manager.setPluginPlaces(["./plugins"])
		self.plugin_manager.collectPlugins()
		print self.plugin_manager.getAllPlugins()

		# Init routes
		urls = [
		] + Route.routes()

		settings = dict(
			static_path = os.path.join(data_dir, "static"),
			template_path = os.path.join(data_dir, "templates"),
			xsrf_cookies = False,
			cookie_secret = "11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1ao/Vo=",
		)
		tornado.web.Application.__init__(self, urls, **settings)

def do_main_program():
	http_server = tornado.httpserver.HTTPServer(FurnivallApplication())
	http_server.listen(options.port)
	print >> sys.stdout, "Listening for connections on port %s" % options.port
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	tornado.options.parse_command_line()
	do_main_program()


	#if __name__ == "__main__":
    #tornado.options.parse_command_line()
    #if options.daemonize:
    #    log_file = 'furnivall.%s.log' % options.port
    #    log = open(os.path.join('/var/log', log_file), 'a+')
    #    with daemon.DaemonContext(
    #        working_directory='/var/lib/furnivall',
    #        umask=0o002,
    #        pidfile=lockfile.FileLock('/var/run/furnivall.pid'),
    #        stdout=log,
    #        stderr=log
    #    ):
    #        do_main_program()
    #else:
    #    do_main_program()
