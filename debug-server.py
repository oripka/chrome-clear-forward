#!/usr/bin/env python
# Reflects the requests from HTTP methods GET, POST, PUT, and DELETE
# Written by Nathan Hamiel (2010)

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser
import json

class RequestHandler(BaseHTTPRequestHandler):

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def do_GET(self):

        request_path = self.path

        print("\n----- Request Start ----->\n")
        print(request_path)
        print(self.headers)
        print("<----- Request End -----\n")


        self.send_response(200)
        self.send_header("Set-Cookie", "foo=bar")

    def do_POST(self):

        request_path = self.path

        #print("\n----- Post Request Start ----->\n")
        #print(request_path)

        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0
        #print(request_headers)
        #print("<----- Post Request End -----\n")


        print("<----- Parsing Start -----\n")
        data = json.loads(self.rfile.read(length))
        print("URL: "+data['url'])
        print("Method: "+data['method'])

        print("Data: "+str(data))
        #print(data['requestHeaders'])
        if 'requestHeaders' in data:
            for item in data['requestHeaders']:
                if item['name'] == "Cookie":
                    print "Cookie: "+ item['value']
                if item['name'] == "Referer":
                    print "Referer: "+ item['value']
                if item['name'] == "Content-length":
                    print "Content-Length: "+ item['value']

        if 'requestBody' in data:
            #TODO Headers not available in this case so this is the only way
            print("Content-Length: "+str(len(str(data["requestBody"]))))
            print("RequestBody: "+str(data['requestBody']))


        print("<----- Parsing End -----\n")

        self.send_response(200)

    do_PUT = do_POST
    do_DELETE = do_GET

def main():
    port = 8000
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler, bind_and_activate=False)
    server.allow_reuse_address = True
    server.server_bind()
    server.server_activate()
    server.serve_forever()


if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = ("Creates an http-server that will echo out any GET or POST parameters\n"
                    "Run:\n\n"
                    "   reflect")
    (options, args) = parser.parse_args()

    main()
