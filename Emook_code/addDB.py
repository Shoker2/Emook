# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Иван/Desktop/Код/Resourses/Доп прога/OriginUI/addDB.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addDB(object):
    def setupUi(self, addDB):
        addDB.setObjectName("addDB")
        addDB.resize(521, 300)
        self.addButton = QtWidgets.QPushButton(addDB)
        self.addButton.setGeometry(QtCore.QRect(410, 262, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.addButton.setFont(font)
        self.addButton.setObjectName("addButton")
        self.closeButton = QtWidgets.QPushButton(addDB)
        self.closeButton.setGeometry(QtCore.QRect(10, 260, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.closeButton.setFont(font)
        self.closeButton.setObjectName("closeButton")
        self.Title = QtWidgets.QLabel(addDB)
        self.Title.setGeometry(QtCore.QRect(16, 9, 491, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Title.setFont(font)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.lineName = QtWidgets.QLineEdit(addDB)
        self.lineName.setGeometry(QtCore.QRect(20, 110, 481, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lineName.setFont(font)
        self.lineName.setText("")
        self.lineName.setObjectName("lineName")
        self.labelName = QtWidgets.QLabel(addDB)
        self.labelName.setGeometry(QtCore.QRect(20, 80, 191, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelName.setFont(font)
        self.labelName.setObjectName("labelName")
        self.lineConnect = QtWidgets.QLineEdit(addDB)
        self.lineConnect.setGeometry(QtCore.QRect(20, 190, 481, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lineConnect.setFont(font)
        self.lineConnect.setText("")
        self.lineConnect.setObjectName("lineConnect")
        self.labelConnect = QtWidgets.QLabel(addDB)
        self.labelConnect.setGeometry(QtCore.QRect(20, 160, 241, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelConnect.setFont(font)
        self.labelConnect.setObjectName("labelConnect")

        self.retranslateUi(addDB)
        QtCore.QMetaObject.connectSlotsByName(addDB)

    def retranslateUi(self, addDB):
        _translate = QtCore.QCoreApplication.translate
        addDB.setWindowTitle(_translate("addDB", "Form"))
        self.addButton.setText(_translate("addDB", "Добавить"))
        self.closeButton.setText(_translate("addDB", "Отмена"))
        self.Title.setText(_translate("addDB", "Добавить базу данных"))
        self.labelName.setText(_translate("addDB", "Название"))
        self.labelConnect.setText(_translate("addDB", "Строка подключения"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    addDB = QtWidgets.QWidget()
    ui = Ui_addDB()
    ui.setupUi(addDB)
    addDB.show()
    sys.exit(app.exec_())
