#!/usr/bin/env python
"""
    Ibervicis Furnivall is an open source framework for distributed user science.
    It helps to organize batches of tasks, collect them form users and do all the related housekeeping.

"""
import os, sys
import tornado.httpserver, tornado.database, tornado.ioloop, tornado.web
from tornado.options import define, options
from pymongo import Connection
from libs.route import Route
from Furnivall import data_dir
from Furnivall.Core.handlers import *
from Furnivall.Core.handlers.api import *

# Default options for the server
define("port", default=8888, help="run on the given port", type=int)
define("daemonize", default=False, help="Run as daemon")

class FurnivallApplication(tornado.web.Application):
	def __init__(self):
		"""
		Sets up the Tornado web server and loads all the init data
		"""
		self.dbconnection = Connection()
		self.db = self.dbconnection['furnivall']

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
