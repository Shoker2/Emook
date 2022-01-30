import threading # Стандартные
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets # Сторонние
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon
from pymongo import MongoClient
import configparser
import openpyxl
import pandas as pd

from Museum_main import Ui_Main # Локальные
from Fond import Ui_Fond
from addForm import Ui_addForm
from addFormPartTwo import Ui_addFormTwo
from Subselection import Ui_Subselection
from readFond import Ui_readForm
from Settings import Ui_Settings
from singin import Ui_SingIn
from addDB import Ui_addDB

def themeSelect(i=1):
	global config
	global geometry
	global ButtonFontPointSize
	global style
	global logo

	config = configparser.ConfigParser() # Открытие config файла
	config.read('Resourses\\config.ini', encoding ="utf8")

	try:
		geometry = configparser.ConfigParser() # Открытие файла с геометрией объектов
		geometry.read('Resourses\\Geometry\\' + config['Settings']['geometry'] + '.ini', encoding ="utf8")

		ButtonFontPointSize = QtGui.QFont() # Получение размера шрифта для всех кнопок
		ButtonFontPointSize.setPointSize(int(geometry['Additions']['ButtonFontPointSize']))
	except:
		ButtonFontPointSize.setPointSize(11)
		geometry = None
		config['Settings']['geometry'] = 'Стандарт'

		with open('Resourses\\config.ini', 'w+', encoding ="utf8") as configfile:
			config.write(configfile)
		if i != 2:
			themeSelect(2)

	try: # Добавляю css
		f = open('Resourses\\styles\\' + config['Settings']['theme'] + '.css', 'r', encoding ="utf8")
		style = f.read()
		f.close()
	except:
		style = ''

	logo = 'Resourses\\logo.png'

themeSelect()

def cgs(select, subselect, num): # Передача геометрии объектов сразу в переменные
	geoList = list(map(int, geometry[select][subselect].split(', ')))
	if num == 2:
		return (geoList[0], geoList[1])
	else:
		return (geoList[0], geoList[1], geoList[2], geoList[3])

def messageBox(title, text, icon=None): # Окно ошибки
	msgBox = QMessageBox()
	if icon != None:
		msgBox.setIcon(icon)
	msgBox.setWindowTitle(title)
	msgBox.setText(text)
	try:
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
		msgBox.setWindowIcon(icon)
	except:
		pass
	msgBox.setStandardButtons(QMessageBox.Ok)
	msgBox.exec()

def restart():
	QtCore.QCoreApplication.quit()
	status = QtCore.QProcess.startDetached(sys.executable, sys.argv)

class main(Ui_Main):
	def setupUi(self, main):
		Ui_Main.setupUi(self, main)
		main.setStyleSheet(style)

		try: # Добавляю иконку
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
			main.setWindowIcon(icon)
		except:
			pass

		if geometry != None:
			w, h = cgs('Main', 'Window', 2)		# Установка геометрии для окна
			main.resize(w, h)
			main.setMaximumSize(w, h)

			x, y, w, h = cgs('Main', 'Title', 4)	# Установка геометрии для разных объектов (кнопки и т.д.)
			self.Title.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Main', 'labelSelection', 4)
			self.labelSelection.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Main', 'allButton', 4)
			self.allButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Main', 'addButton', 4)
			self.addButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Main', 'exitButton', 4)
			self.exitButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Main', 'pushButton_1', 4)
			self.pushButton_1.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Main', 'pushButton_2', 4)
			self.pushButton_2.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Main', 'pushButton_3', 4)
			self.pushButton_3.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Main', 'pushButton_4', 4)
			self.pushButton_4.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Main', 'pushButton_5', 4)
			self.pushButton_5.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Main', 'pushButton_6', 4)
			self.pushButton_6.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Main', 'pushButton_7', 4)
			self.pushButton_7.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Main', 'pushButton_8', 4)
			self.pushButton_8.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Main', 'settingsButton', 4)
			self.settingsButton.setGeometry(QtCore.QRect(x, y, w, h))

			self.allButton.setFont(ButtonFontPointSize) # Устанавливаю размер шрифта на объекты
			self.addButton.setFont(ButtonFontPointSize)
			self.exitButton.setFont(ButtonFontPointSize)
			self.settingsButton.setFont(ButtonFontPointSize)
			self.pushButton_1.setFont(ButtonFontPointSize)
			self.pushButton_2.setFont(ButtonFontPointSize)
			self.pushButton_3.setFont(ButtonFontPointSize)
			self.pushButton_4.setFont(ButtonFontPointSize)
			self.pushButton_5.setFont(ButtonFontPointSize)
			self.pushButton_6.setFont(ButtonFontPointSize)
			self.pushButton_7.setFont(ButtonFontPointSize)
			self.pushButton_8.setFont(ButtonFontPointSize)

			font = QtGui.QFont()
			font.setPointSize(int(geometry['Main']['FontTitle']))
			self.Title.setFont(font)
			font.setPointSize(int(geometry['Main']['FontlabelSelection']))
			self.labelSelection.setFont(font)
		
		self.addButton.clicked.connect(lambda: self.addFormOpen()) #Добаляю функции к кнопкам
		self.pushButton_1.clicked.connect(lambda: self.selectionClicked(self.pushButton_1.text()))
		self.pushButton_2.clicked.connect(lambda: self.selectionClicked(self.pushButton_2.text()))
		self.pushButton_3.clicked.connect(lambda: self.selectionClicked(self.pushButton_3.text()))
		self.pushButton_4.clicked.connect(lambda: self.selectionClicked(self.pushButton_4.text()))
		self.pushButton_5.clicked.connect(lambda: self.selectionClicked(self.pushButton_5.text()))
		self.pushButton_6.clicked.connect(lambda: self.selectionClicked(self.pushButton_6.text()))
		self.pushButton_7.clicked.connect(lambda: self.selectionClicked(self.pushButton_7.text()))
		self.pushButton_8.clicked.connect(lambda: self.selectionClicked(self.pushButton_8.text()))
		self.allButton.clicked.connect(lambda: self.selectionClicked(self.allButton.text()))
		self.settingsButton.clicked.connect(lambda: self.settingsOpen())
		self.exitButton.clicked.connect(lambda: self.back())

	def retranslateUi(self, main):
		_translate = QtCore.QCoreApplication.translate
		Ui_Main.retranslateUi(self, main)
		Main.setWindowTitle("Учёт музейных фондов")
		self.exitButton.setText("Назад")

		self.Title.setText('Учёт музейных фондов')

	def setTitle(self, main, name):
		Main.setWindowTitle("Учёт музейных фондов - " + name)

	def back(self):
		Main.close()
		winEditDB.close()
		winAddDB.close()
		wineditFormTwo.close()
		wineditForm.close()
		winaddFormTwo.close()
		winForm.close()
		try:
			winSubselection.close()
		except:
			pass
		try:
			readForm.close()
		except:
			pass

		winSingIn.show()

	def selectionClicked(self, selection):
		'''
		Открытие нужного окна
		(если это раздел имеет подраздел, то открывается окно выбора подраздела)
		'''
		global selectionMain
		global subselectionMain
		global winFond
		global winSubselection

		selectionMain = selection
		subselectionMain = ''

		Main.hide()

		if selection == 'Изобразительные памятники' or selection == 'Нумизматика' or selection == 'Предметы этнографии' or selection == 'Предметы печатной продукции':
			winSubselection = QtWidgets.QWidget()
			uiSubselection = UiSubselection()
			uiSubselection.setupUi(winSubselection)
			winSubselection.show()

		elif selection == 'Археология' or selection == 'Оружие' or selection == 'Документы, фотографии' or selection == 'Предметы исторической техники' or selection == 'Все':
			winFond = QtWidgets.QWidget()
			uiFond = Fond()
			uiFond.setupUi(winFond)

	def addFormOpen(self):
		Main.hide()

		addForm.setupUi(salf, salfmain)
		addFormPartTwo.setupUi(salk, salkmain)
		winForm.show()

	def settingsOpen(self):
		global Settings
		Settings = QtWidgets.QWidget()
		winSettings = UiSettings()
		winSettings.setupUi(Settings)
		Settings.show()

