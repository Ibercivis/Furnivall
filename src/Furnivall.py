"""
    Ibervicis Furnivall is an open source framework for distributed user science.
    It helps to organize batches of tasks, collect them form users and do all the related housekeeping.

"""
import logging, os, daemon, lockfile
from Core.Handlers import MainHandler, LoginHandler, ObjectManager
import tornado.httpserver, tornado.database, tornado.ioloop, tornado.web

from ZODB.DB import DB
from ZODB.FileStorage import FileStorage

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)
define("daemonize", default=False, help="Run as daemon")

class DynamicUrlHandler(tornado.web.RequestHandler):
    def get(self):
        return

class Application(tornado.web.Application):
    def __init__(self):
        """
            Sets up the tornado web server and loads needed data from db
        """
        conn = DB(FileStorage('Data.fs')).open()
        self.db  = conn.root()
        self.initialize_db()
        self.researchers = self.db['users']
        urls = [
                ('/', MainHandler),
                ('/([^/]+)', MainHandler),
                ('/new/([^/]+)', ObjectManager),
                ('/Login/([^/]+)', LoginHandler),
                ('/View/([^/]+)', DynamicUrlHandler),
                ]

        settings = dict(
                template_path = os.path.join(os.path.dirname(__file__),
                    "templates"),
                static_path = os.path.join(os.path.dirname(__file__),
                    "static"),
                xsrf_cookies = True,
                cookie_secret = "11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        )

        self.special_login_slugs = {
                'root': '/Admin',
                'researcher': '/Admin/Researcher',
                'user': '/User/Home'
        }

        logging.debug('Starting server with urls: %s', urls)

        tornado.web.Application.__init__(self, urls, **settings)

    def initialize_db(self):
        try:
            self.db['users']
        except KeyError:
            from Core.Personality import User
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
