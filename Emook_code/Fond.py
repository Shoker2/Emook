# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/Иван/Desktop/Музейное дело/Fond.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Fond(object):
    def setupUi(self, Fond):
        Fond.setObjectName("Fond")
        Fond.resize(606, 569)
        Fond.setStyleSheet("")
        self.Title = QtWidgets.QLabel(Fond)
        self.Title.setGeometry(QtCore.QRect(6, 20, 591, 31))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.Title.setFont(font)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.listWidget = QtWidgets.QListWidget(Fond)
        self.listWidget.setGeometry(QtCore.QRect(15, 195, 571, 311))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listWidget.setFont(font)
        self.listWidget.setObjectName("listWidget")
        self.comboBoxSearch = QtWidgets.QComboBox(Fond)
        self.comboBoxSearch.setGeometry(QtCore.QRect(20, 100, 561, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBoxSearch.setFont(font)
        self.comboBoxSearch.setEditable(True)
        self.comboBoxSearch.setCurrentText("")
        self.comboBoxSearch.setObjectName("comboBoxSearch")
        self.labelSearch = QtWidgets.QLabel(Fond)
        self.labelSearch.setGeometry(QtCore.QRect(20, 71, 181, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelSearch.setFont(font)
        self.labelSearch.setObjectName("labelSearch")
        self.backButton = QtWidgets.QPushButton(Fond)
        self.backButton.setGeometry(QtCore.QRect(15, 520, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.backButton.setFont(font)
        self.backButton.setObjectName("backButton")
        self.labelSearch_2 = QtWidgets.QLabel(Fond)
        self.labelSearch_2.setGeometry(QtCore.QRect(20, 131, 311, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelSearch_2.setFont(font)
        self.labelSearch_2.setObjectName("labelSearch_2")
        self.comboBoxSearch_2 = QtWidgets.QComboBox(Fond)
        self.comboBoxSearch_2.setGeometry(QtCore.QRect(20, 160, 561, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBoxSearch_2.setFont(font)
        self.comboBoxSearch_2.setEditable(True)
        self.comboBoxSearch_2.setCurrentText("")
        self.comboBoxSearch_2.setObjectName("comboBoxSearch_2")
        self.refreshButton = QtWidgets.QPushButton(Fond)
        self.refreshButton.setGeometry(QtCore.QRect(460, 520, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.refreshButton.setFont(font)
        self.refreshButton.setObjectName("refreshButton")
        self.exporthButton = QtWidgets.QPushButton(Fond)
        self.exporthButton.setGeometry(QtCore.QRect(320, 520, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.exporthButton.setFont(font)
        self.exporthButton.setObjectName("exporthButton")
        self.importButton = QtWidgets.QPushButton(Fond)
        self.importButton.setGeometry(QtCore.QRect(180, 520, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.importButton.setFont(font)
        self.importButton.setObjectName("importButton")

        self.retranslateUi(Fond)
        QtCore.QMetaObject.connectSlotsByName(Fond)

    def retranslateUi(self, Fond):
        _translate = QtCore.QCoreApplication.translate
        Fond.setWindowTitle(_translate("Fond", "Form"))
        self.Title.setText(_translate("Fond", "Нумизматика: Медали"))
        self.labelSearch.setText(_translate("Fond", "Поиск на названию"))
        self.backButton.setText(_translate("Fond", "Назад"))
        self.labelSearch_2.setText(_translate("Fond", "Поиск по номеру учётной записи"))
        self.refreshButton.setText(_translate("Fond", "Обновить"))
        self.exporthButton.setText(_translate("Fond", "Экспортировать"))
        self.importButton.setText(_translate("Fond", "Импортировать"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Fond = QtWidgets.QWidget()
    ui = Ui_Fond()
    ui.setupUi(Fond)
    Fond.show()
    sys.exit(app.exec_())
