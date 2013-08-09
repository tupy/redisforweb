
import time
import hashlib
import pickle
import redis
import flask

app = flask.Flask(__name__)
redis = redis.StrictRedis()

def memoized(func):

  def newfunc(*args, **kwargs):
    
    key = '%s:%s' % (func.func_name, hashlib.md5(str(args) + str(kwargs)).hexdigest()) 
    value = redis.get(key)
    if value: 
      return pickle.loads(value)

    value = func(*args, **kwargs)
    redis.set(key, pickle.dumps(value))
    return value    

  return newfunc


@app.route('/post/<int:year>/<int:month>/<int:day>')
@memoized
def post_view(year, month, day):
  time.sleep(2)
  return "This is the post for %d/%d/%d" % (month, day, year)

if __name__ == '__main__':
  app.run(debug=True)
