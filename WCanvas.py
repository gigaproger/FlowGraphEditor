import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui     import QPainter, QBrush, QFont, QColor
from PyQt5.QtCore    import QPoint, QRect, QLine, QRectF, Qt
from FlowGraphCore   import GraphNode

class WCanvas(QWidget):
  
  
  def __init__(self):
    super().__init__()
    self.scheme = None

  def paintSockets(self, painter, sockets, direction, nodeLeft, nodeTop):
    socketCount = len(sockets)
    
    brush = None
    
    if direction == 'I':
      brush = QBrush(QColor(255, 192, 192))
    elif direction == 'O':
      brush = QBrush(QColor(192, 192, 255))
    else:
      return
    
    for socket in sockets:
      socketRect = QRectF(nodeLeft + socket.left, nodeTop + socket.top, socket.width, socket.height)
      painter.fillRect(socketRect, brush)
      painter.drawText(socketRect, Qt.AlignCenter, socket.name)
   
  def paintNode(self, painter, node):
    
    headLineY = node.top + GraphNode.HEAD_HEIGHT
    nameLeft  = node.left + GraphNode.PICTURE_WIDTH + 2 
    headTextRect = QRect(nameLeft, node.top, node.left + node.width - nameLeft, headLineY - node.top)
    
    # каркас узла
    painter.drawRect(node.left, node.top, node.width, node.height)
    painter.drawLine(node.left, headLineY, node.left + node.width, headLineY)
    painter.drawLine(nameLeft, node.top, nameLeft, headLineY)

    # значок
    painter.drawPixmap(node.left + 1, node.top + 1, node.picture)
    
    # название
    painter.drawText(headTextRect, Qt.AlignCenter, node.name)
        
    # сокеты
    self.paintSockets(painter, node.inputSockets, 'I', node.left, node.top)
    self.paintSockets(painter, node.outputSockets, 'O', node.left, node.top)
    
  def paintLink(self, painter, linkLine):
    painter.drawLine(linkLine)
  
  def paintEvent(self, e):
  
    br = QBrush( QColor(255, 255, 255) )
    
    qp = QPainter()
    
    qp.begin(self)
    
    # фон
    qp.fillRect( self.rect(), br )
    
    # отрисовываем схему
    if self.scheme is not None:
    
      # узлы
      for node in self.scheme.nodes.values():
        self.paintNode(qp, node)

      # связи
      for link in self.scheme.links.values():
        linkLine = self.scheme.calcLinkLine(link.id)
        self.paintLink(qp, linkLine)
        
    qp.end()
