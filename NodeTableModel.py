import sys
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtGui  import QIcon

class NodeTypeInfo(object):
  def __init__(self, className, title, iconName):
    self.className = className
    self.title = title
    self.icon = QIcon(iconName)

class NodeTableModel(QAbstractTableModel):

  def __init__(self, parent = None):
  
    super(NodeTableModel, self).__init__(parent)
    
    self.nodes = list()
    
    self.nodes.append( NodeTypeInfo('NSource',     'Источник',  'images/Source.png')  )
    self.nodes.append( NodeTypeInfo('NAdder',     'Сумматор',  'images/Adder.png')  )
    self.nodes.append( NodeTypeInfo('NAmplifier', 'Усилитель', 'images/Amplifier.png')  )
    self.nodes.append( NodeTypeInfo('NCondition', 'Условие',   'images/Condition.png')  )
    
  def rowCount(self, parent = QModelIndex()):
    return len(self.nodes)
    
  def columnCount(self, parent = QModelIndex()):
    return 1
    
    
  def data(self, index, role):
    
    if not index.isValid():
      return None
      
    if index.row() >= len(self.nodes):
      return None
    
    if role == Qt.DisplayRole:
      return self.nodes[index.row()].title
      
    if role == Qt.DecorationRole:
      return self.nodes[index.row()].icon
    
    return None

    
  def headerData(self, section, orientation, role = Qt.DisplayRole):
 
    if orientation == Qt.Horizontal and role == Qt.DisplayRole:
      return 'Блоки'
  
    return None

