import simplejson as json
import urllib2


class FacebookGraphResponse(object):

  response_array = {}
  
  def __init__(self, content = None):
    if content is not None: 
      self.response_array = json.loads(content)

  def data(self):
    return self.response_array['data']

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
  
  def __init__(self, access_token):
    self.access_token = access_token
  
  def getFriends(self):
    return FacebookGraphResponse(self._request(self._url("me/friends")))
    
  def getWall(self):
    return FacebookGraphResponse(self._request(self._url("me/home")))
    
  def getFriendsFormated(self):
    friends = FacebookGraphResponse(self._request(self._url("me/friends"))).raw()
    for i,v in enumerate(friends['data']):
      friends['data'][i]['img'] = self._friend_img(int(v['id']))
      
    return FacebookGraphResponse().setDataArray(friends)   

  def _friend_img(self, id):
    return self.fb_profil_img % id
    
      
  def _url(self, link):
    return self.fb_url + link + '?access_token=' + self.access_token
    
  def _request(self, url):
      req = urllib2.Request(url)
      return  str(urllib2.urlopen(req).read())
    