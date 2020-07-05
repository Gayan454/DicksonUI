#!/usr/bin/python
# -*- coding: utf-8 -*-
from .signalpy import *
from .signalpy import jslib
import os
package_dir = os.path.dirname(__file__)

class Application():


    def __init__(self, address=('',None)):
        self._forms = []
        self._counter = 0
        self.Icon = b'DicksonUI'
        self.app=app
        self.Hub=Hub
        self.server=Server(address)
        self.server.serve_forever()
        self.location =self.server.base_environ.get('SERVER_NAME')+self.server.base_environ.get('SERVER_PORT')
        app.routes['/']=self.mainhandler
        app.routes['/favicon.ico']=self.faviconhandler
        app.routes['/DicksonUI.js']=self.jslibhandler

    def mainhandler(self, environ, start_response):
        fn = self._forms[0].Name
        start_response('302 Object moved temporarily -- see URI list', [('Location', fn)])
        res=self.location + '/' + fn
        return res.encode()

    def faviconhandler(self, environ, start_response):
        start_response('200 OK', [])
        return[self.Icon]

    def jslibhandler(self, environ, start_response):
        path = os.path.join(package_dir, 'DicksonUI.js')
        start_response('200 OK', [])
        return[jslib.data.encode()+open(path, mode='rb').read()]

    def Add(self, bom):
        if bom.Name == None:
            self._counter += 1
            bom.Name='Window' + str(self._counter)
            self._forms.append(bom)
            bom.initialize(self)
        else:
            self._forms.append(bom)
            bom.initialize(self)

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
        self.server.shutdown()
        self.server.socket.close()
        self.server = None
        self=None

