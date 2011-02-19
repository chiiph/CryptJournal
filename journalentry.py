from PySide.QtGui import QWidget,QLabel,QVBoxLayout

class JournalEntry(QWidget):
  def __init__(self, data, parent = None):
    super(JournalEntry, self).__init__(parent)
    self._data = data

    self.lblDate = QLabel()
    self.lblTitle = QLabel()

    self.lblTitle.setText("<b>"+data["title"]+"</b>")
    self.lblDate.setText("<i>Last modified: "+data["date"]+"</i>")

    layout = QVBoxLayout()
    layout.addWidget(self.lblTitle)
    layout.addWidget(self.lblDate)
    self.setLayout(layout)
    self.show()

  def data(self):
    return self._data
