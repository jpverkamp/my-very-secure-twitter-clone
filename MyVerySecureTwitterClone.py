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
    return str.replace(new RegExp('</?script>', 'g'), '');
}

function sendMessage() {
    $.ajax('/post', {
        data: {
            'message': clean($('textarea[name="message"]').val())
        },
        success: function() {
            location.reload();
        }
    });
}
</script>
'''

    for message in self.messages:
      output += '<p>{0}</p>'.format(message['text'])
      output += '<hr />'

    output += '''
<form action="javascript:sendMessage()">
  <textarea name="message" rows="4" cols="50"></textarea><br />
  <button type="submit">Send!</button>
</form>
    '''

    return output

  @cherrypy.expose
  def post(self, message):
    self.loadMessages()
    self.messages.append({'text': message})
    self.saveMessages()

    raise cherrypy.HTTPRedirect("/")

  def loadMessages(self):
    self.messages = []
    if os.path.exists('messages.json'):
      with open('messages.json', 'r') as fin:
        self.messages = json.loads(fin.read())

  def saveMessages(self):
    with open('messages.json', 'w') as fout:
      fout.write(json.dumps(self.messages))


cherrypy.config.update({
  'server.socket_host': '127.0.0.1',
  'server.socket_port': 8418,
})

if __name__ == '__main__':
  cherrypy.quickstart(MyVerySecureTwitterClone())
