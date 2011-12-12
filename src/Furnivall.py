"""
    Ibervicis Furnivall is an open source framework for distributed user science.
    It helps to organize batches of tasks, collect them form users and do all the related housekeeping.

"""
import logging, os, daemon, lockfile

from Core.common import commonClass as commonClass
from Core.UserHandler import ObjectManager
from Core.Handlers import MainHandler

from tornado.options import define, options
import tornado.httpserver, tornado.database, tornado.ioloop
import tornado.web as web


define("port", default=8888, help="run on the given port", type=int)
define("db_host", default="localhost", help="database host")
define("db_user", default="root", help="database username")
define("db_db", default="furnivall", help="database name")
define("daemonize", default=False, help="Run as daemon")
define("db_password", default="root", help="database password")


class Application(commonClass, web.Application):
    def __init__(self):
        """
            Sets up the tornado web server and loads needed data from db
        """


        self.db  = tornado.database.Connection(options.db_host, \
                options.db_db, options.db_user, options.db_password)
        self.read_config()
        urls = [
                ("/([^/]+)", MainHandler),
                ("/", MainHandler),
                ("/new/([^/]+)", ObjectManager),
                ]

        settings = dict(
                template_path = os.path.join(os.path.dirname(__file__),
                    "templates"),
                static_path = os.path.join(os.path.dirname(__file__),
                    "static"),
                xsrf_cookies = True,
                cookie_secret = "11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        )

        special_login_slugs = {
                'root': '/Admin/',
                'researcher': '/Admin/Researcher',
                'user': '/User/Home'
        }


        logging.info('Loading Furnival main application with logins:%s',
                special_login_slugs)
        logging.debug('Starting server with urls: %s', urls)

        web.Application.__init__(self, urls, **settings)

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
