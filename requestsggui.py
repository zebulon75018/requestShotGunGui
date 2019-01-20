"""
    >>> import qjsonmodel
    
"""

import json
import shotgun_api3 as sg 
from PyQt4 import QtGui, QtCore
import qjsonmodel



class Widget(QtGui.QWidget):
    
    def __init__(self, parent= None):
        super(Widget, self).__init__()

        self.settings = QtCore.QSettings( "requestSG.ini",QtCore.QSettings.IniFormat)  

        self.setLayout(QtGui.QVBoxLayout())

        formlayout = QtGui.QFormLayout()
        self.urlentry = QtGui.QLineEdit(self.settings.value("urlentry","").toString())
        self.namescript = QtGui.QLineEdit(self.settings.value("namescript").toString())
        self.keyscript = QtGui.QLineEdit(self.settings.value("keyscript").toString())
        self.type = QtGui.QLineEdit(self.settings.value("type").toString())
        self.filter = QtGui.QLineEdit(self.settings.value("filter").toString())
        self.fields = QtGui.QLineEdit(self.settings.value("fields").toString())
        formlayout.addRow("URL",self.urlentry)
        formlayout.addRow("namescript",self.namescript)
        formlayout.addRow("keyscript",self.keyscript)
        formlayout.addRow("AssetType",self.type)
        formlayout.addRow("filter",self.filter)
        formlayout.addRow("fields",self.fields)
        
        pushbutton = QtGui.QPushButton("Launch")

        pushbutton.clicked.connect(self.launchSGRequest)
        self.layout().addLayout(formlayout)
        self.layout().addWidget(pushbutton)
        view = QtGui.QTreeView()
        self.layout().addWidget(view)
        self.model = qjsonmodel.QJsonModel()

        view.setModel(self.model)

        view.resize(500, 300)

    def closeEvent(self, e):
        self.settings.setValue("urlentry",self.urlentry.text())
        self.settings.setValue("namescript",self.namescript.text())
        self.settings.setValue("keyscript",self.keyscript.text())
        self.settings.setValue("type",self.type.text())
        self.settings.setValue("filter",self.filter.text())
        self.settings.setValue("fields",self.fields.text())

    def launchSGRequest(self):
        try:
            sgc = sg.Shotgun(
                str(self.urlentry.text()),
                str(self.namescript.text()),
                str(self.keyscript.text())        
                )
            filter = json.loads(str(self.filter.text()))
            fields = json.loads(str(self.fields.text()))
            result = sgc.find(str(self.type.text()), filter, fields)
            self.model.load(result)
        except Exception as e:
                QtGui.QMessageBox.critical(self,"Error","%s" % e)
        
       
   

if __name__ == '__main__':
    import sys


    
    app = QtGui.QApplication(sys.argv)
    dialog = Widget()
    dialog.show()

    
    app.exec_()
