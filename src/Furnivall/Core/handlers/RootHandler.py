from libs.route import Route
from BaseHandler import BaseHandler
import tornado.web

@Route(r"/")
class RootHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.render("home.template")
