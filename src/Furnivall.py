"""
    Ibervicis Furnivall is an open source framework for distributed user science.
    It helps to organize batches of tasks, collect them form users and do all the related housekeeping.

"""
import daemon, logging, os
from Core.common import commonClass as commonClass
from Core.UserHandler import ObjectManager
from tornado.options import define, options
import tornado.httpserver
import tornado.web as web
from Core.Handlers import MainHandler

import tornado.ioloop
import lockfile

define("port", default=8888, help="run on the given port", type=int)
define("db_host", default="localhost", help="database host")
define("db_user", default="root", help="database username")
define("db_db", default="furnivall", help="database name")
define("db_password", default="root", help="database password")


class Application(commonClass, web.Application):
    def __init__(self):
        """
            Sets up the tornado web server and loads needed data from db
        """


        self.db  = tornado.database.Connection(options.db_host, options.db_db, options.db_user, options.password)
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

        self.researchers = self.initialize_researchers()

        logging.info('Loading Furnival main application')
        logging.debug('Researchers initialized from database: %s',
                self.researchers)
        logging.debug('Starting server with urls: %s', urls)

        web.Application.__init__(self, urls, **settings)

def do_main_program(self):
    """
        DO: All objects must be saved and reloaded from the database.
    """
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    with daemon.DaemonContext(
        working_directory='/var/lib/furnivall',
        umask=0o002,
        pidfile=lockfile.FileLock('/var/run/furnivall.pid'),
    ):
        logging.info("Starting daemon")
        do_main_program()
