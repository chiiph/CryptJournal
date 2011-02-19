from cryptsettings import CryptSettings
import datetime
from datetime import datetime

class Journal(object):
  def __init__(self, key):
    self._db = CryptSettings(key)
    self._last_id = int(self.db().value("last_id", "-1"))
    self._date_format = "%d/%m/%y %H:%M"

  def db(self):
    return self._db

  def last_id(self):
    return self._last_id

  def date_format(self):
    return self._date_format

  def add(self, title, data):
    new_id = str(self.last_id() + 1)
    self._last_id = int(new_id)

    self.db().beginGroup(new_id)
    self.db().setValue("title", title)
    self.db().setValue("data", data)
    self.db().setValue("date", datetime.today().strftime(self.date_format()))
    self.db().endGroup()

    self.db().setValue("last_id", str(self._last_id))

    self.db().sync()

  def remove(self, id):
    self.db().remove(id)

  def edit(self, id, title, data):
    self.db().beginGroup(id)
    self.db().setValue("title", title)
    self.db().setValue("data", data)
    self.db().setValue("date", datetime.today().strftime(self.date_format()))
    self.db().endGroup()

    self.db().sync()

  def __getitem__(self, id):
    if id > len(self.db().childGroups()):
      raise IndexError("There's no such entry")
    data = {}
    real_id = self.db().childGroups()[id]
    self.db().beginGroup(real_id)
    data["id"] = real_id
    data["title"] = self.db().value("title")
    data["data"] = self.db().value("data")
    data["date"] = self.db().value("date")
    self.db().endGroup()
    return data
  
  def __setitem__(self, id, data):
    if str(id) in self.db().childGroups():
      self.edit(self, str(id), data["title"], data["data"])
    else:
      self.add(self, data["title"], data["data"])

  def __len__(self):
    return len(self.db().childGroups())
