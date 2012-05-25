from Screens.Screen import Screen

from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Tools.LoadPixmap import LoadPixmap
from Components.MenuList import MenuList
from Components.Label import Label
from enigma import eListboxPythonMultiContent, gFont
from Components.ActionMap import ActionMap

import FacebookHelper

class FB_MainMenu(Screen):

  skin = """
  <screen name="Smb_MainMenu" position="center,center" size="460,400" title="Facebook - Main Menu" >
    <widget name="myMenu" position="10,10" size="420,370" scrollbarMode="showOnDemand" />
    <widget name="Statusbar" position="10,387" size="530,20" font="Regular;13"/>
  </screen>
 
  """

  def buildlist(self):

    if FacebookHelper.variable_get('access_token', None) is None:
      self.SetMessage('Please register your box to Facebook App!')
    
    api = []
    api.append({'name': _("Upload Screen"), 'description': _('Upload current video screenshot with event info'), 'func': self.actions.postimage, 'icon': 'post'})
    api.append({'name': _("Friends"), 'description': _('Your Friends'), 'func': self.actions.Friends, 'icon': 'friends'})
    api.append({'name': _("Wall"), 'description': _('FB Wall'), 'func': self.actions.Wall, 'icon': 'wall'})
    api.append({'name': _("Settings"), 'description': _('Some settings'), 'func': self.actions.Settings, 'icon': 'settings'})
    
   
    list = []
    
    for x in api:
      png = LoadPixmap(FacebookHelper.GetIcon(x['icon']))
        
      obj = [
            x,
              MultiContentEntryText(pos=(60, 0), size=(335, 25), font=0, text=x['name']),
              MultiContentEntryText(pos=(62, 22), size=(335, 17), font=1, text=x['description']),
              MultiContentEntryPixmapAlphaTest(pos=(5, 0), size=(50, 40), png = png),
        ]
          
      #if x.has_key('needaccess') and self.itemaccess(x['needaccess']) is False:
      #  obj.append(MultiContentEntryPixmapAlphaTest(pos=(395, 5), size=(20, 20), png = access))
        
      list.append(obj)  
        
    return list 



  def reset(self):
    print 'reset'

  def cancel(self):
    print "\n[MyMenu] cancel\n"
    self.close(None)

  def MsgCallback(self, back = None):
    self.SetMessage()
    if back is None:
      return
    
    self.SetMessage(str(back))

  def __init__(self, session, args = 0):
    self.session = session
    
     
    list = []

    Screen.__init__(self, session)
    #self["myMenu"] = MenuList(list)

    self["Statusbar"] = Label('')
    
    self["myMenu"] = MenuList(self.buildlist(), False, eListboxPythonMultiContent)
    
    self["myMenu"].l.setFont(0, gFont("Regular", 20))
    self["myMenu"].l.setFont(1, gFont("Regular", 14))
    self["myMenu"].l.setItemHeight(40)   
        
    self["myActionMap"] = ActionMap(["SetupActions"],    
    {
      "ok": self.go,
      "cancel": self.cancel
    }, -1)

  #def itemaccess(self, item):
  #  return dreamclass.GetAccess(item) == True

  def SetMessage(self, msg = ''):
      self["Statusbar"].text = str(msg)  

  def rebuild(self):
    self["myMenu"].setList(self.buildlist())

  def go(self):
    
    try:
      returnItems = self["myMenu"].l.getCurrentSelection()[0]
      returnValue = returnItems['func']
      
      if returnItems.has_key('needaccess') and self.itemaccess(returnItems['needaccess']) is False:
        self.SetMessage('no access')
        return    
      
      returnValue(self, returnItems)
      return
          
    except Exception, e:
      self.SetMessage(str(e))
      print 'Error:', e        

  class actions(object):
  
    @staticmethod
    def Friends(YourScreen, item):
      import FacebookScreenFriends
      reload(FacebookScreenFriends)
      YourScreen.session.open(FacebookScreenFriends.FB_Friends_MainMenu)
      
    @staticmethod
    def Wall(YourScreen, item):
      import FacebookScreenWall
      reload(FacebookScreenWall)
      YourScreen.session.open(FacebookScreenWall.FB_Wall_MainMenu)     
      
    @staticmethod
    def postimage(YourScreen, item):
      import FacebookScreenGrabImage
      reload(FacebookScreenGrabImage)
      YourScreen.session.openWithCallback(YourScreen.MsgCallback, FacebookScreenGrabImage.FB_GrabImage_MainMenu)

    @staticmethod
    def Settings(YourScreen, item):
      import FacebookScreenSettings
      reload(FacebookScreenSettings)
      YourScreen.session.openWithCallback(YourScreen.MsgCallback, FacebookScreenSettings.FB_Settings_MainMenu) 
  