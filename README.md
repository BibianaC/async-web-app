# Async Web App

## Description

1. Create a Python web application using Tornado web server and host it as an App Engine project on Google.
2. The project should have a single page with a form where I can enter a URL to any website (e.g. Wikipedia or BBCNews)
3. The application should fetch that url and build a dictionary that contains the frequency of use of each word on that page.
4. Use this dictionary to display, on the client’s browser, a `word cloud` of the top 100 words, where the font size is largest for the words used most frequently, and gets progressively smaller for words used less often.
5. Each time a URL is fetched, it should save the top 100 words to a MySQL DB (Google Cloud SQL), with the following three columns:
  - The primary key for the word is a salted hash of the word.
  - The word itself is saved in a column that has asymmetrical encryption, and you are saving the encrypted version of the word.
  - The total frequency count of the word.

Each time a new URL is fetched, you should INSERT or UPDATE the word rows.
 
 
Extra points for:
  - Displaying just nouns and verbs (no prepositions or articles)
  - In README, describe the best way to safely store and manage the keys.
  - Elegant front end layout.
  - Clean, well-documented code.

## Local development

### Installation
1. Download the project
  - `$ git clone https://github.com/BibianaC/async-web-app.git`
2. Install dependencies
  - `$ pip install -r requirements.txt`
  - `$ pip install -r requirements.test`

### Run
- Async Web App
  - `$ python async_web_app.py`
  - Enter a `url` in the form.

- Tests `$ py.test test_async_web_app.py `

## Comments

The application functions properly when ran locally, as described above.
I did not managed to make it run in app engine.

### [Google App Engine](https://async-web-app.appspot.com/) - Doesn't work.

When I run Google App Engine locally `$ dev_appserver.py . `. I receive the following error:

```
ImportError: No module named wordcloud.query_integral_image
```
I tried to copy `query_integral_image.so` to `app_engine_dependencies/wordcloud`.
Then I deleted the part of the code that calls `query_integral_image`.
I receive the following error:

```
ApplicationError: ApplicationError: 5 Attempt to bind port without permission.

DEBUG    2016-12-05 20:10:00,243 api_server.py:277] Handled remote_socket.CreateSocket in 0.0033
ERROR    2016-12-05 20:10:00,697 wsgi.py:279] 
Traceback (most recent call last):
  File "/Users/Bibs/dev/google-cloud-sdk/platform/google_appengine/google/appengine/runtime/wsgi.py", line 267, in Handle
    result = handler(dict(self._environ), self._StartResponse)
TypeError: 'module' object is not callable
```

### MySQL DB - Not done.

### Displaying just nouns and verbs (no prepositions or articles)

Two possible ways of implementation.

- Use [NLTK](http://www.nltk.org/) library
  - Run the Python interpreter and type the commands:
  ```
  $ import nltk
  $ nltk.download()
  ```
  - In the app:
  ```
  from nltk.corpus import stopwords

  stop_words=set(stopwords.words('english'))
  txt="a long string of text"
  print filter(lambda w: not w in s,txt.split())
  ```

- Wordcloud library
  ```
  from wordcloud import WordCloud, STOPWORDS
  wordcloud = WordCloud(stopwords=STOPWORDS).generate(most_common_str)
  ```