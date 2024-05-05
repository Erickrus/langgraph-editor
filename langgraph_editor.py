# -*- coding: utf-8 -*-#
'''
LangGraph Editor

Copyright 2024 by Hu, Ying-Hao (hyinghao@hotmail.com)
All rights reserved.
'''

import sys
import os

import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string
from tornado.options import define, options
from tornado.web import StaticFileHandler



import os
import tornado
import json

class CodeHandler(tornado.web.RequestHandler):


    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')

    def options(self):
        # no body
        self.set_header("Access-Control-Allow-Headers","*")
        self.set_status(204)
        self.finish()

    def error_out(self, message):
        self.set_status(400)
        return self.finish(json.dumps({"error": message}))

    def post(self):
        data = json.loads(self.get_argument("json"))

        requiredFields = ["code"]
        for requiredField in requiredFields:
            if requiredField not in data:
                self.set_status(400)
                return self.finish(json.dumps({"error":"Missing data. Required JSON fields: %s" % ", ".join(requiredFields)}))

        print(data["code"])
        with open("/content/output.py", "w") as f:
            f.write(data["code"])

        self.write({"message":"ok"})

class NoCacheStaticFileHandler(StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"^/api/saveCode", CodeHandler),
            (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": os.path.join(".", "static")}),
            (r'^/static/(.*?)$', 
             NoCacheStaticFileHandler, 
             {"path":os.path.join(".", "static"), "default_filename":"index.html"}),
        ]
        tornado.web.Application.__init__(self, handlers)

def main(argv):
    portNum = 8082
    define("port", default=portNum, help="run on the given port", type=int)

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(portNum)

    print("HTTP service is started on port %s" % str(portNum))
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == "__main__":
    main(sys.argv)

