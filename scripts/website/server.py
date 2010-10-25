#    iCraft is Copyright 2010 both
#
#    The Archives team:
#                   <Adam Guy> adam@adam-guy.com AKA "Adam01"
#                   <Andrew Godwin> andrew@aeracode.org AKA "Aera"
#                   <Dylan Lukes> lukes.dylan@gmail.com AKA "revenant"
#                   <Gareth Coles> colesgareth2@hotmail.com AKA "gdude2002"
#
#    And,
#
#    The iCraft team:
#                   <Andrew Caluzzi> tehcid@gmail.com AKA "tehcid"
#                   <Andrew Dolgov> fox@bah.org.ru AKA "gothfox"
#                   <Andrew Horn> Andrew@GJOCommunity.com AKA "AndrewPH"
#                   <Brad Reardon> brad@bradness.co.cc AKA "PixelEater"
#                   <Clay Sweetser> CDBKJmom@aol.com AKA "Varriount"
#                   <James Kirslis> james@helplarge.com AKA "iKJames"
#                   <Jason Sayre> admin@erronjason.com AKA "erronjason"
#                   <Jonathon Dunford> sk8rjwd@yahoo.com AKA "sk8rjwd"
#                   <Joseph Connor> destroyerx100@gmail.com AKA "destroyerx1"
#                   <Joshua Connor> fooblock@live.com AKA "Fooblock"
#                   <Kamyla Silva> supdawgyo@hotmail.com AKA "NotMeh"
#                   <Kristjan Gunnarsson> kristjang@ffsn.is AKA "eugo"
#                   <Nathan Coulombe> NathanCoulombe@hotmail.com AKA "Saanix"
#                   <Nick Tolrud> ntolrud@yahoo.com AKA "ntfwc"
#                   <Noel Benzinger> ronnygmod@gmail.com AKA "Dwarfy"
#                   <Randy Lyne> qcksilverdragon@gmail.com AKA "goober"
#                   <Willem van der Ploeg> willempieeploeg@live.nl AKA "willempiee"
#
#    Disclaimer: Parts of this code may have been contributed by the end-users.
#
#    iCraft is licensed under the Creative Commons
#    Attribution-NonCommercial-ShareAlike 3.0 Unported License. 
#    To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
#    Or, send a letter to Creative Commons, 171 2nd Street,
#    Suite 300, San Francisco, California, 94105, USA.

import web
import json as simplejson
import socket
import configuration as config

urls=(
	'/', 'status',
	'/index', 'status',
	'/(.*).css', 'css'
)
render = web.template.render('templates/')

app = web.application(urls, globals())

BACKEND_HOST = config.host
BACKEND_PORT = config.port
BACKEND_PASSWORD = config.password

class BackendSocket(object):
	
	def __init__(self, host, port, password):
		#print "Connecting to %s:%s" % (host,port)
		self.skt = socket.socket()
		self.skt.connect((host, port))
		self.password = password
	
	def query(self, command, data=None):
		payload = {
			"command": command,
			"password": self.password,
		}
		if data:
			payload.update(data)
		self.skt.send(simplejson.dumps(payload)+"\r\n")
		response = self.skt.recv(1024)
		while response and "\n" not in response:
			response += self.skt.recv(1024)
			# If there's no response, connection lost
			if response == "":
				break
		# We might have not got anything
		if "\n" in response:
			result, response = response.split("\n", 1)
			return simplejson.loads(result)
		else:
			raise IOError
	
	def __del__(self):
		self.skt.close()
	

class status:
	def GET(self):
		bs = BackendSocket(BACKEND_HOST, BACKEND_PORT, BACKEND_PASSWORD)
		worlds = sorted(bs.query("userworlds")['worlds'])
		users = bs.query("users")['users']
		directors = bs.query("directors")['directors']
		admins = bs.query("Admins")['admins']
		mods = bs.query("Mods")['mods']
		members = bs.query("Members")['members']
		return render.status(directors, admins, mods, members, users, worlds)

class css:
 	def GET(self, css):
		styling = open(css+".css", 'rb')
		return styling.read()
		styling.close()

if __name__ == "__main__": app.run()

