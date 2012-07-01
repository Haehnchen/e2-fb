from BaseScreens import Smb_BaseScreen, Smb_BaseEditScreen, Smb_BaseListScreen
from Components.MenuList import MenuList
from Tools.ASCIItranslit import legacyEncode

from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import eListboxPythonMultiContent, gFont
from Components.Label import Label
from urlparse import urlparse

import hashlib
import cgi

from Tools.LoadPixmap import LoadPixmap
from Components.Sources.List import List

from twisted.web import client
import FacebookHelper

class FB_Wall_MainMenu(Smb_BaseListScreen):
  backToMainMenu = True
  title = _("Your Wall")
  list = []
  
  skin ="""
       <screen position="center,center" size="630,450" title="">
            <widget name="myMenu" enableWrapAround="1" position="10,10" size="3,3" scrollbarMode="showOnDemand" />
      <widget source="feedlist" render="Listbox" position="10,10" size="410,400" zPosition="1" scrollbarMode="showOnDemand" transparent="1">
        <convert type="TemplatedMultiContent">
        {"templates":
          {"default": (50,[
              MultiContentEntryText(pos = (60, 1), size = (350, 28), font=1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP| RT_WRAP, text = 0), # index 0 is the name
              MultiContentEntryText(pos = (60, 23), size = (350, 28), font=0, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP| RT_WRAP, text = 1), # index 0 is the name
              MultiContentEntryPixmapAlphaTest(pos = (0, 0), size = (100, 75), png = 2), # index 4 is the thumbnail
            ])
          },
          "fonts": [gFont("Regular", 14),gFont("Regular", 18),gFont("Regular", 26),gFont("Regular", 20)],
          "itemHeight": 77
        }
        </convert>
      </widget>
      
            <widget name="Description" position="402,10" size="230,380" font="Regular;18"/>

                    
            <widget name="red" position="10,394" size="120,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>
            <widget name="green" position="140,394" size="120,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>
            <widget name="yellow" position="270,394" size="120,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>
            <widget name="blue" position="400,394" size="120,30" valign="center" halign="center" zPosition="1" transparent="1" foregroundColor="white" font="Regular;18"/>

            <ePixmap name="pred" position="10,392" size="120,30" zPosition="0" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on"/>
            <ePixmap name="pgreen" position="140,392" size="120,30" zPosition="0" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on"/>
            <ePixmap name="pyellow" position="270,392" size="120,30" zPosition="0" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on"/>
            <ePixmap name="pblue" position="400,392" size="120,30" zPosition="0" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on"/>
            
            <ePixmap name="padd" position="530,397" size="120,30" zPosition="0" pixmap="skin_default/buttons/key_0.png" transparent="1" alphatest="on"/>
            <eLabel name="padd_label" text="Add" position="570,397" size="50,25" font="Regular;19" transparent="1" />
            
            <widget name="Statusbar" position="10,433" size="610,20" font="Regular;14"/>
            
            <eLabel backgroundColor="#808080" position="391,0" size="1,390" />            
            <eLabel backgroundColor="#808080" position="0,390" size="630,1" />
            <eLabel backgroundColor="#808080" position="0,428" size="630,1" />         
        </screen>  
  """      
  
  def build(self):
     
    #self["myMenu"] = MenuList(self.buildlist(), False, eListboxPythonMultiContent)
    #self.act = self.myaction(self)
    
    #
    #self["myMenu"].l.setFont(0, gFont("Regular", 20))
    #self["myMenu"].l.setFont(1, gFont("Regular", 14))
    #self["myMenu"].l.setItemHeight(40)   
    
    #self["myMenu"].onSelectionChanged = [self.Changed]
    
    self.list = self.buildlist()
    self["myMenu"] = MenuList(self.list, False, eListboxPythonMultiContent)
  
    
    self["feedlist"] = List()
    self['feedlist'].setList(self.list) 
    import pprint
    pprint.pprint(self.list) 

    #self["feedlist"].onSelectionChanged = [self.onMenuChanged]        
    
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
      
      if img is not None and img.find("external") == -1:
        path = FacebookHelper.img_download(str(img))
        if path:
          pixmap = LoadPixmap(path)
          
      if img is not None and "external" in img:
          o = cgi.parse_qs(urlparse(img).query)
          url = o.get('url')[0].encode("utf-8")
          if url:
            path = FacebookHelper.img_download(str(img), FacebookHelper.url_img_ext(url))
            if path:
              pixmap = LoadPixmap(path)

      print name
      self.list.append((name, msg, pixmap, x))
#, pixmap, x
      #list.append([
      #      msg,
      #      MultiContentEntryText(pos=(60, 0), size=(320, 20), font=0, text=msg),
      #      MultiContentEntryText(pos=(60, 22), size=(320, 17), font=1, text=name),
      #      MultiContentEntryPixmapAlphaTest(pos=(5, 0), size=(50, 40), png = pixmap),
      #      x
      #])

    return self.list  

  def onMenuChanged(self, item = None):
    obj = self["feedlist"].getCurrent()
    if obj is False:
      return
    
    obj = obj[-1]
    items = {
          'ID': obj.get('id'),
          'Picture': obj.get('picture', '').encode('ascii', 'ignore'),
          'Description': obj.get('description', '').encode('ascii', 'ignore'),
          }

    self.DescriptionToText(items)      
