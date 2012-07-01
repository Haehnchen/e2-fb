from BaseScreens import Smb_BaseScreen, Smb_BaseEditScreen, Smb_BaseListScreen
from Components.MenuList import MenuList
from Tools.ASCIItranslit import legacyEncode

from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import eListboxPythonMultiContent, gFont
from Components.Label import Label

from Tools.LoadPixmap import LoadPixmap

import FacebookHelper
import hashlib
import os
from Components.Pixmap import Pixmap


from Components.Sources.List import List
#<widget name="myMenu" enableWrapAround="1" position="10,10" size="370,380" scrollbarMode="showOnDemand" />
class FB_Friends_MainMenu(Smb_BaseListScreen):
  skin ="""
       <screen position="center,center" size="630,450" title="">
            <widget name="myMenu" enableWrapAround="1" position="10,10" size="3,3" scrollbarMode="showOnDemand" />
      <widget source="feedlist" render="Listbox" position="10,10" size="410,400" zPosition="1" scrollbarMode="showOnDemand" transparent="1">
        <convert type="TemplatedMultiContent">
        {"templates":
          {"default": (50,[
              MultiContentEntryText(pos = (60, 1), size = (350, 28), font=1, flags = RT_HALIGN_LEFT | RT_VALIGN_TOP| RT_WRAP, text = 0), # index 0 is the name
              MultiContentEntryPixmapAlphaTest(pos = (0, 0), size = (100, 75), png = 1), # index 4 is the thumbnail
            ])
          },
          "fonts": [gFont("Regular", 22),gFont("Regular", 18),gFont("Regular", 26),gFont("Regular", 20)],
          "itemHeight": 77
        }
        </convert>
      </widget>
      
            <widget name="Description" position="330,210" size="230,380" font="Regular;18"/>

            <widget name="Statusbar" position="10,433" size="610,20" font="Regular;14"/>
            
        
            <widget name="profile" position="430,10" size="200,200"/> 

            <eLabel backgroundColor="#808080" position="0,428" size="630,1" />     
            <widget name="thumbnail" position="0,0" size="130,98" alphatest="on"/> # fake entry for dynamic thumbnail resizing, currently there is no other way doing this.    
        </screen>  
  """     
  
  backToMainMenu = True
  title = _("Your Friends")
  
  list = []
  
  def build(self):
     
    self.list = self.buildlist()
    self["myMenu"] = MenuList(self.list, False, eListboxPythonMultiContent)
    

    self["feedlist"] = List()
    self["thumbnail"] = Pixmap()
    self["profile"] = Pixmap()

    self['feedlist'].setList(self.list)    
    self["feedlist"].onSelectionChanged = [self.onMenuChanged]    
    
    self["Description"] = Label("")    
   
    #self.actions['down'] = self.keyDown
    
    self.context = ["ChannelSelectBaseActions","WizardActions", "DirectionActions","MenuActions","NumberActions","ColorActions"]
       
       
  def fetchFinished(self, string, parms):
    id = parms['index']
    profile_img = LoadPixmap(parms['img'])
    old = list(self.list[id])
    old[1] = profile_img
    
    self.list[id] = tuple(old)
    self['feedlist'].setList(self.list)

  def setFriendsCount(self):
    self.SetMessage('Currently %s Friends' % len(self.list))
  
    
  def buildlist(self):

    try:
      friends = FacebookHelper.FacebookApi().getFriendsFormated().data()
    except Exception as e:
      self.ErrorException(str(e))
      return
    
    for x in friends:
      #uname=x['name'].decode("utf-8")
      name = x['name'].encode('ascii', 'replace')
      
      profile_img = LoadPixmap(FacebookHelper.GetIconPath() + '/dummy.jpg')
      
      if x.get('img'):
        img = FacebookHelper.downloadImg(x.get('img'), self.fetchFinished, {'index':len(self.list)})
        if img is not None:
          profile_img = img

      self.list.append((name, profile_img, x))

    self.setFriendsCount()

    return self.list  
  


  def keyDown(self):
    #print self[self.currList].count()
    #
    #print self[self.currList].index

    self["feedlist"].selectNext()
    return
   
    #self.statuslist.append(( _("Fetching feed entries"), _("Trying to download the Youtube feed entries. Please wait..." ) ))    
    
    if self["myMenu"].getSelectionIndex() == len(self["myMenu"].list)-1:
      self["myMenu"].down()
      return
    
      print 'next page'
      self.list.append([
              'test',
              MultiContentEntryText(pos=(60, 0), size=(320, 25), font=0, text='test'),
              #MultiContentEntryText(pos=(60, 22), size=(320, 17), font=1, text=dreamclass.format_date(x['updated_on'])),
              #MultiContentEntryPixmapAlphaTest(pos=(5, 0), size=(50, 40), png = profile_img),
             'test'
              ])   
          
      self["myMenu"].l.setList(self.list)
      return
    
    #self["myMenu"].l.selectNext()
    #print 
    self["myMenu"].down()
    #getSelectionIndex
    
    #self["myMenu"].moveToIndex(last_index)
    #print 'nextpage'

  def onLargeProfileImage(self, string, parms):
    self["profile"].instance.setPixmap(LoadPixmap(parms['img']))
    

  def onMenuChanged(self,  test1 = ''):
    obj = self["feedlist"].getCurrent()
    if obj is False:
      return
    
    obj = obj[-1]
    img = FacebookHelper.downloadImg(obj['img_large'], self.onLargeProfileImage)
    
    if self["profile"].instance is not None:
      self["profile"].instance.setPixmap(img)


  
    