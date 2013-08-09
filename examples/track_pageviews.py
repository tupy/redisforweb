
import redis
import flask

app = flask.Flask(__name__)
redis = redis.StrictRedis()

def track_pageviews():
  return redis.incr('pageviews')

@app.route('/')
def index():
  return 'Total of Pageviews: %d' % track_pageviews()


if __name__ == '__main__':
  app.run(debug=True)
