import sys
from PyQt5.QtWidgets import QWidget, QTableView, QAbstractItemView, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QFileDialog
from PyQt5.QtCore import Qt
from WCanvas import WCanvas
from NodeView import NodeView

from NodeTableModel import NodeTableModel
from FlowGraphCore import GraphScheme

# Главное окно
class WMain(QWidget):
  
  def __init__(self):
    super().__init__()

    self.scheme = GraphScheme()    
#    self.scheme.makeTestScheme()
#    self.scheme.save('D:/ZZ/000.json')
#    self.scheme.load('D:/ZZ/000.json')
    
    self.initUI()

  def initUI(self):
    self.setWindowTitle('Редактор вычислительного графа - Новая Схема')
    self.setAcceptDrops(False)
    
    # панель команд
    self.frControl = QFrame()
    self.pbOpen = QPushButton('Открыть')
    self.pbSave = QPushButton('Сохранить')
    
    # набор узлов
    self.nodeModel = NodeTableModel()
        
    self.nodeView = NodeView()
    self.nodeView.setMaximumWidth(200)
    self.nodeView.setModel(self.nodeModel)
    self.nodeView.setDragDropMode(QAbstractItemView.DragOnly)
    
    self.canvas = WCanvas()
    self.canvas.setFocusPolicy(Qt.StrongFocus)
    self.canvas.scheme = self.scheme
    

    # компоновка панели команд
    controlPanelBox = QHBoxLayout()
    controlPanelBox.addStretch(1)
    controlPanelBox.addWidget(self.pbOpen)
    controlPanelBox.addWidget(self.pbSave)
    self.frControl.setLayout(controlPanelBox)
    
    # компоновка низа
    centralBox = QHBoxLayout()
    centralBox.addWidget(self.nodeView)
    centralBox.addWidget(self.canvas)
    
    # компоновка верхнего уровня
    mainBox = QVBoxLayout()
    
    mainBox.addWidget(self.frControl)
    mainBox.addLayout(centralBox)
    
    self.setLayout(mainBox)
    
    # карта сигналов-слотов
    self.pbOpen.clicked.connect(self.onOpenScheme)
    self.pbSave.clicked.connect(self.onSaveScheme)
    
  def onOpenScheme(self):
    filePath = QFileDialog.getOpenFileName(self, 'Открыть схему', '.')

    if filePath[0]:
      self.scheme.load(filePath[0])
      self.canvas.repaint()
      self.canvas.setFocus()
      title = 'Редактор вычислительного графа: ' + filePath[0]
      self.setWindowTitle(title)
    
  def onSaveScheme(self):
    if self.scheme.filePath == '':
      
      filePath, _ = QFileDialog.getSaveFileName(self, 'Сохранить схему', '.')
    
      if filePath:
        self.scheme.save(filePath)
        title = 'Редактор вычислительного графа: ' + filePath
        self.setWindowTitle(title)
    else:
      self.scheme.save(self.scheme.filePath)
      
      