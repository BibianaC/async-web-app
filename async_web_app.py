from collections import Counter
import os
import re

from bs4 import BeautifulSoup
import requests
import tornado.httpserver
import tornado.ioloop
import tornado.web
from wordcloud import WordCloud


def get_html_text(url):
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'lxml')

    # Delete elements from html.
    [script.extract() for script in html(
        ['script', 'style', '[document]', 'head', 'title', 'meta'])]

    return html.text.encode('utf8')


def count_words(text):
    words_list = re.findall(r'\w+', text.lower())
    counter_dict = Counter(words_list)

    # Remove integers and single character tokens.
    for word in counter_dict.copy():
        if type(word) is int or len(word) == 1:
            counter_dict.pop(word)

    return counter_dict


def get_most_common_words(counter_dict):
    # Take the 100 most common words and mutiply by their frequency.
    # TODO find a better way.
    most_common = [
        (word + ' ') * frequency
        for word, frequency in counter_dict.most_common(100)
    ]
    return ' '.join(most_common)


def generate_word_cloud(string):
    wordcloud = WordCloud(background_color='white').generate(string)
    return wordcloud.to_image()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", wordcloud=None)

    def post(self):
        url = self.get_argument('fetch_url', None)
        text = get_html_text(url)
        counter_dict = count_words(text)
        most_common_str = get_most_common_words(counter_dict)
        wordcloud = generate_word_cloud(most_common_str)

        self.render("index.html", wordcloud=wordcloud)


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
