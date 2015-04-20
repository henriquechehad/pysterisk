#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import datetime

class Log(object):

    def __init__(self, log_file):
        self.log_path = log_file

    def log(self, text):
        open(self.log_path, 'ab+', 512).write("%s: %s\n" % (datetime.datetime.now(), text))


class AMI():
	
	logdata = None
	s = None

	def __init__(self, log_file='/tmp/pysterisk_ami.log'):
		self.logdata = Log(log_file)
		

	def connect(self, host, port, username, password,):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((host, port))

		params = [
					"Action: login",
        			"Events: off",
          			"Username: " + username,
          			"Secret: " + password
          		]

		self.s.send("\r\n".join(params) + "\r\n")

		# Login try respose
		data = ""
		while "\r\n" not in data:
    			data += self.s.recv(1024)

		self.s.send("Action: status\r\n\r\n")

		# Action Respose
		return self._get()

	def logoff(self):
		self.logdata.log('Action Logoff')
		self.s.send("Action: Logoff\r\n\r\n")
		self.s.close()

		
	def command(self, command=None):

		params = ["Action: command",]
		params.append("command: " + command)
		self.s.send("\r\n".join(params) + "\r\n\r\n")
		
		self.logdata.log('Action Command: %s' % command)		
		return self._get()


	def action(self, action=None, message=None, value=None):

		params = ["Action: " + action,]
		if (message):
			params.append(message + ": " + value)

		self.s.send("\r\n".join(params) + "\r\n\r\n")
		
		self.logdata.log('Action %s - Message: %s - Value: %s' % (action, message, value))
		return self._get()


	def _get(self):
		data = ""
		while (True):
			if ('\r\n\r\n' in data):
				break
			data += self.s.recv(1024)
			print data
			return data