class Fond(Ui_Fond):
	def setupUi(self, main):
		Ui_Fond.setupUi(self, main)
		main.setStyleSheet(style)

		try: # Установка иконки
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
			main.setWindowIcon(icon)
		except:
			pass

		if geometry != None:
			w, h = cgs('Fond', 'Window', 2) # Установка геометрии объектам
			main.resize(w, h)
			main.setMaximumSize(w, h)

			x, y, w, h = cgs('Fond', 'Title', 4)
			self.Title.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Fond', 'listWidget', 4)
			self.listWidget.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Fond', 'comboBoxSearch', 4)
			self.comboBoxSearch.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Fond', 'labelSearch', 4)
			self.labelSearch.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Fond', 'backButton', 4)
			self.backButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Fond', 'labelSearch_2', 4)
			self.labelSearch_2.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Fond', 'comboBoxSearch_2', 4)
			self.comboBoxSearch_2.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Fond', 'refreshButton', 4)
			self.refreshButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Fond', 'exporthButton', 4)
			self.exporthButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('Fond', 'importButton', 4)
			self.importButton.setGeometry(QtCore.QRect(x, y, w, h))

			font = QtGui.QFont()	# Установка размера шрифта
			font.setPointSize(int(geometry['Fond']['FontTitle']))
			self.Title.setFont(font)
			font.setPointSize(int(geometry['Fond']['FontlabelSearch']))
			self.labelSearch.setFont(font)
			font.setPointSize(int(geometry['Fond']['FontlabelSearch_2']))
			self.labelSearch_2.setFont(font)
			font.setPointSize(int(geometry['Fond']['FontlistWidget']))
			self.listWidget.setFont(font)

			self.backButton.setFont(ButtonFontPointSize)
			self.refreshButton.setFont(ButtonFontPointSize)
			self.exporthButton.setFont(ButtonFontPointSize)
			self.importButton.setFont(ButtonFontPointSize)

		# Добавление функций к объектам
		self.comboBoxSearch.activated.connect(lambda: self.openInBox(self.comboBoxSearch.currentText()))
		self.comboBoxSearch_2.activated.connect(lambda: self.openInBoxId(self.comboBoxSearch_2.currentText()))
		self.listWidget.itemDoubleClicked.connect(self.openInList)
		self.backButton.clicked.connect(lambda: self.mainOpen())
		self.refreshButton.clicked.connect(lambda: self.refresh())
		self.exporthButton.clicked.connect(lambda: self.save())
		self.importButton.clicked.connect(lambda: self.selectExel())

		if subselectionMain != '':
			self.Title.setText(selectionMain + ': ' + subselectionMain)
		elif selectionMain == 'Все':
			self.Title.setText('Все фонды')
		else:
			self.Title.setText(selectionMain)

		global collection
		global select
		global subselect
		select = selectionMain
		subselect = subselectionMain

		db = cluster['Все']
		collection = db['none']

		self.refresh(2)

		global fondSelf
		fondSelf = self

	def retranslateUi(self, main):
		Ui_Fond.retranslateUi(self, main)
		main.setWindowTitle("Список экспонатов")

	def refresh(self, test='1'): # Обновление списка экспонатов
		s = []
		if select == 'Все':
			nameid = collection.find()
		else:
			nameid = collection.find({'select': select, 'subselect': subselect})

		if test != '1':
			winFond.show()

		global listItems
		listItems = []
		listid = []
		try:
			for b in nameid:
				s.append(b)
				listItems.append(str(b['Name']))
				listid.append(str(b['number']))

			self.listWidget.clear()
			self.comboBoxSearch.clear()
			self.comboBoxSearch_2.clear()
			for i in range(len(listItems)):
				if listid[i] != '':
					self.listWidget.addItem(listItems[i] + ' №' + listid[i])
					self.comboBoxSearch.addItem(listItems[i])
					self.comboBoxSearch_2.addItem(listid[i])
				else:
					self.listWidget.addItem(listItems[i])
					self.comboBoxSearch.addItem(listItems[i])

			self.comboBoxSearch.setCurrentText("")
			self.comboBoxSearch_2.setCurrentText("")
		except:
			winFond.close()
			messageBox('Ошибка подключения', 'Не удалось открыть базу данных.')
			Main.show()

	def mainOpen(self):
		winFond.hide()
		Main.show()

	def openInBox(self, name): # Открытие по номеру учётной записи
		self.comboBoxSearch.setCurrentText("")
		self.open(name)
		
	def openInBoxId(self, id): # Открытие через поиск по названию
		self.comboBoxSearch_2.setCurrentText("")
		nameid = collection.find()
		for b in nameid:
			if b['number'] == id:
				name = b['Name']
		self.open(name)

	def openInList(self): # Открытие со списка
		id = int(self.listWidget.currentRow())
		name = listItems[id]
		self.open(name)

	def open(self, name): # Открытие окнв с информацией о экспонате
		wineditFormTwo.hide()
		wineditForm.hide()
		global forread
		forread = []

		nameid = collection.find({'Name': name})
		for b in nameid:
			fonds = b['fonds']
			select = b['select']
			subselect = b['subselect']
			number = b['number']
			gifter = b['gifter']
			point = b['point']
			description = b['description']

			forread = [fonds, name, number, gifter, point, description, select, subselect]
		
		if len(forread) != 0:
			global readForm
			readForm = QtWidgets.QWidget()
			uiRead = UiReadForm()
			uiRead.setupUi(readForm)
			readForm.show()

	def getList(self, way): # Получает таблицу exel с базы данных
		exlName = []
		exlFond = []
		exlSelect = []
		exlSubselect = []
		exlNumber = []
		exlGifter = []
		exlPoint = []
		exlDesc = []

		if select == 'Все':
			nameid = collection.find()
		else:
			nameid = collection.find({'select': select, 'subselect': subselect})
		for b in nameid:
			exlName.append(b['Name'])
			exlFond.append(b['fonds'])
			exlSelect.append(b['select'])
			exlSubselect.append(b['subselect'])
			exlNumber.append(b['number'])
			exlGifter.append(b['gifter'])
			exlPoint.append(b['point'])
			exlDesc.append(b['description'])

		df = pd.DataFrame({
			'Название': exlName,
			'Номер': exlNumber,
			'Фонд': exlFond,
			'Раздел': exlSelect,
			'Подраздел': exlSubselect,
			'Даритель': exlGifter,
			'Место хранения': exlPoint,
			'Описание': exlDesc
			})
		df.to_excel(way, sheet_name='Данные экспонатов', index=False)

	def setList(self, way): # Загружает экспонату с таблицы exel в базу данных
		exl = openpyxl.open(r''+ way, read_only=True)
		sheet = exl.active

		post = []
		for row in range(2, int(sheet.max_row)+1):
			Name = str(sheet[row][0].value)
			number = str(sheet[row][1].value)
			if number == 'None':
				number = ''
			fonds = str(sheet[row][2].value)
			selection = str(sheet[row][3].value)

			subselection = str(sheet[row][4].value)
			if subselection == 'None':
				subselection = ''

			gifter = str(sheet[row][5].value)
			if gifter == 'None':
				gifter = ''
			point = str(sheet[row][6].value)
			if str(point) == 'None':
				point = ''
			description = str(sheet[row][7].value)
			if str(description) == 'None':
				description = ''

			post = {'fonds': fonds, 'select': selection, 'subselect': subselection , 'Name': Name, 'number': number, 'gifter': gifter, 'point': point, 'description': description}

			db = cluster['Все']
			collection = db['none']
			collection.delete_one({'Name': Name})
			collection.insert_one(post)

		exl._archive.close()
		messageBox('Готово', 'Таблица загружена в базу данных')
		self.refresh()

	def selectExel(self): # Выбор файла таблицы exel
		way, _ = QFileDialog.getOpenFileName(None, 'Выбрать файл', './', "Exel таблица (*.xlsx)")
		if way != '':
			thread = threading.Thread(target=self.setList(way))
			thread.start()

	def save(self): # Выбор места сохранения таблицы exel
		way, _ = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File',"Данные экспонатов.xlsx", 'Exel таблица (*.xlsx)')
		if way != '':
			thread = threading.Thread(target=self.getList(way))
			thread.start()

