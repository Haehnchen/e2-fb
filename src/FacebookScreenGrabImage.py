import FacebookHelper
from BaseScreens import Smb_BaseEditScreen
from Components.config import getConfigListEntry, ConfigText, ConfigYesNo
from enigma import ePicLoad
from Components.AVSwitch import AVSwitch
from Components.Pixmap import Pixmap
import os

from enigma import eEPGCache
from RecordTimer import parseEvent
from Components.Sources.StaticText import StaticText

from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.ConfigList import ConfigListScreen, ConfigList

class FB_GrabImage_MainMenu(Smb_BaseEditScreen):
  skin = """
    <screen name="ConfigListScreen" position="center,center" size="560,400" title="Facebook - Post Screenshot">
      <ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />
      <ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />
      <ePixmap pixmap="skin_default/buttons/blue.png" position="420,0" size="140,40" alphatest="on" />
      <widget source="key_red" render="Label" position="0,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
      <widget source="key_green" render="Label" position="140,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
      <widget source="key_blue" render="Label" position="420,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
      <widget name="config" position="5,50" size="550,100" scrollbarMode="showOnDemand" zPosition="1"/>
      <widget name="myPic" position="5,120" size="550,280" zPosition="1" alphatest="on" />
    </screen>"""  

  
  path = '/tmp/facebook.jpg'

  def __init__(self, session, args=None):
    Screen.__init__(self, session)
    ConfigListScreen.__init__(self, [])    
    self.args = args
        
    self["key_red"] = StaticText(_("Cancel"))
    self["key_green"] = StaticText(_("OK"))
    self["key_blue"] = StaticText(_("Grab Image"))
    # SKIN Compat HACK!
    self["key_yellow"] = StaticText("")
    # EO SKIN Compat HACK!
    self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
    {
      "red": self.cancel,
      "blue": self.layoutFinished,
      "green": self.__SaveValues,
      "save": self.__SaveValues,
      "cancel": self.cancel,
      "ok": self.__SaveValues,
    }, -2)
        
    self.build()
    self.run()   
  
  def build(self):

    self.Scale = AVSwitch().getFramebufferScale()
    self.PicLoad = ePicLoad()
    self["myPic"] = Pixmap()
    
    self.PicLoad.PictureData.get().append(self.DecodePicture)
    self.onLayoutFinish.append(self.layoutFinished)
  
  def layoutFinished(self):
    try:
      self.path = FacebookHelper.GrabVideoImg()
    except Exception as e:
      print "Error:" + str(e)
        
    self.ShowPicture(self.path)
  
  def __SaveValues(self):
    values = {}
    for x in self["config"].list:
      values[x[2]] = x[1].getValue()

    result = self.save(values)
    self.close(result)   
  
  def buildlist(self):
    
    #current_channel = EPGNow.CurrentService(self.session).command()
    serviceref = self.session.nav.getCurrentlyPlayingServiceReference()
    service = self.session.nav.getCurrentService()
    
    info = service.info()
    
    default = {
      'servicename': info.getName(),
      'eventname': '',
      'comment': '',
    }
    
    epg = eEPGCache.getInstance()
    event = epg.lookupEventTime(serviceref, -1, 0)  
        
    if event is not None:
      curEvent = parseEvent(event)
      default['eventname'] = curEvent[2]
      #description = curEvent[3]
      #eventid = curEvent[4]  
    
    fields = [
       {'name': 'servicename', 'field': ConfigText(fixed_size = False) , 'text': _('Channellname'), 'value': default['servicename']},
       {'name': 'eventname', 'field': ConfigText(fixed_size = False) , 'text': _('Event-Name'), 'value': default['eventname']},
       {'name': 'comment', 'field': ConfigText(fixed_size = False) , 'text': _('Comment'), 'value': default['comment']},
       #{'name': 'grabimage', 'field': ConfigYesNo() , 'text': 'Attach Screenshot', 'value': True},       
      ]
    
    list = []
    
    for field in fields:
      field['field'].setValue(field['value'])
      list.append(getConfigListEntry(_(field['text']), field['field'], field['name']))
      
    return list
  
  def ShowPicture(self, url):
    if not os.path.exists(url):
      return
    
    self.PicLoad.setPara([
                          self["myPic"].instance.size().width(),
                          self["myPic"].instance.size().height(),
                          self.Scale[0],
                          self.Scale[1],
                          0,
                          1,
                          "#002C2C39"])
    
    self.PicLoad.startDecode(url)  
  
  def DecodePicture(self, PicInfo = ""):
    ptr = self.PicLoad.getData()
    self["myPic"].instance.setPixmap(ptr)  
  
  def save(self, values):
    
    fields = []
    
    if len(values['servicename']) > 0: fields.append(values['servicename'])
    if len(values['eventname']) > 0: fields.append(values['eventname'])
    if len(values['comment']) > 0: fields.append(values['comment'])
    
    msg = ' - '.join(fields)
 
    try:
      FacebookHelper.FacebookApi().postImage(self.path, msg)
    except Exception as e:
      return "Error:" + str(e)
          
    return _('Posted to wall')
