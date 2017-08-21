import sys
import json
from PyQt5.QtGui import QPixmap, QPolygonF
from PyQt5.QtCore import QLineF, QPointF, QRectF, Qt


# Сокет
class GraphSocket(object):
  
  def __init__(self, name, direction, x, y, w, h):
    
    self.name = name
    self.direction = direction

    self.left   = x
    self.top    = y
    self.width  = w
    self.height = h

    self.linkID = None
    
# Абстрактный узел    
class GraphNode(object):

  # константы рисования
  HEAD_HEIGHT = 34
  PICTURE_WIDTH = 32
  DEFAULT_SOCKET_WIDTH = 30
  DEFAULT_SOCKET_HEIGHT = 15
  INTER_SOCKET_HEIGHT = 5

  def __init__(self, id, name, x, y, w, h):
    self.id = id
    self.name   = name
    self.left   = x
    self.top    = y
    self.width  = w
    self.height = h
    
    self.inputSockets = list()
    self.outputSockets = list()
    
    self.picture = QPixmap( self.pictureFileName() )
    
    self.makeSockets()
    
    self.arrangeSockets('I')
    self.arrangeSockets('O')
    
  def makeSockets(self):
    pass

  def attachLink(self, direction, socketIndex, linkID):
    if direction == 'I':
      self.inputSockets[socketIndex].linkID = linkID
    elif direction == 'O':
      self.outputSockets[socketIndex].linkID = linkID
 
  def detachLink(self, direction, socketIndex):
    if direction == 'I':
      self.inputSockets[socketIndex].linkID = None
    elif direction == 'O':
      self.outputSockets[socketIndex].linkID = None
      
  def arrangeSockets(self, direction):
    ss = None

    if direction == 'I':
      ss = self.inputSockets
    elif direction == 'O':
      ss = self.outputSockets
    else:
      return
    
    socketCount = len(ss)
    
    if socketCount == 0:
      return
      
    socketSpace = socketCount * GraphNode.DEFAULT_SOCKET_HEIGHT + (socketCount - 1) * GraphNode.INTER_SOCKET_HEIGHT
    
    socketTop = GraphNode.HEAD_HEIGHT
    socketTop += (self.height - GraphNode.HEAD_HEIGHT) / 2 - socketSpace / 2
      
    for socket in ss:
    
      if direction == 'I':
        socket.left = 1
        socket.top  = socketTop
        
      elif direction == 'O':
        socket.left = self.width - GraphNode.DEFAULT_SOCKET_WIDTH
        socket.top  = socketTop
      
      socketTop += GraphNode.DEFAULT_SOCKET_HEIGHT + GraphNode.INTER_SOCKET_HEIGHT
      
# Узел Источник
class NSource(GraphNode):

  def __init__(self, id, x, y, w, h):
    super().__init__(id, 'Источник', x, y, w, h)

  def pictureFileName(self):
    return 'images/Source.png'
  
  def makeSockets(self):
    self.inputSockets.clear()
    self.outputSockets.clear()

    self.outputSockets.append(GraphSocket('S',  'O', 0, 0, GraphNode.DEFAULT_SOCKET_WIDTH, GraphNode.DEFAULT_SOCKET_HEIGHT))
    
# Узел Сумматор
class NAdder(GraphNode):

  def __init__(self, id, x, y, w, h):
    super().__init__(id, 'Сумматор', x, y, w, h)

  def pictureFileName(self):
    return 'images/Adder.png'
    
  def makeSockets(self):
    self.inputSockets.clear()
    self.outputSockets.clear()

    self.inputSockets.append(GraphSocket('N1', 'I', 0, 0, GraphNode.DEFAULT_SOCKET_WIDTH, GraphNode.DEFAULT_SOCKET_HEIGHT))
    self.inputSockets.append(GraphSocket('N2', 'I', 0, 0, GraphNode.DEFAULT_SOCKET_WIDTH, GraphNode.DEFAULT_SOCKET_HEIGHT))
    self.inputSockets.append(GraphSocket('N3', 'I', 0, 0, GraphNode.DEFAULT_SOCKET_WIDTH, GraphNode.DEFAULT_SOCKET_HEIGHT))
    self.outputSockets.append(GraphSocket('S',  'O', 0, 0, GraphNode.DEFAULT_SOCKET_WIDTH, GraphNode.DEFAULT_SOCKET_HEIGHT))
    
