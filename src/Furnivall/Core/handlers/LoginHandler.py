from libs.route import Route
from BaseHandler import BaseHandler
import hashlib
import tornado

@Route(r"/login")
class LoginHandler(BaseHandler):
	def get(self):
		self.render("login.template")

	def post(self):
		username = self.get_argument("txt-username", "")
		password = self.get_argument("txt-password", "")

		hasher = hashlib.sha256()
		hasher.update(password)
		digested_password = hasher.hexdigest()

		users = self.application.db.users
		user = users.find_one({'$or' : [{'name': username}, {'email': username}]})
		if user and user['password'] == digested_password:
			self.set_current_user(username)
			self.redirect(u"/")
		else:
			print "Usuario incorrecto"
			self.render("login.template")

	def set_current_user(self, user):
		if user:
			self.set_secure_cookie("user", tornado.escape.json_encode(user))
		else:
			self.clear_cookie("user")


@Route(r"/logout")
class LogoutHandler(BaseHandler):
	def get(self):
		self.clear_cookie("user")
		self.redirect(u"/login")

@Route(r"/register")
class RegisterHandler(LoginHandler):
	def get(self):
		self.render("register.template")

	def post(self):
		username = self.get_argument("txt-nickname", "")
		email = self.get_argument("txt-email", "")
		password = self.get_argument("txt-password", "")
		repeated_password = self.get_argument("txt-repeat-password", "")

		users = self.application.db.users
		already_taken = users.find_one({'$or' : [{'name': username}, {'email': email}]})
		if already_taken:
			error_msg = u"El nombre de usuario o el email ya han sido usados"
			self.render("register.template")

		hasher = hashlib.sha256()
		hasher.update(password)
		user = { 'name': username,
				 'email': email,
				 'password': hasher.hexdigest() } ## FIXME: [JUANJO] Comprobar que los dos passwords son los mismos.
		users.insert(user)

		self.set_current_user(username)

		self.redirect(u"/")
