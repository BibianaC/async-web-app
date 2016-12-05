# CHECK ORDER
from collections import Counter
import os
import re

from bs4 import BeautifulSoup
import requests
import tornado.httpserver
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        url = self.get_argument('fetch_url', None)
        response = requests.get(url)
        html = BeautifulSoup(response.text, 'lxml')

        # Delete script, style and head elements.
        for script in html(["script", "style", "head"]):
            script.extract()

        text = (html.text).encode('utf8')
        words_list = re.findall(r'\w+', text.lower())
        counter_dict = Counter(words_list)
        most_common = counter_dict.most_common(100)

        print most_common


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]
        settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), "bootstrap")
        }
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