# Узел Усилитель
class NAmplifier(GraphNode):

  def __init__(self, id, x, y, w, h):
    super().__init__(id, 'Усилитель', x, y, w, h)

  def pictureFileName(self):
    return 'images/Amplifier.png'
        
  def makeSockets(self):
    self.inputSockets.clear()
    self.outputSockets.clear()

    self.inputSockets.append(GraphSocket('S',  'I', 0, 0, GraphNode.DEFAULT_SOCKET_WIDTH, GraphNode.DEFAULT_SOCKET_HEIGHT))
    self.inputSockets.append(GraphSocket('K',  'I', 0, 0, GraphNode.DEFAULT_SOCKET_WIDTH, GraphNode.DEFAULT_SOCKET_HEIGHT))
    self.outputSockets.append(GraphSocket('A',  'O', 0, 0, GraphNode.DEFAULT_SOCKET_WIDTH, GraphNode.DEFAULT_SOCKET_HEIGHT))

# Узел Ветвление
class NCondition(GraphNode):
  def __init__(self, id, x, y, w, h):
    super().__init__(id, 'Ветвление', x, y, w, h)

  def pictureFileName(self):
    return 'images/Condition.png'
    
  def makeSockets(self):
    self.inputSockets.clear()
    self.outputSockets.clear()
    
    self.inputSockets.append(GraphSocket('S',  'I', 0, 0, GraphNode.DEFAULT_SOCKET_WIDTH, GraphNode.DEFAULT_SOCKET_HEIGHT))
    self.outputSockets.append(GraphSocket('T',  'O', 0, 0, GraphNode.DEFAULT_SOCKET_WIDTH, GraphNode.DEFAULT_SOCKET_HEIGHT))
    self.outputSockets.append(GraphSocket('F',  'O', 0, 0, GraphNode.DEFAULT_SOCKET_WIDTH, GraphNode.DEFAULT_SOCKET_HEIGHT))
    
# Связь    
class GraphLink(object):
  def __init__(self, id, nodeOutID, nodeInID, socketOutIndex, socketInIndex):
    self.id = id
    self.nodeOutID = nodeOutID
    self.nodeInID = nodeInID
    self.socketInIndex = socketInIndex
    self.socketOutIndex = socketOutIndex
    
