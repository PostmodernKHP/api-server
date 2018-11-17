import time
import json
from uuid import uuid4
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = 'localhost'
PORT_NUMBER = 9000
PENDING_USERS = {
  '0243cf5e-98d3-4e17-1234-151e8b7ef750': {'severity': 55},
  '2': {'severity': 15},
  '3': {'severity': 90}
  }

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
      # Handle for different GET endpoints
      if self.path == '/userid':
        data = {'userId': str(uuid4())}
      elif self.path == '/pendinguser':
        data = PENDING_USERS
      else:
        data = {'nothingHere': None}

      self.respond(data)

    def do_POST(self):
      content_len = int(self.headers['Content-Length'])
      # grab data here
      post_body = self.rfile.read(content_len)
      # create new user
      if self.path == '/user':
        new_user = json.loads(post_body.decode('UTF-8'))
        print(new_user)
        user_id = new_user.pop('id')
        PENDING_USERS[user_id] = new_user

      self.send_response(200)
      self.end_headers()


    def respond(self, data):
      data = json.dumps(data)
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.send_header("Access-Control-Allow-Origin", "*")
      self.end_headers()
      self.wfile.write(bytes(data, 'UTF-8'))


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))