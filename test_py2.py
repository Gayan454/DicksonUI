#!/usr/bin/python
# -*- coding: utf-8 -*-
from dicksonui import Application, Form, Controls
a = Controls.h1()
a.Text("Hi")
Myform = Form()
App = Application()
Myform.Add(a)
App.Add(Myform)
print(Myform.Name())
print("Navigate To - "+App.location)