class addForm(Ui_addForm):
	def setupUi(self, main):
		Ui_addForm.setupUi(self, main)
		main.setStyleSheet(style)

		try: # Установка иконки
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
			main.setWindowIcon(icon)
		except:
			pass

		if geometry != None:
			w, h = cgs('addForm', 'Window', 2) # Установка геометрии объектам
			main.resize(w, h)
			main.setMaximumSize(w, h)

			x, y, w, h = cgs('addForm', 'Title', 4)
			self.Title.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'labelSelection', 4)
			self.labelSelection.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'Section', 4)
			self.Section.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'labelSubselection', 4)
			self.labelSubselection.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'Subselection', 4)
			self.Subselection.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'radioButtonFond_1', 4)
			self.radioButtonFond_1.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'radioButtonFond_2', 4)
			self.radioButtonFond_2.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'nextButton', 4)
			self.nextButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'backButton', 4)
			self.backButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'lineEditName', 4)
			self.lineEditName.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'labelName', 4)
			self.labelName.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'labelNumber', 4)
			self.labelNumber.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'lineEditNumber', 4)
			self.lineEditNumber.setGeometry(QtCore.QRect(x, y, w, h))

			font = QtGui.QFont() # Установка размера шрифта
			font.setPointSize(int(geometry['addForm']['FontTitle']))
			self.Title.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontlabelSelection']))
			self.labelSelection.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontSection']))
			self.Section.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontlabelSubselection']))
			self.labelSubselection.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontSubselection']))
			self.Subselection.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontradioButtonFond_1']))
			self.radioButtonFond_1.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontradioButtonFond_2']))
			self.radioButtonFond_2.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontlineEditName']))
			self.lineEditName.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontlabelName']))
			self.labelName.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontlabelNumber']))
			self.labelNumber.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontlineEditNumber']))
			self.lineEditNumber.setFont(font)

			self.nextButton.setFont(ButtonFontPointSize)
			self.backButton.setFont(ButtonFontPointSize)

		# Добавление функций к объектам
		self.Section.activated.connect(lambda: self.selectionClicked(self.Section.currentText()))
		self.backButton.clicked.connect(lambda: self.mainOpen())
		self.nextButton.clicked.connect(lambda: self.next())

		self.Section.addItem("Изобразительные памятники")
		self.Section.addItem("Нумизматика")
		self.Section.addItem("Археология")
		self.Section.addItem("Предметы этнографии")
		self.Section.addItem("Оружие")
		self.Section.addItem("Документы, фотографии")
		self.Section.addItem("Предметы исторической техники")
		self.Section.addItem("Предметы печатной продукции")

		self.selectionClicked(self.Section.currentText())

		global salf
		global salfmain
		salf = self
		salfmain = main

	def retranslateUi(self, main):
		Ui_addForm.retranslateUi(self, main)
		main.setWindowTitle("Добавление экспоната")

	def selectionClicked(self, selection): # Установка подразделов в выпадающий список, в зависимости от выбранного раздела
		self.Subselection.clear()

		if selection == 'Изобразительные памятники':
			self.labelSubselection.setEnabled(True)
			self.Subselection.setEnabled(True)

			self.Subselection.addItem("Живопись")
			self.Subselection.addItem("Графика")
			self.Subselection.addItem("Скульптуры")
			self.Subselection.addItem('Другое')

		elif selection == 'Нумизматика':
			self.labelSubselection.setEnabled(True)
			self.Subselection.setEnabled(True)

			self.Subselection.addItem("Монеты")
			self.Subselection.addItem("Медали")
			self.Subselection.addItem("Значки")

		elif selection == 'Предметы этнографии':
			self.labelSubselection.setEnabled(True)
			self.Subselection.setEnabled(True)

			self.Subselection.addItem('Предметы быта')
			self.Subselection.addItem('Орудия труда')

		elif selection == 'Предметы печатной продукции':
			self.labelSubselection.setEnabled(True)
			self.Subselection.setEnabled(True)

			self.Subselection.addItem('Книги')
			self.Subselection.addItem('Брошуры, открытки')
			self.Subselection.addItem('Плакаты')
			self.Subselection.addItem('Другое')

		else:
			self.labelSubselection.setEnabled(False)
			self.Subselection.setEnabled(False)

		self.nextButton.setEnabled(True)

	def next(self): # Переход на следующюю страницу и сохранение текущих характеристик
		global selectionAdd
		global subselectionAdd
		global fondsAdd
		global nameAdd
		global numberAdd

		selectionAdd = self.Section.currentText()
		subselectionAdd = self.Subselection.currentText()

		if self.radioButtonFond_1.isChecked() == True:
			fondsAdd = 'Основной фонд'
		elif self.radioButtonFond_2.isChecked() == True:
			fondsAdd = 'Научно-вспомогательный фонд'

		nameAdd = self.lineEditName.text()
		numberAdd = self.lineEditNumber.text()

		winForm.hide()
		winaddFormTwo.show()

	def mainOpen(self):
		winForm.hide()
		Main.show()

