import sys
from PyQt5.QtWidgets import QApplication
from WMain import WMain

if __name__ == '__main__':
  app = QApplication(sys.argv)
  
  w = WMain()
  w.showMaximized()
  
  sys.exit(app.exec_())