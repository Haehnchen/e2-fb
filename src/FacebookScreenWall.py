from BaseScreens import Smb_BaseScreen, Smb_BaseEditScreen, Smb_BaseListScreen
from Components.MenuList import MenuList
from Tools.ASCIItranslit import legacyEncode

from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import eListboxPythonMultiContent, gFont
from Components.Label import Label

import hashlib

from Tools.LoadPixmap import LoadPixmap

from twisted.web import client
import FacebookHelper

class FB_Wall_MainMenu(Smb_BaseListScreen):
  backToMainMenu = True
  title = _("Your Wall")
  
  def build(self):
     
    self["myMenu"] = MenuList(self.buildlist(), False, eListboxPythonMultiContent)
    #self.act = self.myaction(self)
    
    self["myMenu"].l.setFont(0, gFont("Regular", 20))
    self["myMenu"].l.setFont(1, gFont("Regular", 14))
    self["myMenu"].l.setItemHeight(40)   
    
    #self["myMenu"].onSelectionChanged = [self.Changed]
    
    self["Description"] = Label("")    
    
    self["red"] = Label("Download")
    self["green"] = Label("Upload")
    self["yellow"] = Label("Edit")
    self["blue"] = Label("Delete")    
    
    #self.actions['red'] = self.ActionHelperDownload
    #self.actions['green'] = self.ActionHelperUpload
    #self.actions['yellow'] = self.ActionHelperEdit
    #self.actions['blue'] = self.ActionHelperDelete
    #self.actions['0'] = self.ActionHelperAdd
    
    self.context = ["ChannelSelectBaseActions","WizardActions", "DirectionActions","MenuActions","NumberActions","ColorActions"]
        
  def buildlist(self):
    
    list = []

    #png = boxwrapper.Icon("channellist_list")

    try:
      wall = FacebookHelper.FacebookApi().getWall().data()
    except Exception as e:
      self.ErrorException(str(e))
      return
    
    dummy_img = LoadPixmap(FacebookHelper.GetIconPath() + '/dummy.jpg')
    
    for x in wall:
      #name = str(x['name'])
      
      msg = x.get('message', '').encode('ascii', 'ignore')
      name = x.get('name', '').encode('ascii', 'ignore')
      
      if str(x.get('type', '')) is 'photo':
        msg = x.get('story', '').encode('ascii', 'ignore')
      
      if str(x.get('type', '')) is 'status':
        msg = x.get('story', '').encode('ascii', 'ignore')      
      
      if x.get('from', None):
        name = x['from'].get('name', '').encode('ascii', 'ignore')
      
      if msg is '':
        msg = x.get('story', '').encode('ascii', 'ignore')  


      
      img = x.get('picture', None)
      
      pixmap = dummy_img
      
      #http://external.ak.fbcdn.net/safe_image.php?d=AQB5kTNOiq63sj4f&w=90&h=90&url=http\u00253A\u00252F\u00252Fbilder.bild.de\u0
      if img is not None and img.find("external") == -1:
        path = FacebookHelper.img_download(str(img))
        if path:
          pixmap = LoadPixmap(path)
        

        
        
      #if x.get('picture', None):
      #  img = x.get('picture', None)
      #  to = '/tmp/'
      #  client.downloadPage(x.get('picture', None)).addCallback(self.fetchFinished,str(tubeid)).addErrback(self.fetchFailed,str(tubeid))

      list.append([
            msg,
            MultiContentEntryText(pos=(60, 0), size=(320, 20), font=0, text=msg),
            MultiContentEntryText(pos=(60, 22), size=(320, 17), font=1, text=name),
            MultiContentEntryPixmapAlphaTest(pos=(5, 0), size=(50, 40), png = pixmap),
            x
    ])

    return list  

  def onMenuChanged(self, item):
    obj = item[-1]
    items = {
          'ID': obj.get('id'),
          'Picture': obj.get('picture', '').encode('ascii', 'ignore'),
          'Description': obj.get('description', '').encode('ascii', 'ignore'),
          
          }

    self.DescriptionToText(items)      