class addFormPartTwo(Ui_addFormTwo):
	def setupUi(self, main):
		Ui_addFormTwo.setupUi(self, main)
		main.setStyleSheet(style)

		try: # Установка иконки
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
			main.setWindowIcon(icon)
		except:
			pass

		if geometry != None:
			w, h = cgs('addFormPartTwo', 'Window', 2) # Установка геометрии объектов
			main.resize(w, h)
			main.setMaximumSize(w, h)

			x, y, w, h = cgs('addFormPartTwo', 'Title', 4)
			self.Title.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'labelGifter', 4)
			self.labelGifter.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'lineEditGifter', 4)
			self.lineEditGifter.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'labelDescription', 4)
			self.labelDescription.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'textEditDescription', 4)
			self.textEditDescription.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'labelPoint', 4)
			self.labelPoint.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'lineEditPoint', 4)
			self.lineEditPoint.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'saveButton', 4)
			self.saveButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'backButton', 4)
			self.backButton.setGeometry(QtCore.QRect(x, y, w, h))

			font = QtGui.QFont() # Установка размера шрифта
			font.setPointSize(int(geometry['addFormPartTwo']['FontTitle']))
			self.Title.setFont(font)
			font.setPointSize(int(geometry['addFormPartTwo']['FontlabelGifter']))
			self.labelGifter.setFont(font)
			font.setPointSize(int(geometry['addFormPartTwo']['FontlineEditGifter']))
			self.lineEditGifter.setFont(font)
			font.setPointSize(int(geometry['addFormPartTwo']['FontlabelDescription']))
			self.labelDescription.setFont(font)
			font.setPointSize(int(geometry['addFormPartTwo']['FonttextEditDescription']))
			self.textEditDescription.setFont(font)
			font.setPointSize(int(geometry['addFormPartTwo']['FontlabelPoint']))
			self.labelPoint.setFont(font)
			font.setPointSize(int(geometry['addFormPartTwo']['FontlineEditPoint']))
			self.lineEditPoint.setFont(font)

			self.backButton.setFont(ButtonFontPointSize)
			self.saveButton.setFont(ButtonFontPointSize)

		# Добавление функций к кнопкам
		self.backButton.clicked.connect(lambda: self.back())
		self.saveButton.clicked.connect(lambda: self.save())

		global salk
		global salkmain
		salk = self
		salkmain = main

	def retranslateUi(self, main):
		Ui_addFormTwo.retranslateUi(self, main)
		main.setWindowTitle("Добавление экспоната")

	def save(self): # Сохранение экспаната в базу данных
		selection = selectionAdd
		subselection = subselectionAdd
		fonds = fondsAdd
		Name = nameAdd
		number = numberAdd

		db = cluster['Все']
		collection = db['none']

		if Name != '':
			if collection.count_documents({'Name': Name}) == 0:
				gifter = self.lineEditGifter.text()
				point = self.lineEditPoint.text()
				description = self.textEditDescription.toPlainText()

				post = {'fonds': fonds, 'select': selection, 'subselect': subselection , 'Name': Name, 'number': number, 'gifter': gifter, 'point': point, 'description': description}

				db = cluster['Все']
				collection = db['none']
				collection.insert_one(post)

				self.mainOpen()
			else:
				messageBox('Ошибка названия', 'Введено уже существующее название экспоната', QMessageBox.Critical)
		else:
			messageBox('Ошибка названия', 'Не введено название экспонат', QMessageBox.Critical)

	def back(self):
		winaddFormTwo.hide()
		winForm.show()

	def mainOpen(self):
		winaddFormTwo.hide()
		Main.show()

class UiSubselection(Ui_Subselection):
	def setupUi(self, main):
		Ui_Subselection.setupUi(self, main)
		main.setStyleSheet(style)

		try: # Установка иконки
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
			main.setWindowIcon(icon)
		except:
			pass

		if geometry != None:
			w, h = cgs('UiSubselection', 'Window', 2) # Установка геометрии объектам
			main.resize(w, h)
			main.setMaximumSize(w, h)

			x, y, w, h = cgs('UiSubselection', 'Title', 4)
			self.Title.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiSubselection', 'labelSubselection', 4)
			self.labelSubselection.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiSubselection', 'backButton', 4)
			self.backButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiSubselection', 'pushButton_1', 4)
			self.pushButton_1.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiSubselection', 'pushButton_2', 4)
			self.pushButton_2.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiSubselection', 'pushButton_3', 4)
			self.pushButton_3.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiSubselection', 'pushButton_4', 4)
			self.pushButton_4.setGeometry(QtCore.QRect(x, y, w, h))

			font = QtGui.QFont() # Установка размера шрифта
			font.setPointSize(int(geometry['UiSubselection']['FontTitle']))
			self.Title.setFont(font)
			font.setPointSize(int(geometry['UiSubselection']['FontlabelSubselection']))
			self.labelSubselection.setFont(font)

			self.backButton.setFont(ButtonFontPointSize)
			self.pushButton_1.setFont(ButtonFontPointSize)
			self.pushButton_2.setFont(ButtonFontPointSize)
			self.pushButton_3.setFont(ButtonFontPointSize)
			self.pushButton_4.setFont(ButtonFontPointSize)

		# Добовление функций к кнопкам
		self.pushButton_1.clicked.connect(lambda: self.selectionClicked(self.pushButton_1.text()))
		self.pushButton_2.clicked.connect(lambda: self.selectionClicked(self.pushButton_2.text()))
		self.pushButton_3.clicked.connect(lambda: self.selectionClicked(self.pushButton_3.text()))
		self.pushButton_4.clicked.connect(lambda: self.selectionClicked(self.pushButton_4.text()))
		self.backButton.clicked.connect(lambda: self.mainOpen())

		Empty = '...' # Текст пустой кнопки
		self.Title.setText(selectionMain)
		if selectionMain == 'Изобразительные памятники': # Установка названий подразделов на кнопки
			self.pushButton_1.setText("Живопись")
			self.pushButton_2.setText("Графика")
			self.pushButton_3.setText("Скульптуры")
			self.pushButton_4.setText('Другое')

		elif selectionMain == 'Нумизматика':
			self.pushButton_1.setText("Медали")
			self.pushButton_2.setText("Монеты")
			self.pushButton_3.setText("Значки")
			self.pushButton_4.setText(Empty)
			self.pushButton_4.setEnabled(False)

		elif selectionMain == 'Предметы этнографии':
			self.pushButton_1.setText("Предметы быта")
			self.pushButton_2.setText("Орудия труда")
			self.pushButton_3.setText(Empty)
			self.pushButton_4.setText(Empty)
			self.pushButton_3.setEnabled(False)
			self.pushButton_4.setEnabled(False)

		elif selectionMain == 'Предметы печатной продукции':
			self.pushButton_1.setText('Книги')
			self.pushButton_2.setText("Брошуры, открытки")
			self.pushButton_3.setText("Плакаты")
			self.pushButton_4.setText("Другое")

	def retranslateUi(self, main):
		_translate = QtCore.QCoreApplication.translate
		Ui_Subselection.retranslateUi(self, main)
		main.setWindowTitle("Учёт музейных фондов")

	def selectionClicked(self, selection): # Переход к списку экспонатов
		global subselectionMain
		subselectionMain = selection

		winSubselection.hide()

		global winFond
		winFond = QtWidgets.QWidget()
		uiFond = Fond()
		uiFond.setupUi(winFond)


	def mainOpen(self):
		winSubselection.hide()
		Main.show()

