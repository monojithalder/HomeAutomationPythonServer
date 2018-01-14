from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qs
import cgi
import serial
import time
import sys
import glob

ser = ''
class GP(BaseHTTPRequestHandler):
    global ser
    ports = glob.glob('/dev/tty[A-Za-z]*')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    port = result[0]
    ser = serial.Serial(port, 9600)
    time.sleep(10)
    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_HEAD(self):
        self._set_headers()
    def do_GET(self):
        self._set_headers()
        print parse_qs(self.path[2:])
        self.wfile.write("<html><body><h1>Get Request Received!</h1></body></html>")
    def do_POST(self):
        global ser
        self._set_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        #print form.getvalue("foo")
        pin_no = form.getvalue("pinNo")
        try:
            ser.write(pin_no)
            self.wfile.write('{"success": 1}')
        except:
            ports = glob.glob('/dev/tty[A-Za-z]*')
            result = []
            for port in ports:
                try:
                    s = serial.Serial(port)
                    s.close()
                    result.append(port)
                except (OSError, serial.SerialException):
                    pass
            port = result[0]
            ser = serial.Serial(port, 9600)
            time.sleep(10)
            self.wfile.write('{"success": 0}')
            #pass
        

def run(server_class=HTTPServer, handler_class=GP, port=8088):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Server running at localhost:8088...'
    httpd.serve_forever()

run()   