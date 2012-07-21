import os
from twisted.web import resource, http
from Plugins.Plugin import PluginDescriptor
import urllib
from FacebookHelper import variable_set, variable_get

from twisted.web.util import redirectTo

import BaseScreens
import FacebookScreenMain
from time import time


def main(session, **kwargs):
	reload(FacebookScreenMain)
	try:
		session.open(FacebookScreenMain.FB_MainMenu)
	except:
		print 'errr'	

class FacebookWebAuth(resource.Resource):

	req = None

	def render_GET(self, req):
		self.req = req
		
		access_token = req.args.get("access_token", None)
		local_url = str(req.prePathURL())
		
		if access_token is None:
			red = 'http://www.espend.de/fb/?local=' + local_url
			auth_url = "https://www.facebook.com/dialog/oauth?client_id=440490789296919&scope=read_stream,read_friendlists,publish_stream,read_mailbox,friends_online_presence&redirect_uri=%s&response_type=token" % urllib.quote_plus(red)
			
			return redirectTo(auth_url, req)
		
		variable_set('access_token', str(self.GET('access_token')))
		variable_set('expires_on', str(int(self.GET('expires_in')) + time()))

		jsonp_callback = req.args.get("jsonp_callback", None)
		return str(jsonp_callback[0]) + '({"msg":"box ok"})';
	
	def GET(self, var):
		return self.req.args.get(var, None)[0]

def Plugins(path, **kwargs):
		return [
					PluginDescriptor(name="Facebook", description="Facebook",where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main),
					PluginDescriptor(name="Facebook", where = PluginDescriptor.WHERE_EXTENSIONSMENU, icon="plugin.png", fnc=main),
          PluginDescriptor(where=PluginDescriptor.WHERE_SESSIONSTART, fnc=sessionstart, needsRestart=False)
    ]

def sessionstart(reason, **kwargs):                                               
	if reason == 0 and "session" in kwargs:                                                        
		if os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebChilds/Toplevel.py"):
			from Plugins.Extensions.WebInterface.WebChilds.Toplevel import addExternalChild
			addExternalChild( ("fb", FacebookWebAuth(), "Facebook", "1", True) )          
		else:                                                                                  
			print "[Facebook] Webif not found"