import sys
from PyQt5.QtGui     import QPainter, QBrush, QFont, QColor, QPen
from PyQt5.QtCore    import QPoint, QRect, QLine, QLineF, QRectF, Qt
from FlowGraphCore   import GraphNode

# возвращает перо для выделенных объектов
def makeSelectedPen():
  pen = QPen(QColor(0, 0, 255))
  pen.setStyle(Qt.DotLine)
  pen.setWidth(2)
  return pen

# рисование сокетов узла
def paintSockets(painter, sockets, direction, nodeLeft, nodeTop):
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

# рисование узла
def paintNode(painter, node, isSelected):
  
  simplePen = QPen(QColor(0, 0, 0))
  selectedPen = makeSelectedPen()
  
  headLineY = node.top + GraphNode.HEAD_HEIGHT
  nameLeft  = node.left + GraphNode.PICTURE_WIDTH + 2 
  headTextRect = QRect(nameLeft, node.top, node.left + node.width - nameLeft, headLineY - node.top)
  
  # каркас узла
  if isSelected:
    painter.setPen(selectedPen)
  else:
    painter.setPen(simplePen)
    
  painter.drawRect(node.left, node.top, node.width, node.height)
  
  painter.setPen(simplePen)
  
  painter.drawLine(node.left, headLineY, node.left + node.width, headLineY)
  painter.drawLine(nameLeft, node.top, nameLeft, headLineY)

  # значок
  painter.drawPixmap(node.left + 1, node.top + 1, node.picture)
  
  # название
  painter.drawText(headTextRect, Qt.AlignCenter, node.name)
      
  # сокеты
  paintSockets(painter, node.inputSockets, 'I', node.left, node.top)
  paintSockets(painter, node.outputSockets, 'O', node.left, node.top)

# рисование связи  
def paintLink(painter, linkLine, isSelected):
  simplePen = QPen(QColor(0, 0, 0))
  selectedPen = makeSelectedPen()
  
  if isSelected:
    painter.setPen(selectedPen)
  else:
    painter.setPen(simplePen)
  
  painter.drawLine(linkLine)  