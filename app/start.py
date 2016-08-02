#-*- encoding: utf-8 -*-

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import config
import route

from tornado.options import define, options

define("port", default=9801, help="Count Run server on a specific port", type=int)
define("service_log_file", default='./logs/sso.log', help="Count Run server on service_log_file", type=str)

class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, route.route, **(config.settings))


def main():
    tornado.options.parse_command_line()

    config.log_path = options.service_log_file
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