class UiReadForm(Ui_readForm):
	def setupUi(self, main):
		Ui_readForm.setupUi(self, main)
		main.setStyleSheet(style)

		try: # Установка иконки
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
			main.setWindowIcon(icon)
		except:
			pass

		if geometry != None:
			w, h = cgs('UiReadForm', 'Window', 2) # Установка геометрии объекстов
			main.resize(w, h)
			main.setMaximumSize(w, h)

			x, y, w, h = cgs('UiReadForm', 'Title', 4)
			self.Title.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'titleSelection', 4)
			self.titleSelection.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'titleSubselection', 4)
			self.titleSubselection.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'labelNumber', 4)
			self.labelNumber.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'labelGifter', 4)
			self.labelGifter.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'labelDescription', 4)
			self.labelDescription.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'labelPoint', 4)
			self.labelPoint.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'labelSelection', 4)
			self.labelSelection.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'labelSubselection', 4)
			self.labelSubselection.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'labelTypeFond', 4)
			self.labelTypeFond.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'lableNumber', 4)
			self.lableNumber.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'lableGifter', 4)
			self.lableGifter.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'lablePoint', 4)
			self.lablePoint.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'textBrowserDescription', 4)
			self.textBrowserDescription.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'pushButtonDelite', 4)
			self.pushButtonDelite.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'pushButtonClose', 4)
			self.pushButtonClose.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiReadForm', 'pushButtonEdit', 4)
			self.pushButtonEdit.setGeometry(QtCore.QRect(x, y, w, h))

			font = QtGui.QFont() # Установка размера шрифта
			font.setPointSize(int(geometry['UiReadForm']['FontTitle']))
			self.Title.setFont(font)
			font.setPointSize(int(geometry['UiReadForm']['FonttitleSelection']))
			self.titleSelection.setFont(font)
			font.setPointSize(int(geometry['UiReadForm']['FonttitleSubselection']))
			self.titleSubselection.setFont(font)
			font.setPointSize(int(geometry['UiReadForm']['FontlabelNumber']))
			self.labelNumber.setFont(font)
			font.setPointSize(int(geometry['UiReadForm']['FontlabelGifter']))
			self.labelGifter.setFont(font)
			font.setPointSize(int(geometry['UiReadForm']['FontlabelDescription']))
			self.labelDescription.setFont(font)
			font.setPointSize(int(geometry['UiReadForm']['FontlabelPoint']))
			self.labelPoint.setFont(font)
			font.setPointSize(int(geometry['UiReadForm']['FontlabelSelection']))
			self.labelSelection.setFont(font)
			font.setPointSize(int(geometry['UiReadForm']['FontlabelSubselection']))
			self.labelSubselection.setFont(font)
			font.setPointSize(int(geometry['UiReadForm']['FontlabelTypeFond']))
			self.labelTypeFond.setFont(font)
			font.setPointSize(int(geometry['UiReadForm']['FontlableNumber']))
			self.lableNumber.setFont(font)
			font.setPointSize(int(geometry['UiReadForm']['FontlableGifter']))
			self.lableGifter.setFont(font)
			font.setPointSize(int(geometry['UiReadForm']['FontlablePoint']))
			self.lablePoint.setFont(font)
			font.setPointSize(int(geometry['UiReadForm']['FonttextBrowserDescription']))
			self.textBrowserDescription.setFont(font)

			self.pushButtonDelite.setFont(ButtonFontPointSize)
			self.pushButtonClose.setFont(ButtonFontPointSize)
			self.pushButtonEdit.setFont(ButtonFontPointSize)

		# Добавление функций к кнопкам
		self.pushButtonDelite.clicked.connect(lambda: self.showDialog())
		self.pushButtonClose.clicked.connect(lambda: readForm.close())
		self.pushButtonEdit.clicked.connect(lambda: self.editOpen())

	def editOpen(self):
		readForm.hide()

		uieditForm.Substitution()
		uEFT.Substitution()

		wineditForm.show()

	def retranslateUi(self, main):
		_translate = QtCore.QCoreApplication.translate
		Ui_readForm.retranslateUi(self, main)
		readForm.setWindowTitle("Данные экспоната")
		self.Title.setText(forread[1])
		self.labelSelection.setText(forread[6])
		self.labelSubselection.setText(forread[7])
		self.labelTypeFond.setText(forread[0])
		self.lableNumber.setText(str(forread[2]))
		self.lableGifter.setText(forread[3])
		self.lablePoint.setText(forread[4])
		self.textBrowserDescription.setHtml(forread[5])

	def showDialog(self): # Окно подтверждения о удалении экспоната из базы данных
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText("Вы действительно хотите удалить этот экспонат из базы данных?")
		msgBox.setWindowTitle("Удалить этот экспонат?")
		try:
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
			msgBox.setWindowIcon(icon)
		except:
			pass
		msgBox.setIcon(QMessageBox.Question)
		msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)

		returnValue = msgBox.exec()
		if returnValue == QMessageBox.Yes :
		  self.Del()

	def Del(self):  # Удаление экспоната из базы данных
		selection = forread[6]
		subselection = forread[7]

		db = cluster['Все']
		collection = db['none']
		collection.delete_one({'Name': forread[1]})

		fondSelf.refresh()
		readForm.hide()

