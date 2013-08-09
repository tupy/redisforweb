
import flask
import redis

app = flask.Flask(__name__)
redis = redis.StrictRedis()


@app.route('/')
def index():
  teams = redis.zrevrange('top:teams', 0, -1, withscores=True)
  template = """
  <h2>Ranking of soccer fan base in Bahia</h2>
  <ol>
  {% for name, votes in teams %}
    <li>{{name}}: {{votes|int}} <a href="/vote/{{name}}">+1</a></li>
  {% endfor %}
  </ol>
  """
  return flask.render_template_string(template, teams=teams)


@app.route('/vote/<key>')
def vote(key):
  key = 'team:%s' % key
  votes = redis.hincrby(key, 'votes', 1)
  team = redis.hget(key, 'name')
  redis.zadd('top:teams', votes, team)
  return flask.redirect('/')


def setup():

  teams = [('Bahia', 2400000), ('Vitoria', 2000000), ('Jacuipense', 5005), ('Galicia', 5000)]

  for name, votes in teams:
    key = 'team:%s' % name
    redis.hmset(key, dict(name=name, votes=votes))
    redis.zadd('top:teams', votes, name)


if __name__ == '__main__':
  setup()
  app.run(debug=True)
