# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 22:57:17 2014

@author: satary
"""
from PyQt4 import QtGui,QtCore
import sys
class TableWidget(QtGui.QTableWidget):
    def __init__(self,parent=None):
        super(TableWidget, self).__init__(parent)
        self.parent=parent
        #self.table = QtGui.QTableWidget()
        self.clip = QtGui.QApplication.clipboard()
        #self.mainLayout = QtGui.QVBoxLayout(self)
        #self.mainLayout.addWidget(self.table)
        self.horizontalHeader().setMovable(True)
        self.verticalHeader().setMovable(True)
        self.horizontalHeader().setDefaultSectionSize(60)
        self.setMinimumWidth(237)
        self.setMinimumHeight(260)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
       

        self.rowOrder=['Cell number',
                    'Cell area',
                    'Mean intensity im1',
                    'Mean intensity im2',
                    'Abs foci number',
                    'Abs foci area',
                    'Abs foci soid',
                    'Rel foci number',
                    'Rel foci area',
                    'Rel foci soid',
                    'Foci intensity',
                    'Foci size']
        self.columnOrder=['Mean', 'MSE']


    def buildFromDict(self,inDict):
        rowOrder =self.rowOrder
        columnOrder =self.columnOrder
        for row in inDict:
            if not(row in rowOrder):
                rowOrder.append(row)
            for col in inDict[row]:
                if not(col in columnOrder):
                    columnOrder.append(col)

        rows=[]
        columns=[]
        for row in rowOrder:
            if row in inDict:
                rows.append(row)
                self.insertRow(self.rowCount())
                self.setVerticalHeaderItem(self.rowCount()-1, QtGui.QTableWidgetItem(row))
                for col in columnOrder:
                    if (col in inDict[row]):
                        if (not(col in columns)):
                            columns.append(col)
                            self.insertColumn(self.columnCount())
                            self.setHorizontalHeaderItem(self.columnCount()-1,QtGui.QTableWidgetItem(col))

        for row in rows:
            for col in columns:
                try:
                    item=QtGui.QTableWidgetItem(str(inDict[row][col]))
                    item.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
                    self.setItem(rows.index(row),columns.index(col),item)
                except:
                    pass                                      
        self.verticalHeader().setDefaultSectionSize(self.verticalHeader().minimumSectionSize())



        
        
    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.ControlModifier):        
            if e.key() == QtCore.Qt.Key_C:
                self.copySelectionToClipboard()
        
    def contextMenuEvent(self, pos):
        menu = QtGui.QMenu()
        copyAction = menu.addAction("Copy")
        action = menu.exec_(QtGui.QCursor.pos())
        if action == copyAction:
            self.copySelectionToClipboard()
        
    def copySelectionToClipboard(self):
        selected = self.selectedRanges()
        s = ""
        for r in xrange(selected[0].topRow(),selected[0].bottomRow()+1):
            for c in xrange(selected[0].leftColumn(),selected[0].rightColumn()+1):
                try:
                    s += str(self.item(r,c).text()) + "\t"
                except AttributeError:
                    s += "\t"
            s = s[:-1] + "\n" #eliminate last '\t'
            self.clip.setText(s)
            
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = TableWidget()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    