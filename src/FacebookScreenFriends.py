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

from twisted.web import client

class FB_Friends_MainMenu(Smb_BaseListScreen):
  backToMainMenu = True
  title = _("Your Friends")
  
  list = []
  
  def build(self):
     
    self.list = self.buildlist()
    self["myMenu"] = MenuList(self.list, False, eListboxPythonMultiContent)

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
    
    self.actions['down'] = self.keyDown
    
    #self.actions['red'] = self.ActionHelperDownload
    #self.actions['green'] = self.ActionHelperUpload
    #self.actions['yellow'] = self.ActionHelperEdit
    #self.actions['blue'] = self.ActionHelperDelete
    #self.actions['0'] = self.ActionHelperAdd
    
    self.context = ["ChannelSelectBaseActions","WizardActions", "DirectionActions","MenuActions","NumberActions","ColorActions"]
        
  def buildlist(self):
    
    list = []

    try:
      friends = FacebookHelper.FacebookApi().getFriendsFormated().data()
    except Exception as e:
      self.ErrorException(e)
      return
    
    for x in friends:
      #name = str(x['name'])
      name = x['name'].encode('ascii', 'ignore')

      profile_img = LoadPixmap(FacebookHelper.GetIconPath() + '/dummy.jpg')
      
      if x.get('img', None):
        img = x.get('img', None)
        img_hash = hashlib.md5(img).hexdigest()

        #FacebookHelper.url_img_ext(img)
        to = '/tmp/' + img_hash + '.' + 'jpg' 
        if os.path.exists(to) is False:
          print 'Download: ' + img
          client.downloadPage(img, to)

        if os.path.exists(to) is True:
          profile_img = LoadPixmap(to)

      list.append([
            name,
            MultiContentEntryText(pos=(60, 0), size=(320, 25), font=0, text=name),
            #MultiContentEntryText(pos=(60, 22), size=(320, 17), font=1, text=dreamclass.format_date(x['updated_on'])),
            MultiContentEntryPixmapAlphaTest(pos=(5, 0), size=(50, 40), png = profile_img),
            x
    ])


    return list  

  def keyDown(self):
    #print self[self.currList].count()
    #
    #print self[self.currList].index

    
   
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

  def onMenuChanged(self, item):
    obj = item[-1]
    items = {
          #'Update': dreamclass.format_date(obj.get('content_updated')),
          #'Orbitals': str(obj.get('orbitals')),
          #'Comment': str(obj.get('comment')),
          }

    self.DescriptionToText(items)      
  
    