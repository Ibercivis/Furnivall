#!/usr/bin/env python
"""
    Ibervicis Furnivall is an open source framework for distributed user science.
    It helps to organize batches of tasks, collect them form users and do all the related housekeeping.

"""
from tornadorpc.json import JSONRPCHandler
from tornadorpc import private
import logging, os, daemon, lockfile
from Furnivall.Core.Handlers import MainHandler, LoginHandler, ObjectManager
from Furnivall import data_dir
import tornado.httpserver, tornado.database, tornado.ioloop, tornado.web
import Furnivall.Views as Views
from ZODB.DB import DB
from ZODB.FileStorage import FileStorage

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)
define("daemonize", default=False, help="Run as daemon")

class StaticInterfaceProvider(tornado.web.RequestHandler):
    def get(self, template, place):
        return self.render(template + "_" + place, user_id=self.get_secure_cookie('username'))

class DynamicUrlHandler(tornado.web.RequestHandler):
    """
        Manages views' urls.
    """
    def get(self, researcher, view, askfor):
        viewfile, viewclass = self.application.extra_urls[view]
        researcher = researcher # TODO: Get researcher.
        view = getattr(getattr(Views, view),viewfile)(False) # TODO: make this with a initialized object from somewhere
        return self.write(getattr(view, viewclass)(askfor))

class RPCDynamicUrlHandler(JSONRPCHandler):
    def send_command(self, command):
        viewfile, viewclass = self.application.extra_urls[view]
        researcher = researcher # TODO: Get researcher.
        view = getattr(getattr(Views, view),viewfile)(False) # TODO: make this with a initialized object from somewhere
        return getattr(view, viewclass)(command)

class Application(tornado.web.Application):
    def __init__(self):
        """
            Sets up the tornado web server and loads needed data from db
        """
        conn = DB(FileStorage('Data.fs')).open()
        self.db  = conn.root()
        self.initialize_db()
        self.extra_urls = {}
        self.researchers = self.db['users']
        for a in self.get_all_urls():
            for template in a.keys():
                self.extra_urls[template] = a[template]

        urls = [
                ('/', MainHandler),
                ('/([^/]+)', MainHandler),
                ('/new/([^/]+)', ObjectManager),
                ('/Login/([^/]+)', LoginHandler),
                ('/RPC/([^/]+)/([^/]+)/([^/]+)', RPCDynamicUrlHandler),
                ('/View/([^/]+)/([^/]+)/([^/]+)', DynamicUrlHandler),
                ('/([^/]+)/(.+)', StaticInterfaceProvider ),
                ]

        settings = dict(
                static_path=os.path.join(data_dir, "static"),
                template_path=os.path.join(data_dir, "templates"),
                xsrf_cookies = True,
                cookie_secret = "11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1ao/Vo=",
        )

        self.special_login_slugs = {
                'root': '/Admin',
                'researcher': '/Admin/Researcher',
                'user': '/User/Home'
        }

        logging.debug('Starting server with urls: %s', urls)

        tornado.web.Application.__init__(self, urls, **settings)

    def get_all_urls(self):
        """
            generator returning a dict of url: (file, class) list for the url building
        """
        views = Views.ViewClasses 
        return ( getattr(getattr(Views, viewfile), views[viewfile][0])(None).templates\
            for viewfile in views.keys() )

    def initialize_db(self):
        try:
            self.db['users']
        except KeyError:
            from Furnivall.Core.Personality import User
            self.db['users'] = {
                    'anonymous' : User(self),
                    'root' : User(self)
                    }
            self.db['users']['anonymous'].set_password("anonymous")
            self.db['users']['root'].set_password("root")
            self.db['users']['root'].grant_permission('root')

def do_main_program():
    """
        DO: All objects must be saved and reloaded from the database.
    """
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    if options.daemonize:
        log_file = 'furnivall.%s.log' % options.port
        log = open(os.path.join('/var/log', log_file), 'a+')
        with daemon.DaemonContext(
            working_directory='/var/lib/furnivall',
            umask=0o002,
            pidfile=lockfile.FileLock('/var/run/furnivall.pid'),
            stdout=log,
            stderr=log
        ):
            do_main_program()
    else:
        do_main_program()
