# -*- coding: utf-8 -*-

from libs.route import Route
from BaseHandler import BaseHandler

@Route(r"/admin/users")
class UsersHandler(BaseHandler):
	def get(self):
		self.users = []
		for user in self.application.db.users.find():
			self.users.append({'name': user['name'],
							   'email': user['email']})

		self.render("admin/users.template", users = self.users)
