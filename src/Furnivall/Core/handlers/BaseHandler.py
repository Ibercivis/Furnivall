import tornado.web

class BaseHandler(tornado.web.RequestHandler):

	def prepare(self):
		self.application_list = []
		for app in self.application.db.applications.find():
			self.application_list.append(app['name'])

	def get_login_url(self):
		return u"/login"

	def get_current_user(self):
		user_json = self.get_secure_cookie("user")
		if user_json:
			return tornado.escape.json_decode(user_json)
		else:
			return None

	def render(self, template, **kwargs):
		kwargs['application_list'] = self.application_list

		super(BaseHandler, self).render(template, **kwargs)