class UiSettings(Ui_Settings):
	def setupUi(self, main):
		Ui_Settings.setupUi(self, main)
		main.setStyleSheet(style)

		try: # Установка иконки
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
			main.setWindowIcon(icon)
		except:
			pass

		if geometry != None:
			w, h = cgs('UiSettings', 'Window', 2) # Устанока геометрии объектов
			main.resize(w, h)
			main.setMaximumSize(w, h)

			x, y, w, h = cgs('UiSettings', 'Title', 4)
			self.Title.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiSettings', 'appyButton', 4)
			self.appyButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiSettings', 'themeLabel', 4)
			self.themeLabel.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiSettings', 'themeComboBox', 4)
			self.themeComboBox.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiSettings', 'geometryComboBox', 4)
			self.geometryComboBox.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('UiSettings', 'geometryLabel', 4)
			self.geometryLabel.setGeometry(QtCore.QRect(x, y, w, h))

			font = QtGui.QFont() # Установка размера рифта
			font.setPointSize(int(geometry['UiSettings']['FontTitle']))
			self.Title.setFont(font)
			font.setPointSize(int(geometry['UiSettings']['FontthemeLabel']))
			self.themeLabel.setFont(font)
			font.setPointSize(int(geometry['UiSettings']['FontthemeComboBox']))
			self.themeComboBox.setFont(font)
			font.setPointSize(int(geometry['UiSettings']['FontgeometryLabel']))
			self.geometryLabel.setFont(font)
			font.setPointSize(int(geometry['UiSettings']['FontgeometryComboBox']))
			self.geometryComboBox.setFont(font)

			self.appyButton.setFont(ButtonFontPointSize)

		self.themeComboBox.clear() # Устанока списка тем в выпадающий список из папки styles
		self.themeComboBox.addItem(config['Settings']['theme'])
		with os.scandir(os.getcwd() + '\\Resourses\\styles') as listOfEntries:  
					for entry in listOfEntries:
						if entry.is_file() and entry.name[-3:] == 'css' and entry.name[:-4] != config['Settings']['Theme']:
							self.themeComboBox.addItem(entry.name[:-4])

		self.geometryComboBox.clear() # Установка списка геометрий для объектов в выпадающий список из папки Geometry
		self.geometryComboBox.addItem(config['Settings']['geometry'])
		with os.scandir(os.getcwd() + '\\Resourses\\Geometry') as listOfEntries:  
					for entry in listOfEntries:
						if entry.is_file() and entry.name[-3:] == 'ini' and entry.name[:-4] != config['Settings']['geometry']:
							self.geometryComboBox.addItem(entry.name[:-4])
		
		self.appyButton.clicked.connect(lambda: self.appy()) # Добавление функции сохранения настроек к нопки

	def retranslateUi(self, main):
		_translate = QtCore.QCoreApplication.translate
		Ui_Settings.retranslateUi(self, main)
		main.setWindowTitle("Настройки")

	def appy(self): # Сохранение настроек
		config['Settings']['theme'] = self.themeComboBox.currentText()
		config['Settings']['geometry'] = self.geometryComboBox.currentText()

		with open('Resourses\\config.ini', 'w+', encoding ="utf8") as configfile:
			config.write(configfile)

		themeSelect()

		messageBox('Перезапуск приложения', 'Для применения настроек\n будет автоматически перезагруженно приложение')

		Main.show()
		Settings.hide()
		restart()

class editForm(Ui_addForm):
	def setupUi(self, main):
		Ui_addForm.setupUi(self, main)
		main.setStyleSheet(style)

		try: # Установка иконки
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
			main.setWindowIcon(icon)
		except:
			pass

		if geometry != None:
			w, h = cgs('addForm', 'Window', 2) # Установка геометрии объектам
			main.resize(w, h)
			main.setMaximumSize(w, h)

			x, y, w, h = cgs('addForm', 'Title', 4)
			self.Title.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'labelSelection', 4)
			self.labelSelection.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'Section', 4)
			self.Section.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'labelSubselection', 4)
			self.labelSubselection.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'Subselection', 4)
			self.Subselection.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'radioButtonFond_1', 4)
			self.radioButtonFond_1.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'radioButtonFond_2', 4)
			self.radioButtonFond_2.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'nextButton', 4)
			self.nextButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'backButton', 4)
			self.backButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'lineEditName', 4)
			self.lineEditName.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'labelName', 4)
			self.labelName.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'labelNumber', 4)
			self.labelNumber.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addForm', 'lineEditNumber', 4)
			self.lineEditNumber.setGeometry(QtCore.QRect(x, y, w, h))

			font = QtGui.QFont() # Установка размера шрифта
			font.setPointSize(int(geometry['addForm']['FontTitle']))
			self.Title.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontlabelSelection']))
			self.labelSelection.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontSection']))
			self.Section.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontlabelSubselection']))
			self.labelSubselection.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontSubselection']))
			self.Subselection.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontradioButtonFond_1']))
			self.radioButtonFond_1.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontradioButtonFond_2']))
			self.radioButtonFond_2.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontlineEditName']))
			self.lineEditName.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontlabelName']))
			self.labelName.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontlabelNumber']))
			self.labelNumber.setFont(font)
			font.setPointSize(int(geometry['addForm']['FontlineEditNumber']))
			self.lineEditNumber.setFont(font)

			self.nextButton.setFont(ButtonFontPointSize)
			self.backButton.setFont(ButtonFontPointSize)

		# Добавление функций к объектам
		self.Section.activated.connect(lambda: self.selectionClicked(self.Section.currentText()))
		self.backButton.clicked.connect(lambda: self.close())
		self.nextButton.clicked.connect(lambda: self.next())

		self.Section.addItem("Изобразительные памятники")
		self.Section.addItem("Нумизматика")
		self.Section.addItem("Археология")
		self.Section.addItem("Предметы этнографии")
		self.Section.addItem("Оружие")
		self.Section.addItem("Документы, фотографии")
		self.Section.addItem("Предметы исторической техники")
		self.Section.addItem("Предметы печатной продукции")

		self.selectionClicked(self.Section.currentText())

	def retranslateUi(self, main):
		Ui_addForm.retranslateUi(self, main)
		main.setWindowTitle("Редактирование экспоната")
		self.Title.setText("Редактировать экспонат")
		self.backButton.setText("Отмена")

	def selectionClicked(self, selection): # Установка подразделов в выпадающий список, в зависимости от выбранного раздела
		self.Subselection.clear()

		if selection == 'Изобразительные памятники':
			self.labelSubselection.setEnabled(True)
			self.Subselection.setEnabled(True)

			self.Subselection.addItem("Живопись")
			self.Subselection.addItem("Графика")
			self.Subselection.addItem("Скульптуры")
			self.Subselection.addItem('Другое')

		elif selection == 'Нумизматика':
			self.labelSubselection.setEnabled(True)
			self.Subselection.setEnabled(True)

			self.Subselection.addItem("Монеты")
			self.Subselection.addItem("Медали")
			self.Subselection.addItem("Значки")

		elif selection == 'Предметы этнографии':
			self.labelSubselection.setEnabled(True)
			self.Subselection.setEnabled(True)

			self.Subselection.addItem('Предметы быта')
			self.Subselection.addItem('Орудия труда')

		elif selection == 'Предметы печатной продукции':
			self.labelSubselection.setEnabled(True)
			self.Subselection.setEnabled(True)

			self.Subselection.addItem('Книги')
			self.Subselection.addItem('Брошуры, открытки')
			self.Subselection.addItem('Плакаты')
			self.Subselection.addItem('Другое')

		else:
			self.labelSubselection.setEnabled(False)
			self.Subselection.setEnabled(False)

		self.nextButton.setEnabled(True)

	def next(self): # Переход на следующюю страницу и сохранение текущих характеристик
		global selectionAdd
		global subselectionAdd
		global fondsAdd
		global nameAdd
		global numberAdd

		selectionAdd = self.Section.currentText()
		subselectionAdd = self.Subselection.currentText()

		if self.radioButtonFond_1.isChecked() == True:
			fondsAdd = 'Основной фонд'
		elif self.radioButtonFond_2.isChecked() == True:
			fondsAdd = 'Научно-вспомогательный фонд'

		nameAdd = self.lineEditName.text()
		numberAdd = self.lineEditNumber.text()

		wineditForm.hide()
		wineditFormTwo.show()

	def Substitution(self):
		self.Section.setCurrentText(forread[6])
		self.selectionClicked(self.Section.currentText())
		self.Subselection.setCurrentText(forread[7])

		if forread[0] == 'Основной фонд':
			self.radioButtonFond_1.setChecked(True)
		else:
			self.radioButtonFond_2.setChecked(True)

		self.lineEditName.setText(forread[1])
		self.lineEditNumber.setText(str(forread[2]))

	def close(self):
		wineditForm.hide()

