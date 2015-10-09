import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.auth
from tornado.options import define, options
from tornado.web import URLSpec as URL

import base64
import uuid
import hashlib

import base

define("port", default=8888, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        try:
            user=self.get_secure_cookie("user")
            return user
        except:
            return None

class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login/")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)


class LoginHandler(BaseHandler):
    def get(self):
        self.render("html/login.html")
    def post(self):
        username=self.get_argument("username")
        password=hashlib.md5(self.get_argument("password")).hexdigest()
        userdata=base.accounts()
        print username
        print password
        print userdata.is_user(username, password)
        if userdata.is_user(username, password):
            self.set_secure_cookie("user", username)
            self.redirect("/")
class CreateuserHandler(BaseHandler):
    def get(self):
        self.render("html/createuser.html")

settings = {
    "cookie_secret": base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
    "login_url": "/login/",
}

application = tornado.web.Application([
        URL(r"/", MainHandler),
        URL("/login/", LoginHandler),
        URL(r"/create", CreateuserHandler, name='create'),
        URL(r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "public"}),
], debug=True, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
