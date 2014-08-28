import json
import os

import cherrypy

class MyVerySecureTwitterClone(object):

  @cherrypy.expose
  def index(self):
    self.loadMessages()

    output = '''
<script src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
<script>
function clean(str) {
    return str.replace(/</g, '&lt;')
              .replace(/"/g, '&quot;')
              .replace(/'/g, '&#39;');
}

function sendMessage() {
    $.ajax('/post', {
        data: {
            'message': clean($('textarea[name="message"]').val()),
            'name': clean($('input[name="name"]').val())
        },
        success: function() {
            location.reload();
        }
    });
}
</script>
'''

    for message in self.messages:
      output += '<p>{0} -- <a href="/profile?name={1}">{1}</a></p>'.format(
          self.clean(message['text']),
          self.clean(message['name'])
      )
      output += '<hr />'

    output += '''
<form action="javascript:sendMessage()">
  Name:<br /><input name="name" /><br />
  Message:<br /><textarea name="message" rows="4" cols="50"></textarea><br />
  <button type="submit">Send!</button>
</form>
    '''

    return output

  @cherrypy.expose
  def post(self, name, message):
    self.loadMessages()
    self.messages.append({'name': name, 'text': message})
    self.saveMessages()

    raise cherrypy.HTTPRedirect("/")

  @cherrypy.expose
  def profile(self, name):
    return '''This is {0}'s profile<br />
Click <a href="/">here</a> to return'''.format(name)

  def loadMessages(self):
    self.messages = []
    if os.path.exists('messages.json'):
      with open('messages.json', 'r') as fin:
        self.messages = json.loads(fin.read())

  def saveMessages(self):
    with open('messages.json', 'w') as fout:
      fout.write(json.dumps(self.messages))

  def clean(self, str):
    return (str.replace('<', '&lt;')
               .replace('"', '&quot;')
               .replace("'", '&#39;'));

cherrypy.config.update({
  'server.socket_host': '127.0.0.1',
  'server.socket_port': 8418,
})

if __name__ == '__main__':
  cherrypy.quickstart(MyVerySecureTwitterClone())
