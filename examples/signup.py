
import redis
import flask

from flask import request, redirect

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'k3rdsvalkdsahdklh2344dsabnbbdas/1!dssdf'
redis = redis.StrictRedis()


class User:

  def __init__(self):
    self.id = None
    self.name = None
    self.email = None
    self.password = None

  @staticmethod
  def save(user):
    if user.id is None:
      user.id = redis.incr('user_count')
    redis.hmset('user:%d' % user.id, user.__dict__)
    return user
    
  @staticmethod
  def get(uid):
    user = User()
    attrs = user.__dict__.keys()
    _user = dict(zip(attrs, redis.hmget('user:%d' % uid, attrs)))
    user.__dict__.update(_user)
    return user
 
@app.route('/')
def index():
  
  uid = flask.session.get('uid')
  if uid is not None:
    user = User.get(int(uid))
    return "Hello %s (%s)" % (user.name, user.email)
  return """
  <form action="/signup" method="post">
    <input type="text" name="name" value="" placeholder="Type your name" /><br />
    <input type="text" name="email" value="" placeholder="e-mail" /><br />
    <input type="password" name="password" value="" placeholder="Password" /><br />
    <input type="submit" name="submit" value="Signup" />
  </form>
  """


@app.route('/signup', methods=['POST'])
def signup():  

  user = User()
  user.name = request.form.get('name')
  user.email = request.form.get('email')
  User.save(user)
  
  flask.session['uid'] = user.id
  return redirect('/')

if __name__ == '__main__':
 app.run(debug=True)
