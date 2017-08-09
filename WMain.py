import sys
from PyQt5.QtWidgets import QWidget, QTableView, QHBoxLayout, QVBoxLayout, QPushButton, QFrame 
from WCanvas import WCanvas
from NodeTableModel import NodeTableModel
from FlowGraphCore import GraphScheme

# Главное окно
class WMain(QWidget):
  
  def __init__(self):
    super().__init__()

    self.scheme = GraphScheme()    
    self.scheme.makeTestScheme()
    
    self.initUI()

  def initUI(self):
    self.setWindowTitle('Редактор вычислительного графа')
    
    # панель команд
    self.frControl = QFrame()
    self.pbOpen = QPushButton('Открыть')
    self.pbSave = QPushButton('Сохранить')
        
    
    
    # набор узлов
    self.nodeModel = NodeTableModel()
        
    self.nodeView = QTableView()
    self.nodeView.setMaximumWidth(200)
    self.nodeView.setModel(self.nodeModel)
    
    
    self.canvas = WCanvas()
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