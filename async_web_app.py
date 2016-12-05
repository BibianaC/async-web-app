# CHECK ORDER
from collections import Counter
import os
import re

from bs4 import BeautifulSoup
import requests
import tornado.httpserver
import tornado.ioloop
import tornado.web
from wordcloud import WordCloud


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", wordcloud=None)

    def post(self):
        url = self.get_argument('fetch_url', None)
        response = requests.get(url)
        html = BeautifulSoup(response.text, 'lxml')

        # Delete elements from html.
        [script.extract() for script in html(
            ['script', 'style', '[document]', 'head', 'title', 'meta'])]

        text = (html.text).encode('utf8')
        words_list = re.findall(r'\w+', text.lower())
        counter_dict = Counter(words_list)

        for word in counter_dict.copy():
            if type(word) is int or len(word) == 1:
                counter_dict.pop(word)

        # Takes the 100 most common words and mutiplies them for its frequency
        most_common = [
            (word + ' ') * frequency
            for word, frequency in counter_dict.most_common(100)
        ]
        most_common_str = ' '.join(most_common)

        wordcloud = WordCloud(background_color='white').generate(most_common_str)
        image = wordcloud.to_image()

        self.render("index.html", wordcloud=image)

        # print counter_dict


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