class editFormPartTwo(Ui_addFormTwo):
	def setupUi(self, main):
		Ui_addFormTwo.setupUi(self, main)
		main.setStyleSheet(style)

		try: # Установка иконки
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
			main.setWindowIcon(icon)
		except:
			pass

		if geometry != None:
			w, h = cgs('addFormPartTwo', 'Window', 2) # Установка геометрии объектов
			main.resize(w, h)
			main.setMaximumSize(w, h)

			x, y, w, h = cgs('addFormPartTwo', 'Title', 4)
			self.Title.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'labelGifter', 4)
			self.labelGifter.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'lineEditGifter', 4)
			self.lineEditGifter.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'labelDescription', 4)
			self.labelDescription.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'textEditDescription', 4)
			self.textEditDescription.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'labelPoint', 4)
			self.labelPoint.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'lineEditPoint', 4)
			self.lineEditPoint.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'saveButton', 4)
			self.saveButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('addFormPartTwo', 'backButton', 4)
			self.backButton.setGeometry(QtCore.QRect(x, y, w, h))

			font = QtGui.QFont() # Установка размера шрифта
			font.setPointSize(int(geometry['addFormPartTwo']['FontTitle']))
			self.Title.setFont(font)
			font.setPointSize(int(geometry['addFormPartTwo']['FontlabelGifter']))
			self.labelGifter.setFont(font)
			font.setPointSize(int(geometry['addFormPartTwo']['FontlineEditGifter']))
			self.lineEditGifter.setFont(font)
			font.setPointSize(int(geometry['addFormPartTwo']['FontlabelDescription']))
			self.labelDescription.setFont(font)
			font.setPointSize(int(geometry['addFormPartTwo']['FonttextEditDescription']))
			self.textEditDescription.setFont(font)
			font.setPointSize(int(geometry['addFormPartTwo']['FontlabelPoint']))
			self.labelPoint.setFont(font)
			font.setPointSize(int(geometry['addFormPartTwo']['FontlineEditPoint']))
			self.lineEditPoint.setFont(font)

			self.backButton.setFont(ButtonFontPointSize)
			self.saveButton.setFont(ButtonFontPointSize)

		# Добавление функций к кнопкам
		self.backButton.clicked.connect(lambda: self.back())
		self.saveButton.clicked.connect(lambda: self.save())

	def retranslateUi(self, main):
		Ui_addFormTwo.retranslateUi(self, main)
		main.setWindowTitle("Редактирование экспоната")
		self.Title.setText("Редактировать экспонат")
		self.saveButton.setText("Изменить")

	def save(self): # Сохранение экспаната в базу данных
		selection = selectionAdd
		subselection = subselectionAdd
		fonds = fondsAdd
		Name = nameAdd
		number = numberAdd
		gifter = self.lineEditGifter.text()
		point = self.lineEditPoint.text()
		description = self.textEditDescription.toPlainText()

		db = cluster['Все']
		collection = db['none']

		post = {'fonds': fonds, 'select': selection, 'subselect': subselection , 'Name': Name, 'number': number, 'gifter': gifter, 'point': point, 'description': description}

		if Name != '':
			if str(Name) == str(forread[1]):
				collection.update_one({'Name': forread[1]}, {'$set': post})
				self.mainOpen()

			elif collection.count_documents({'Name': Name}) == 0:
				collection.update_one({'Name': forread[1]}, {'$set': post})
				self.mainOpen()

			else:
				messageBox('Ошибка названия', 'Введено название уже существующего экспоната', QMessageBox.Critical)
		else:
			messageBox('Ошибка названия', 'Не введено название экспонат', QMessageBox.Critical)

	def Substitution(self):
		self.lineEditGifter.setText(forread[3])
		self.lineEditPoint.setText(forread[4])
		self.textEditDescription.setPlainText(forread[5])

	def back(self):
		wineditFormTwo.hide()
		wineditForm.show()

	def mainOpen(self):
		wineditFormTwo.hide()
		fondSelf.refresh()

# New

class wSingIn(Ui_SingIn):
	def setupUi(self, main):
		Ui_SingIn.setupUi(self, main)
		main.setStyleSheet(style)

		try: # Установка иконки
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
			main.setWindowIcon(icon)
		except:
			pass

		if geometry != None:
			w, h = cgs('wSingIn', 'Window', 2) # Устанока геометрии объектов
			main.resize(w, h)
			main.setMaximumSize(w, h)

			x, y, w, h = cgs('wSingIn', 'Title', 4)
			self.Title.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wSingIn', 'listWidget', 4)
			self.listWidget.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wSingIn', 'editButton', 4)
			self.editButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wSingIn', 'addButton', 4)
			self.addButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wSingIn', 'removeButton', 4)
			self.removeButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wSingIn', 'exitButton', 4)
			self.exitButton.setGeometry(QtCore.QRect(x, y, w, h))

			font = QtGui.QFont() # Установка размера рифта
			font.setPointSize(int(geometry['wSingIn']['FontTitle']))
			self.Title.setFont(font)
			font.setPointSize(int(geometry['wSingIn']['FontlistWidget']))
			self.listWidget.setFont(font)

			self.editButton.setFont(ButtonFontPointSize)
			self.addButton.setFont(ButtonFontPointSize)
			self.removeButton.setFont(ButtonFontPointSize)
			self.exitButton.setFont(ButtonFontPointSize)

		self.exitButton.clicked.connect(lambda: winSingIn.close())
		self.addButton.clicked.connect(lambda: self.add())
		self.listWidget.itemDoubleClicked.connect(self.open)
		self.editButton.clicked.connect(lambda: self.edit())
		self.removeButton.clicked.connect(lambda: self.showDialog())

		global singInSelf
		singInSelf = self

	def retranslateUi(self, main):
		Ui_SingIn.retranslateUi(self, main)
		main.setWindowTitle("Выбор базы данных")

		self.listWidget.clear()
		for item in config['databases']:
			self.listWidget.addItem(item)

	def add(self):
		uADB.setupUi(winAddDB)
		winAddDB.show()

	def showDialog(self): # Окно подтверждения о удалении экспоната из базы данных
		try:
			name = str(self.listWidget.currentItem().text())
		except:
			name = None
		if name != None:
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText("Вы действительно хотите удалить запись о этой базе данных?")
			msgBox.setWindowTitle("Удалить эту запись?")
			try:
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
				msgBox.setWindowIcon(icon)
			except:
				pass
			msgBox.setIcon(QMessageBox.Question)
			msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)

			returnValue = msgBox.exec()
			if returnValue == QMessageBox.Yes :
			  self.remove(name)

	def remove(self, name):
		try:
			del config['databases'][name]

			with open('Resourses\\config.ini', 'w+', encoding ="utf8") as configfile:
				config.write(configfile)

			uWSI.retranslateUi(winSingIn)
		except:
			pass

	def edit(self):
		try:
			name = str(self.listWidget.currentItem().text())
			connect = str(config['databases'][name])

			uEDB.setLabels(name, connect)
			winEditDB.show()
		except:
			pass

	def open(self, item):
		global cluster

		name = str(item.text())
		connect = str(config['databases'][name])

		test = 'No'
		try:
			cluster = MongoClient(connect)
			cluster.server_info()
			test = 'Ok'
		except:
			messageBox('Не удалось войти в базу данных', 'Проверьте соединение с интернетом и строку подключения на ошибки')

		if test == 'Ok':
			Main.show()
			uimain.setTitle(Main, name)
			winSingIn.close()

