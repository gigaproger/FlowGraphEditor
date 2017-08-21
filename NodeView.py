import sys
from PyQt5.QtCore import QModelIndex, QMimeData, QPoint, QRect, QLine, Qt
from PyQt5.QtGui  import QPainter, QPixmap, QDrag
from PyQt5.QtWidgets import QTableView
import SchemePainting

class NodeView(QTableView):
  def __init__(self, parent = None):
    super(NodeView, self).__init__(parent)
  
  def startDrag(self, supportedActions):

    index = self.selectionModel().currentIndex()
    
    if ( not index.isValid() ):
      return

    indexList = list()
    indexList.append(index)
      
    mimeData = self.model().mimeData(indexList)
    
    node = self.parent().scheme.createNode(mimeData.text(), 0, 0, 150, 90)
    
    pixmap = QPixmap(151, 91)
    
    qp = QPainter(pixmap)

    qp.fillRect(QRect(0, 0, pixmap.width(), pixmap.height()), Qt.white)
    
    SchemePainting.paintNode(qp, node, False)
    
    node = None
    
    qp.end()
    
    drag = QDrag(self)
    
    drag.setMimeData(mimeData)
    drag.setHotSpot(QPoint(pixmap.width()/2, pixmap.height()/2))
    drag.setPixmap(pixmap)
    drag.exec(Qt.MoveAction)
    