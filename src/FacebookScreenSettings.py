from Plugins.Extensions.ShareMyBox import boxwrapper, dreamclass
from FacebookHelper import variable_set, variable_get
from Plugins.Extensions.ShareMyBox.ShareMyBoxRequets import ShareMyBoxApi as Request 

from BaseScreens import Smb_BaseEditScreen
from Components.config import getConfigListEntry, ConfigText, ConfigYesNo

class FB_Settings_MainMenu(Smb_BaseEditScreen):
  
  def buildlist(self):

    fields = [
       {'name': 'external_curl', 'field': ConfigYesNo() , 'text': 'Use external curl (if Python install doesnt support https)', 'value': bool(variable_get('external_curl', True))},
      ]
    
    list = []
    for field in fields:
      field['field'].setValue(field['value'])
      list.append(getConfigListEntry(_(field['text']), field['field'], field['name']))
      
    return list
  
  def save(self, values):
    print values['external_curl']
    variable_set('external_curl', bool(values['external_curl']))
    return _('Settings saved')
          