class wAddDB(Ui_addDB):
	def setupUi(self, main):
		Ui_addDB.setupUi(self, main)
		main.setStyleSheet(style)

		try: # Установка иконки
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
			main.setWindowIcon(icon)
		except:
			pass

		if geometry != None:
			w, h = cgs('wAddDB', 'Window', 2) # Устанока геометрии объектов
			main.resize(w, h)
			main.setMaximumSize(w, h)

			x, y, w, h = cgs('wAddDB', 'Title', 4)
			self.Title.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wAddDB', 'labelName', 4)
			self.labelName.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wAddDB', 'lineName', 4)
			self.lineName.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wAddDB', 'labelConnect', 4)
			self.labelConnect.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wAddDB', 'lineConnect', 4)
			self.lineConnect.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wAddDB', 'addButton', 4)
			self.addButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wAddDB', 'closeButton', 4)
			self.closeButton.setGeometry(QtCore.QRect(x, y, w, h))

			font = QtGui.QFont() # Установка размера рифта
			font.setPointSize(int(geometry['wAddDB']['FontTitle']))
			self.Title.setFont(font)
			font.setPointSize(int(geometry['wAddDB']['FontlabelName']))
			self.labelName.setFont(font)
			font.setPointSize(int(geometry['wAddDB']['FontlineName']))
			self.lineName.setFont(font)
			font.setPointSize(int(geometry['wAddDB']['FontlabelConnect']))
			self.labelConnect.setFont(font)
			font.setPointSize(int(geometry['wAddDB']['FontlineConnect']))
			self.lineConnect.setFont(font)

			self.closeButton.setFont(ButtonFontPointSize)
			self.addButton.setFont(ButtonFontPointSize)

		self.closeButton.clicked.connect(lambda: winAddDB.close())
		self.addButton.clicked.connect(lambda: self.add())

	def retranslateUi(self, main):
		Ui_addDB.retranslateUi(self, main)
		main.setWindowTitle("Добавление базы данных")

	def add(self):
		name = str(self.lineName.text())
		connect = str(self.lineConnect.text())
		if name.strip() != '' and connect.strip() != '':
			test = 'No'
			try:
				connect.index(":")
				cluster = MongoClient(connect)
				cluster.server_info()
				test = 'Ok'
			except:
				messageBox('Не удалось добавить базу данных', 'Проверьте соединение с интернетом и строку подключения на ошибки')

			if test == 'Ok':
				config['databases'][name] = connect
				with open('Resourses\\config.ini', 'w+', encoding ="utf8") as configfile:
					config.write(configfile)
				winAddDB.close()
				uWSI.retranslateUi(winSingIn)

class wEditDB(Ui_addDB):
	def setupUi(self, main):
		Ui_addDB.setupUi(self, main)
		main.setStyleSheet(style)

		try: # Установка иконки
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
			main.setWindowIcon(icon)
		except:
			pass

		if geometry != None:
			w, h = cgs('wAddDB', 'Window', 2) # Устанока геометрии объектов
			main.resize(w, h)
			main.setMaximumSize(w, h)

			x, y, w, h = cgs('wAddDB', 'Title', 4)
			self.Title.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wAddDB', 'labelName', 4)
			self.labelName.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wAddDB', 'lineName', 4)
			self.lineName.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wAddDB', 'labelConnect', 4)
			self.labelConnect.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wAddDB', 'lineConnect', 4)
			self.lineConnect.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wAddDB', 'addButton', 4)
			self.addButton.setGeometry(QtCore.QRect(x, y, w, h))
			x, y, w, h = cgs('wAddDB', 'closeButton', 4)
			self.closeButton.setGeometry(QtCore.QRect(x, y, w, h))

			font = QtGui.QFont() # Установка размера рифта
			font.setPointSize(int(geometry['wAddDB']['FontTitle']))
			self.Title.setFont(font)
			font.setPointSize(int(geometry['wAddDB']['FontlabelName']))
			self.labelName.setFont(font)
			font.setPointSize(int(geometry['wAddDB']['FontlineName']))
			self.lineName.setFont(font)
			font.setPointSize(int(geometry['wAddDB']['FontlabelConnect']))
			self.labelConnect.setFont(font)
			font.setPointSize(int(geometry['wAddDB']['FontlineConnect']))
			self.lineConnect.setFont(font)

			self.closeButton.setFont(ButtonFontPointSize)
			self.addButton.setFont(ButtonFontPointSize)

		self.closeButton.clicked.connect(lambda: winEditDB.close())
		self.addButton.clicked.connect(lambda: self.edit())

	def retranslateUi(self, main):
		Ui_addDB.retranslateUi(self, main)
		main.setWindowTitle("Изменение записи базы данных")
		self.Title.setText("Измененить запись базы данных")
		self.addButton.setText("Изменить")

	def setLabels(self, name, connect):
		self.name = name
		self.connect = connect
		self.lineName.setText(name)
		self.lineConnect.setText(connect)

	def edit(self):
		name = str(self.lineName.text())
		connect = str(self.lineConnect.text())
		test = 'No'
		try:
			connect.index(":")
			cluster = MongoClient(connect)
			cluster.server_info()
			test = 'Ok'
		except:
			messageBox('Не удалось изменить базу данных', 'Проверьте соединение с интернетом и строку подключения на ошибки')

		if test == 'Ok':
			del config['databases'][self.name]
			config['databases'][name] = connect

			with open('Resourses\\config.ini', 'w+', encoding ="utf8") as configfile:
				config.write(configfile)

			uWSI.retranslateUi(winSingIn)
			winEditDB.close()

app = QtWidgets.QApplication(sys.argv)

Main = QtWidgets.QWidget()
uimain = main()
uimain.setupUi(Main)

winForm = QtWidgets.QWidget()
uiaddForm = addForm()
uiaddForm.setupUi(winForm)

winaddFormTwo = QtWidgets.QWidget()
ui = addFormPartTwo()
ui.setupUi(winaddFormTwo)

wineditForm = QtWidgets.QWidget()
uieditForm = editForm()
uieditForm.setupUi(wineditForm)

wineditFormTwo = QtWidgets.QWidget()
uEFT = editFormPartTwo()
uEFT.setupUi(wineditFormTwo)

winSingIn = QtWidgets.QWidget()
uWSI = wSingIn()
uWSI.setupUi(winSingIn)

winAddDB = QtWidgets.QWidget()
uADB = wAddDB()
uADB.setupUi(winAddDB)

winEditDB = QtWidgets.QWidget()
uEDB = wEditDB()
uEDB.setupUi(winEditDB)

winSingIn.show()
sys.exit(app.exec_())