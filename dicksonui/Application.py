#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from socketserver import ThreadingMixIn
except ImportError:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
    from SocketServer import ThreadingMixIn
import os
import threading
from .utiles import find_free_port
package_dir = os.path.dirname(__file__)
from sys import version_info
if version_info[0] < 3:
    from .Form_min import Form as form
else:
    from .Form import Form as form

class Application(ThreadingMixIn, HTTPServer):

    """Server that responds to each request in a separate thread."""

    allow_reuse_address = True
    daemon_threads = True  # comment to keep threads alive until finished

    def __init__(
        self,
        host='127.0.0.1',
        port=1024,
        max_port=65535,
        ):

        self.port = find_free_port(port, max_port)
        self._forms = []
        self._counter = 0
        self.routes = {}
        self.Icon = None
        self.location ='http://localhost:' + str(self.port)
        HTTPServer.__init__(self, (host, self.port), RequestHandler)
        t = threading.Thread(target=self.serve_forever)
        t.daemon = False
        t.start()


    def rhandler(self, s):
        if s.path == '/DicksonUI.js':
            path = os.path.join(package_dir, 'DicksonUI.js')
            s.send_response(200)
            s.send_no_cache_headers()
            s.end_headers()
            s.write_bytes(open(path).read())
        if s.path == '/favicon.ico':
            try:
                s.send_response(200)
                s.send_no_cache_headers()
                s.end_headers()
                s.wfile.write(self.Icon)
            except Exception as e:
                print(e)
        if s.path == '/':
            s.send_response(302)
            if version_info[0] < 3:
                fn = self._forms[0].Name()
            else:
                fn = self._forms[0].Name
            s.send_header('Location', 'http://localhost:'
                          + str(self.port) + '/' + fn)
            s.end_headers()
        for _form in self._forms:
            if version_info[0] < 3:
                fn = _form.Name()
            else:
                fn = _form.Name
            if s.path.startswith('/' + fn):
                if s.path == '/' + fn:
                    path = os.path.join(package_dir, 'index.html')
                    s.send_response(200)
                    s.send_no_cache_headers()
                    s.end_headers()
                    s.write_bytes(open(path).read())
                else:
                    _form.RequestHandler(s)
        for route in self.routes:
            if s.path.startswith(route):
                f = self.routes[route]
                f(s)

    def Register(self, Path, Handler):
        self.routes[Path] = Handler

    def Add(self, Form=form):
        if version_info[0] < 3:
            if Form.Name() == None:
                self._counter += 1
                Form.Name('Form' + str(self._counter))
        else:
            if Form.Name == None:
                self._counter += 1
                Form.Name = 'Form' + str(self._counter)
        self._forms.append(Form)

    def config(self, *args):
        self.conf = args

    def Show(self, form):
        if self.conf[0] == 'chrome app':
            from .chrome import chrome
            c = chrome()
            path = c.find_path()
            if path == None:
                raise Exception('Chrome or Chromium not available')
            t = threading.Thread(target=c.run, args=[path,
                                 self.conf[1], self.location + '/'
                                 + form.Name, self.conf[2]])
            t.daemon = True
            t.start()
        elif self.conf[0] == 'firefox':
            from .firefox import firefox
            f = firefox()
            path = f.find_path()
            if path == None:
                raise Exception('Firefox not available')
            t = threading.Thread(target=f.run, args=[
                                path,
                                self.conf[1],
                                self.location + '/' + form.Name,
                                self.conf[2],
                                self.conf[3],
                                self.conf[4],])
            t.daemon = True
            t.start()
        elif self.conf[0] == 'edge':
            from .edge import edge
            t = threading.Thread(target=edge.run, args=[path,
                self.conf[1], self.location + '/'
                + form.Name])
            t.daemon = True
            t.start()
        elif self.conf[0] == 'webview':
            import webview
            c = {
                'width': self.conf[1],
                'height': self.conf[2],
                'resizable': self.conf[3],
                'fullscreen': self.conf[4],
                }
            w = webview.create_window(form.Name, self.location + '/'
                    + form.Name, **c)
            webview.start()

        # Electron support coming soon.

    def stop(self):
        self.shutdown()
        self.socket.close()
        self = None


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.server.rhandler(self)

    def send_no_cache_headers(self):
        """Add headers to the response telling the client to not cache anything."""

        # Source: http://stackoverflow.com/questions/49547/making-sure-a-web-page-is-not-cached-across-all-browsers

        self.send_header('Cache-Control',
                         'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')

    def do_POST(self):
        self.server.rhandler(self)
    
    def write_bytes(self, string):
        try:
            self.wfile.write(bytes(string))
        except:
            self.wfile.write(bytes(string, 'utf-8'))

    def version_string(self):
        """Return the server software version string."""
        return "DicksonUI"
