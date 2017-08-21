import sys
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui     import QPainter, QBrush, QFont, QColor, QPen, QDragEnterEvent, QDropEvent
from PyQt5.QtCore    import QPoint, QRect, QLine, QLineF, QRectF, QMimeData, Qt
from FlowGraphCore   import GraphNode
import SchemePainting 

class WCanvas(QWidget):
  
  def __init__(self):
    super().__init__()
    self.scheme = None
    self.mode   = 'N' # режим: 'N' - нормальный, 'M' - перемещение, 'L' - связывание
    self.newNode = None
    self.movingX = 0
    self.movingY = 0
    self.newLinkLine = QLineF(0, 0, 10, 10)
    self.nodeOutID = 0
    self.socketOutIndex = 0
    self.setAcceptDrops(True)

  # событие нажатия клавиши
  def keyPressEvent(self, e):
  
    if e.key() == Qt.Key_Delete:
      if self.scheme.selectionType == 'L':
        self.scheme.removeLink(self.scheme.selection.pop())
        self.scheme.clearSelection()
        self.repaint()
      elif self.scheme.selectionType == 'N':
        for nodeID in self.scheme.selection:
          self.scheme.removeNode(nodeID)
        self.scheme.clearSelection()
        self.repaint()
  
  # событие однократного клика мышкой  
  def mousePressEvent(self, e):
    
    selectionType = self.scheme.selectionType
  
    objectType, nodeID, objectID = self.scheme.objectAtPoint(e.pos()) 
    
    if objectType in ('N', 'SI', 'SO'):
      
      if e.modifiers() & Qt.ControlModifier:
        if nodeID in self.scheme.selection:
          self.scheme.removeNodeFromSelection(nodeID)
        else:
          self.scheme.addNodeToSelection(nodeID)
      else:
        if nodeID not in self.scheme.selection:
          self.scheme.clearSelection()
          self.scheme.addNodeToSelection(nodeID)
        
      self.repaint()
      
    elif objectType == 'L':
      
      self.scheme.addLinkToSelection(objectID)
      self.repaint()
      
    else:
      if self.scheme.selectionType != '-':
        self.scheme.clearSelection()  
        self.repaint()
        
    # включаем режим перемещения, если щелкнули на узле
    if objectType == 'N':
      self.setMouseTracking(True)
      self.mode = 'M'
      self.movingX = e.pos().x()
      self.movingY = e.pos().y()
    
    # включаем режим связывания, если щелкнули на выходном сокете
    if objectType == 'SO':
      self.nodeOutID = nodeID
      self.socketOutIndex = objectID
      self.setMouseTracking(True)
      self.mode = 'L'
      self.newLinkLine.setP1(self.scheme.socketLinkPoint(nodeID, 'O', objectID))
      self.newLinkLine.setP2(e.pos())

  def mouseMoveEvent(self, e):
    
    if self.mode == 'M':
      dx = e.pos().x() - self.movingX
      dy = e.pos().y() - self.movingY
      
      if (dx != 0) or (dy != 0):
        self.scheme.moveSelectedNodes(dx, dy)
        self.repaint()
        self.movingX = e.pos().x()
        self.movingY = e.pos().y()
        
    elif self.mode == 'L':
      self.newLinkLine.setP2( e.pos() )
      self.repaint()
        
  # событие однократного клика мышкой  
  def mouseReleaseEvent(self, e):
  
    if self.mode == 'M':
    
      self.setMouseTracking(False)
      self.mode = 'N'
      
    elif self.mode == 'L':
    
      self.setMouseTracking(False)
      self.mode = 'N'
      
      objectType, nodeID, objectID = self.scheme.objectAtPoint(e.pos()) 
      
      if (objectType == 'SI') and (self.nodeOutID != nodeID):
        self.scheme.linkNodes(self.nodeOutID, nodeID, self.socketOutIndex, objectID, 0)
      
      self.repaint()
        
  
  def dragEnterEvent(self, e):
  
    if e.mimeData().hasFormat('text/plain'):
      
      e.accept()
      
      nodeClassName = e.mimeData().text()
            
      self.newNode = self.scheme.createNode(nodeClassName, e.pos().x(), e.pos().y(), 150, 90)
      
      self.scheme.clearSelection()
 
    else:
      e.ignore()

#  def dragLeaveEvent(self, e):
#    self.mode = 'N'
#    self.newNode = None
#    self.repaint()
 
  def dropEvent(self, e):
    ll = e.pos().x() - self.newNode.width / 2
    tt = e.pos().y() - self.newNode.height / 2
    self.scheme.addNode(self.newNode.__class__.__name__, ll, tt, self.newNode.width, self.newNode.height)
    self.mode = 'N'
    self.newNode = None
    self.repaint()

  # событие рисования  
  def paintEvent(self, e):
  
    br = QBrush( QColor(255, 255, 255) )
    
    qp = QPainter()
    
    qp.begin(self)
    
    # фон
    qp.fillRect( self.rect(), br )
    
    isSelected = False
    
    # отрисовываем схему
    if self.scheme is not None:
    
      # узлы
      for node in self.scheme.nodes.values():
        if self.scheme.selectionType == 'N' and node.id in self.scheme.selection:
          isSelected = True
        else:
          isSelected = False
          
        SchemePainting.paintNode(qp, node, isSelected)

      # связи
      qp.save()
      
      for link in self.scheme.links.values():
        if self.scheme.selectionType == 'L' and link.id in self.scheme.selection:
          isSelected = True
        else:
          isSelected = False
          
        linkLine = self.scheme.calcLinkLine(link.id)
        SchemePainting.paintLink(qp, linkLine, isSelected)
      
      qp.restore()
      
      if self.mode == 'L':
        qp.drawLine(self.newLinkLine)
      
    qp.end()