# Схема (собственно, граф)  
class GraphScheme(object):
 
  def __init__(self):
    self.filePath = '' # путь к файлу схемы
    self.nodes = dict() # узлы
    self.links = dict() # связи
    self.nextID = 1     # id для следующего создаваемого объекта
    self.selectionType = '-' # тип выделения: '-' - ничего не выделено, 'N' - узлы, 'L' - связьб
    self.selection = set() # множество выделенных объектов
  
  # очистить схему
  def clear(self):
    self.nodes.clear()
    self.links.clear()    
  
  # создать узел с 0-ым id и вернуть его
  def createNode(self, typeName, x, y, w, h):
    nodeClass = getattr(sys.modules[__name__], typeName)
    node = nodeClass(0, x, y, w, h)
    return node
  
  # создать узел и добавить его в схему
  def addNode(self, typeName, x, y, w, h):
    
    node = self.createNode(typeName, x, y, w, h)
    
    newID = self.nextID
    
    self.nextID += 1
    
    node.id = newID
    
    self.nodes[newID] = node
  
    return newID
    
  # удалить узел 
  def removeNode(self, nodeID):
    
    if nodeID in self.nodes:
      node = self.nodes[nodeID]
 
      for socket in node.inputSockets:
        self.removeLink(socket.linkID)

      for socket in node.outputSockets:
        self.removeLink(socket.linkID)
        
      del self.nodes[nodeID]
  
  # удалить связь
  def removeLink(self, linkID):
    
    if linkID in self.links:
    
      link = self.links[linkID]
     
      nodeOut = self.nodes[link.nodeOutID]
      nodeIn =  self.nodes[link.nodeInID]
      nodeOut.detachLink('O', link.socketOutIndex)
      nodeIn.detachLink('I',  link.socketInIndex)
       
      del self.links[linkID]    
    
  
  # соединить связью два узла
  def linkNodes(self, nodeOutID, nodeInID, socketOutIndex, socketInIndex, linkID):
  
    if nodeOutID in self.nodes and nodeInID in self.nodes:
      
      
      if linkID == 0:
        oid = self.nextID
        self.nextID += 1
      else:
        oid = linkID
      
      self.links[oid] = GraphLink(oid, nodeOutID, nodeInID, socketOutIndex, socketInIndex)
    
      nodeOut = self.nodes[nodeOutID]
      nodeIn  = self.nodes[nodeInID]
    
      nodeOut.attachLink('O', socketOutIndex, oid)
      nodeIn.attachLink('I', socketInIndex, oid)
    
      return oid
      
    return 0

  # очистить выделение
  def clearSelection(self):
    self.selectionType = '-'
    self.selection.clear()


  # добавить связь в выделение
  def addLinkToSelection(self, linkID):
    self.selectionType = 'L'
    self.selection.clear()
    self.selection.add(linkID)

  # добавить узел в выделение
  def addNodeToSelection(self, nodeID):
  
    if self.selectionType != 'N':
      self.selectionType = 'N'
      self.selection.clear()
      
    self.selection.add(nodeID)

  # удалить узел из выделения
  def removeNodeFromSelection(self, nodeID):
      
    if self.selectionType == 'N' and nodeID in self.selection:
      self.selection.remove(nodeID)
  
    
  # выдать координаты линии связи
  def calcLinkLine(self, linkID):
    
    if linkID not in self.links:
      return None
      
    link = self.links[linkID]

    nodeOut = self.nodes[link.nodeOutID]  
    nodeIn = self.nodes[link.nodeInID]
    socketOut = nodeOut.outputSockets[link.socketOutIndex]
    socketIn  = nodeIn.inputSockets[link.socketInIndex]
    
    xo = nodeOut.left + socketOut.left + socketOut.width
    yo = nodeOut.top + socketOut.top + socketOut.height / 2.0
    
    xi = nodeIn.left + socketIn.left
    yi = nodeIn.top + socketIn.top + socketIn.height / 2.0
    
    return QLineF(xo, yo, xi, yi)
    
  # выдать окружающий линию связи полигон
  def linkBoundingPolygon(self, linkID):
    linkLine = self.calcLinkLine(linkID)
    
    if not (linkLine is None):
      nv = linkLine.normalVector()
      nv.setLength(5)
      
      pp = QLineF(nv.p2(), nv.p1())
      
      s1 = pp.normalVector()
      s1.setLength( linkLine.length() )
      
      nv = linkLine.normalVector()
      nv.setLength(-5)
      pp = QLineF(nv.p2(), nv.p1())
      
      s2 = pp.normalVector()
      s2.setLength(-linkLine.length())
  
      ret = QPolygonF()
      ret.append(s1.p1())
      ret.append(s1.p2())
      ret.append(s2.p2())
      ret.append(s2.p1())
      
      return ret
  
    return None
  
  # выдать точку присоединения связи к сокету
  def socketLinkPoint(self, nodeID, socketType, socketIndex):

    ret = QPointF()
    
    if nodeID in self.nodes:
      node = self.nodes[nodeID]
      
      if socketType == 'I':
      
        if socketIndex >= 0 and socketIndex < len(node.inputSockets):
          
          socket = node.inputSockets[socketIndex]
          ret    = QPointF(node.left, node.top + socket.top + socket.height / 2.0)
          
      elif socketType == 'O':

        if socketIndex >= 0 and socketIndex < len(node.outputSockets):
          
          socket = node.outputSockets[socketIndex]
          ret    = QPointF(node.left + node.width, node.top + socket.top + socket.height / 2.0)
  
    return ret
  
  # поиск объекта в точке
  def objectAtPoint( self, point ):
    
    objectType = '-'
    objectID = 0
    nodeID   = 0
    
    for node in self.nodes.values():
    
      r = QRectF(node.left, node.top, node.width, node.height)
      
      if r.contains( point ):

        objectType = 'N'
        objectID = node.id
        nodeID   = node.id
        
        i = 0
        
        for socket in node.inputSockets:
        
          sr = QRectF(node.left + socket.left, node.top + socket.top, socket.width, socket.height)
          
          if sr.contains( point ):
            objectType = 'SI'
            objectID   = i
            break
            
          i += 1

        if objectType != 'SI':
        
          i = 0
          
          for socket in node.outputSockets:
          
            sr = QRectF(node.left + socket.left, node.top + socket.top, socket.width, socket.height)
            
            if sr.contains( point ):
              objectType = 'SO'
              objectID   = i
              break
              
            i += 1

        break
    
    if objectType != 'N':
    
      for link in self.links.values():
        po = self.linkBoundingPolygon(link.id)

        if not (po is None):
          if po.containsPoint( point, Qt.WindingFill ):
            objectType = 'L'
            objectID = link.id
            break

        
    return (objectType, nodeID, objectID)
  
  # пермещение выделенных узлов 
  def moveSelectedNodes(self, dx, dy):
    
    if self.selectionType == 'N':
      for nodeID in self.selection:
        node = self.nodes[nodeID]
        node.left += dx
        node.top += dy
        
  
  # формирование тестовой схемы
  def makeTestScheme(self):
    
    nid1 = self.createNode('NSource', 'Старт', 10, 50, 150, 90)
    nid2 = self.createNode('NSource', 'Старт', 10, 200, 150, 90)
    nid3 = self.createNode('NAmplifier', 'Умножитель', 220, 120, 150, 90)
    nid4 = self.createNode('NCondition', 'Порог', 400, 120, 150, 90)
    
    self.linkNodes(nid1, nid3, 0, 0)
    self.linkNodes(nid2, nid3, 0, 1)
    self.linkNodes(nid3, nid4, 0, 0)
    
  # загрузить из файла 
  def load(self, filePath):

    maxID = 0
    oid = 0
    
    self.clear()
    
    content = dict()
    
    with open(filePath, "r", encoding="utf-8") as file:
      content = json.load(file)
       
    for n in content['nodes']:
      oid = int(n['id'])
      nodeClass = getattr(sys.modules[__name__], n['t'])
      self.nodes[ oid ] = nodeClass(oid, int(n['x']), int(n['y']), int(n['w']), int(n['h']) )
      
      if maxID < oid:
        maxID = oid
        
    for l in content['links']:
      oid = int(l['id'])

      self.linkNodes( int(l['no']), int(l['ni']), int(l['so']), int(l['si']), oid )
      
      if maxID < oid:
        maxID = oid
      
    self.nextID = maxID + 1
    self.filePath = filePath
    
  # сохранить в файл
  def save(self, filePath):
    content = {'nodes' : list(), 'links' : list() }
    
    for node in self.nodes.values():
      nc =  { 't' : node.__class__.__name__, 'id' : node.id, 'n' : node.name, 'x' : node.left, 'y':node.top, 'w' : node.width, 'h' : node.height }
      content['nodes'].append(nc)

    for link in self.links.values():
      lc =  { 'id' : link.id, 'no' : link.nodeOutID, 'ni' : link.nodeInID, 'so' : link.socketOutIndex, 'si' : link.socketInIndex }
      content['links'].append(lc)
      
    with open(filePath, "w", encoding="utf-8") as file:
      json.dump(content, file)

    self.filePath = filePath  