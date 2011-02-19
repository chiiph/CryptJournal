from ui_cryptjournal import Ui_CryptJournal
from journal import Journal
from journalentry import JournalEntry

from PySide import QtCore, QtGui
import sys
import docutils.core

class CryptJournal(QtGui.QMainWindow):
  def __init__(self):
    super(CryptJournal,self).__init__()
    self._journal = None
    self._editing = False
    self._editing_id = -1
    self._loaded = -1
    self.ui = Ui_CryptJournal()
    self.ui.setupUi(self)

    self.ui.grpJournal.hide()
    self.ui.grpEdit.hide()
    self.ui.textEntry.hide()
    self.ui.toolBar.addAction(self.ui.actionAdd)
    self.ui.toolBar.addAction(self.ui.actionEdit)
    self.ui.toolBar.addAction(self.ui.actionDelete)
    self.ui.toolBar.addAction(self.ui.actionHide)
    self.ui.toolBar.hide()

    self.ui.linePassphrase.returnPressed.connect(self.create_journal)

    self.ui.actionAdd.triggered.connect(self.add)
    self.ui.actionDelete.triggered.connect(self.delete)
    self.ui.actionEdit.triggered.connect(self.edit)

    self.ui.buttonBox.clicked.connect(self.handle_add_buttons)
    self.ui.listEntries.itemDoubleClicked.connect(self.load_journal_entry)
    self.ui.listEntries.itemActivated.connect(self.load_journal_entry)
    
    self.show()

  def create_journal(self):
    key = self.ui.linePassphrase.text()
    if len(key) <= 0:
      return

    self.ui.grpPassphrase.hide()
    self.ui.grpJournal.show()
    self.ui.toolBar.show()
    self._journal = Journal(key)

    self.fill_journal_list()

  def fill_journal_list(self):
    self.ui.listEntries.clear()
    for entry in self._journal:
      item = QtGui.QListWidgetItem()
      item.setSizeHint(QtCore.QSize(0,65));
      self.ui.listEntries.addItem(item)
      self.ui.listEntries.setItemWidget(item, JournalEntry(data=entry))

  def load_journal_entry(self, entry):
    data = self.ui.listEntries.itemWidget(entry).data()

    if self.ui.textEntry.isVisible() and self._loaded == data["id"]:
      self._loaded = -1
      self.ui.textEntry.hide()
      return

    html = "<h1>"+data["title"]+"</h1>\n"
    html += "<h3><i>Last modified: "+data["date"]+"</i></h3>"
    html += self.parse_text(data["data"])

    self.ui.textEntry.setHtml(html)
    self.ui.textEntry.show()
    self._loaded = data["id"]

  def parse_text(self, text):
    parts = docutils.core.publish_parts(text, writer_name="html")
    html = parts['body'] 
    return html

  def add(self):
    self.ui.grpEdit.show()
    self.ui.lineTitle.setFocus()

  def delete(self):
    entry = self.ui.listEntries.currentItem()
    if entry is None:
      return
    res = QtGui.QMessageBox.question(self,"Are you sure?",\
        "Are you sure you want to delete this entry?",\
        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
    if res != QtGui.QMessageBox.Yes:
      return
    data = self.ui.listEntries.itemWidget(entry).data()
    self._journal.remove(data["id"])
    self.fill_journal_list()
  
  def edit(self):
    entry = self.ui.listEntries.currentItem()
    if entry is None:
      return
    self.ui.textEntry.hide()
    data = self.ui.listEntries.itemWidget(entry).data()
    self._editing = True
    self._editing_id = data["id"]
    self.ui.lineTitle.setText(data["title"])
    self.ui.textData.setPlainText(data["data"])
    self.ui.grpEdit.show()
    self.fill_journal_list()
  
  def handle_add_buttons(self, button):
    if button.text() == "Save":
      if self._editing and self._editing_id > -1:
        self._journal.edit(self._editing_id,\
            self.ui.lineTitle.text(),\
            self.ui.textData.toPlainText())
      else:
        self._journal.add(self.ui.lineTitle.text(),\
            self.ui.textData.toPlainText())

    self._editing = False
    self._editing_id = -1
    self.ui.lineTitle.clear()
    self.ui.textData.clear()
    self.ui.grpEdit.hide()
    self.fill_journal_list()

if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  c = CryptJournal()
  app.exec_()

