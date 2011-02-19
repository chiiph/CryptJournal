from PySide.QtCore import QSettings

import crypt
import base64

class CryptSettings(QSettings):
  def __init__(self, key, parent=None):
    super(CryptSettings, self).\
        __init__(u"self", u"cryptjounal",\
                 parent=parent)
    self._key = key

  def key(self):
    """ Represents the encryption key """
    return self._key

#  @classmethod
  def setValue(self, key, value):
    encrypted_value = crypt.encode(self.key(), value)
    encoded_value = base64.b64encode(str(encrypted_value))
    super(CryptSettings, self).setValue(key,encoded_value)

#  @classmethod
  def value(self, key, defaultValue="", type=None):
    try:
      encoded_value = super(CryptSettings, self).\
          value(key, defaultValue=defaultValue)
      encrypted_value = base64.b64decode(encoded_value)
      return crypt.decode(self.key(), encrypted_value)
    except:
      return defaultValue

#  @classmethod
  def dump_all(self):
    for group in self.childGroups():
      print "Id:", group
      self.beginGroup(group)
      print "\tTitle:", self.value("title")
      print "\tDate:", self.value("date")
      print "\tData:", self.value("data")
      self.endGroup()

if __name__ == "__main__":
  c = CryptSettings(key="hola")
#  c.setValue("field1", "sarandaraaaaannnn")
  print c.value(key="field1", defaultValue="AA")
