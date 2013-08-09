
import time
import threading
import simplejson
import flask
import redis

from flask import request

app = flask.Flask(__name__)
app.config['CONTACT_MAIL'] = 'suport@example.com'
redis = redis.StrictRedis()

@app.route('/')
def index():
  return """
  <form action="/send_mail" method="post">
    <input type="text" name="from" value="" placeholder="Your e-mail" /><br />
    <input type="text" name="subject" value="" placeholder="Subject" /><br />
    <label>Message:</label><br />
    <textarea name="message"></textarea><br />
    <input type="submit" name="submit" value="Send" />
  </form>
  """

@app.route('/send_mail', methods=['POST'])
def send_mail():

  data = {
    'from': request.form.get('from'),
    'recipients': [app.config['CONTACT_MAIL']],
    'subject': request.form.get('subject'),
    'message': request.form.get('message')
  } 

  mail_message = simplejson.dumps(data)
  redis.rpush('mailqueue', mail_message)

  return 'Message sent!'

class Mailer(threading.Thread):
  
  def run(self):
    while True:
      mail_message = redis.lpop('mailqueue')
      if mail_message:
        mail_message = simplejson.loads(mail_message)
        self.send(mail_message)
      time.sleep(1)
 
  def send(self, mail_message):
    print "Sending mail from %s" % mail_message['from']
    

if __name__ == '__main__':
  Mailer().start()
  app.run(debug=True)
