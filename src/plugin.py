import os
from twisted.web import resource, http
from Plugins.Plugin import PluginDescriptor
import urllib
from FacebookHelper import variable_set, variable_get

from twisted.web.util import redirectTo

import BaseScreens
#import FacebookScreenFriends
import FacebookScreenMain


def main(session, **kwargs):
	reload(FacebookScreenMain)
	try:
		session.open(FacebookScreenMain.FB_MainMenu)
	except:
		print 'errr'	
		#import traceback
		#traceback.print_exc()

class FacebookWebAuth(resource.Resource):

	req = None

	def render_GET(self, req):
		self.req = req
		
		access_token = req.args.get("access_token", None)
		local_url = str(req.prePathURL())
		
		if access_token is None:
			red = 'http://www.espend.de/fb.php?local=' + local_url
			auth_url = "https://www.facebook.com/dialog/oauth?client_id=440490789296919&scope=read_stream,read_friendlists,publish_stream,read_mailbox,friends_online_presence&redirect_uri=%s&response_type=token" % urllib.quote_plus(red)
			
			return redirectTo(auth_url, req)
			#return '<iframe id="test" src="' + auth_url +  '" width="90%" height="400"><p>Ihr Browser kann leider keine eingebetteten Frames anzeigen</p></iframe>'

				
			#return str(req.getHeader.keys())
			#return str(url) + 'hello world: ' + str(req.getRequestHostname()) + str(req.uri) + str(req.getHost()) 
		
		variable_set('access_token', str(self.GET('access_token')))
		variable_set('expires_in', str(self.GET('expires_in')))

		jsonp_callback = req.args.get("jsonp_callback", None)
		return str(jsonp_callback[0]) + '({"msg":"box ok"})';
		
		return str(access_token)
	
	def GET(self, var):
		return self.req.args.get(var, None)[0]

def Plugins(path, **kwargs):
		return [
		##			PluginDescriptor(where = [PluginDescriptor.WHERE_SESSIONSTART, PluginDescriptor.WHERE_AUTOSTART], fnc = autostart),
					PluginDescriptor(name="Facebook", description="Facebook",where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main),
					PluginDescriptor(name="Facebook", where = PluginDescriptor.WHERE_EXTENSIONSMENU, icon="plugin.png", fnc=main),
          PluginDescriptor(where=PluginDescriptor.WHERE_SESSIONSTART, fnc=sessionstart, needsRestart=False)
    ]

def sessionstart(reason, **kwargs):                                               
	if reason == 0 and "session" in kwargs:                                                        
		if os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebChilds/Toplevel.py"):
			from Plugins.Extensions.WebInterface.WebChilds.Toplevel import addExternalChild
			addExternalChild( ("Facebook", FacebookWebAuth(), "Facebook", "1", True) )          
		else:                                                                                  
			print "[Facebook] Webif not found"