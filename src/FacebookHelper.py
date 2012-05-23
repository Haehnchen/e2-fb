from Components.config import config, ConfigSubsection, configfile, ConfigText
from FacebookApi import FacebookGraph
import os
import hashlib
from twisted.web import client

config.plugins.Facebook = ConfigSubsection()
config.plugins.Facebook.access_token = ConfigText()
config.plugins.Facebook.expires_in = ConfigText()


def variable_get(name, default = None):
  vals = config.plugins.Facebook.getSavedValue()
  if name in vals:
    return vals[name]

  return default
 
def variable_set(name, value):
  getattr(config.plugins.Facebook, name).setValue(value)
  config.plugins.Facebook.save()
  configfile.save()  
  
def FacebookApi():
  #access_token = "AAAGQn8EF2xcBAIZBqxY5SloR51vJmFgsopBLqSQouyI1ZA3QAgZB8ywMHqWnGIt6lTN0V2yHUCBpJmrtIahCa5lY8I9z5BCn33Ojz8zPLc0AMdZA4GVZB"
  access_token = variable_get('access_token')
  return FacebookGraph(access_token)

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

def img_download(img):
  img_hash = hashlib.md5(img).hexdigest()
  to = '/tmp/' + img_hash + '.' + url_img_ext(img)
  print img
  print to
    
  if os.path.exists(to):
    return to

  client.downloadPage(img, to)
    
  if os.path.exists(to):
    return to
  
  return None

def url_img_ext(url):
  last_index = url.rfind('.') + 1;
  return url[last_index:]  