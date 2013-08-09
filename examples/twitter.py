import time
import redis
import flask

from flask import request, redirect

app = flask.Flask(__name__)
redis = redis.StrictRedis()

@app.route('/')
def index():
  tweets = [redis.get(k) for k in redis.keys('tweet:*')]
  return """
  <form action="/tweet" method="post">
  <textarea name="message"></textarea><br />
  <input type="submit" name="submit" value="Enviar">
  </form>
  <br />
  %s
  """ % '<br /><br />'.join(tweets) 


@app.route('/tweet', methods=['POST'])
def tweet():
  message = request.form.get('message')
  key = 'tweet:%s' % time.strftime('%Y-%m-%d-%Hh%M')
  redis.set(key, message)
  return redirect('/')


if __name__ == '__main__':
  app.run(debug=True)
