import simplejson as json
import urllib2
import os

class FacebookGraphResponse(object):

  response_array = {}
 
  def __init__(self, content = None):
    if content is not None: 
      self.response_array = json.loads(content)
      self.checkError();

  def checkError(self):
    if not self.error() is None:
      raise Exception(str(self.error().get('message')))

  def data(self):
    return self.response_array['data']

  def error(self):
    return self.response_array.get('error')

  def setDataArray(self, ar):
    self.response_array = ar
    
    return self;

  def paging(self):
    return self.response_array['paging']
  
  def raw(self):
    return self.response_array

class FacebookGraph(object):
 
  fb_url = "https://graph.facebook.com/"
  fb_profil_img = 'http://graph.facebook.com/%s/picture?type=square'
  fb_profil_img_large = 'http://graph.facebook.com/%s/picture?type=large'
  
  request_handler = 'curl'
  
  def __init__(self, access_token):
    self.access_token = access_token
  
  def setRequestHandler(self, value):
    self.request_handler = value
  
  def getFriends(self):
    return FacebookGraphResponse(self._request(self._url("me/friends")))
    
  def getWall(self):
    return FacebookGraphResponse(self._request(self._url("me/home")))
    
  def getFriendsFormated(self):
    friends = FacebookGraphResponse(self._request(self._url("me/friends"))).raw()
    for i,v in enumerate(friends['data']):
      friends['data'][i]['img'] = self._friend_img(int(v['id']))
      friends['data'][i]['img_large'] = self._friend_img(int(v['id']), 'large')
      
    return FacebookGraphResponse().setDataArray(friends)   

  def _friend_img(self, id, type = 'square'):
    if type is 'square':
      return self.fb_profil_img % id
    if type is 'large':
      return self.fb_profil_img_large % id
      
  def _url(self, link):
    return self.fb_url + link + '?access_token=' + self.access_token
    
  def postImage(self, img, msg = ''):
    if not os.path.exists(img):
      raise IOError('Img not found:' + str(img))
      
    url = self._url("me/photos")
    
    if self.request_handler is 'curl':
      response = self._cmd("-F 'source=@/%s' -F 'message=%s' %s" % (img, msg, url))
      return FacebookGraphResponse(response)
    else:
      raise IOError('only curl support current')
    
    
    
  def _cmd(self, cmd):
    test = os.popen('curl -s -k ' + cmd).read()
    print 'curl -s -k ' + cmd
    print test
    return test
    
  def LongLifeToken(self):
    pass    
    
  def _request(self, url):
    if self.request_handler is "curl":
      return self._cmd(url)
    
    req = urllib2.Request(url)
    return  str(urllib2.urlopen(req).read())
    