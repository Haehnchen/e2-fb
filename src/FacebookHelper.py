from Components.config import config, ConfigSubsection, configfile, ConfigText, ConfigYesNo
from FacebookApi import FacebookGraph
import os
import hashlib
from twisted.web import client

config.plugins.Facebook = ConfigSubsection()
config.plugins.Facebook.access_token = ConfigText()
config.plugins.Facebook.expires_on = ConfigText()
config.plugins.Facebook.external_curl = ConfigYesNo()

from Tools.LoadPixmap import LoadPixmap

def variable_get(name, default = None):
  vals = config.plugins.Facebook.getSavedValue()
  if name in vals:
    return vals[name]

  return default
 
def variable_set(name, value):
  getattr(config.plugins.Facebook, name).setValue(value)
  config.plugins.Facebook.save()
  configfile.save()  
  
def downloadImg(img, callback, parms = {}):
  img_hash = hashlib.md5(img).hexdigest()

  to = '/tmp/' + img_hash + '.' + 'jpg'
  parms['img'] = to    

  if os.path.exists(to) is True:
    return LoadPixmap(to)
        
  if os.path.exists(to) is False:
    client.downloadPage(img, to).addCallback(callback, parms)
      
  return None  
  
def FacebookApi():
  access_token = variable_get('access_token')
  if access_token  is None:
    raise Exception('unkown access_token')
  
  api = FacebookGraph(access_token)
  
  if bool(variable_get('external_curl', True)) is False:
    api.setRequestHandler('')
  
  return api

def GetIconPath():
  return os.path.dirname(os.path.realpath(__file__)) + '/icons/'

def GetIcon(string):
  filename = GetIconPath() + '/' + GetIconName(string)
  if os.path.exists(filename):
    return filename
  
  return GetIconPath() + 'plugin.png'
  
def GetIconName(string):
  if not string.endswith('.png'):
    string += '.png'
    
  return string.lower()

def GrabVideoImg(url = '/tmp/facebook.jpg'):
  ctrl = os.popen('grab -v -j 75 ' + url).read()
  if not "Done" in ctrl:
    raise IOError('image grabbing error')

  return url

def img_download(img, force_ext = None):
  img_hash = hashlib.md5(img).hexdigest()
  
  if force_ext is None:
    force_ext = url_img_ext(img)
  
  to = '/tmp/' + img_hash + '.' + force_ext
    
  if os.path.exists(to):
    return to

  client.downloadPage(img, to)
    
  if os.path.exists(to):
    return to
  
  return None

def url_img_ext(url):
  last_index = url.rfind('.') + 1;
  return url[last_index:]  