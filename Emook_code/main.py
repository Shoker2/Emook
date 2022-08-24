import threading # Стандартные
import os
import os.path
import sys
import logging
from logging.handlers import RotatingFileHandler
import traceback

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
from search import thefuzz_search
from search import thefuzz_search_id

def themeSelect(i=1):
	global config
	global geometry
	global styleSheets
	global ButtonFontPointSize
	global style
	global logo
	global configWay
	configWay = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents') + '\\emookconfig.ini'

	check_config = os.path.exists(configWay)

	if check_config == False:
		cc = open(configWay, "w+", encoding ="utf8")
		cc.write('[Settings]\ntheme = Голубая светлая\ngeometry = Стандарт\n\n[databases]')
		cc.close()

	config = configparser.ConfigParser() # Открытие config файла
	config.read(configWay, encoding ="utf8")

	try:
		geometry = configparser.ConfigParser() # Открытие файла с геометрией объектов
		geometry.read('Resourses\\Geometry\\' + config['Settings']['geometry'] + '.ini', encoding ="utf8")

		ButtonFontPointSize = QtGui.QFont() # Получение размера шрифта для всех кнопок
		ButtonFontPointSize.setPointSize(int(geometry['Additions']['ButtonFontPointSize']))
	except Exception:
		logging.critical(traceback.format_exc().replace('"', '\''))
		ButtonFontPointSize.setPointSize(11)
		geometry = None
		config['Settings']['geometry'] = 'Стандарт'

		with open(configWay, 'w+', encoding ="utf8") as configfile:
			config.write(configfile)
		if i != 2:
			themeSelect(2)

	try: # Добавляю css
		styleSheets = configparser.ConfigParser() # Открытие файла с стилями объектов
		styleSheets.read('Resourses\\styles\\' + config['Settings']['theme'] + '.ini', encoding ="utf8")
	except Exception:
		logging.critical(traceback.format_exc().replace('"', '\''))

	logo = 'Resourses\\logo.png'

log_file_name = 'Resourses\\log_records.csv'

if not(os.path.isdir("./Resourses")):
	os.makedirs('Resourses')
	os.makedirs('Resourses\\Geometry')
	os.makedirs('Resourses\\styles')

if not(os.path.exists(log_file_name)):
	with open(log_file_name, 'a+', encoding='utf-8') as f:
		f.write('timestamp,status,"text"\n')

logging.basicConfig(handlers=[RotatingFileHandler(	# Делаю настройки log файла
					filename=log_file_name, encoding='utf-8', mode='a+', maxBytes=1100000, backupCount=2)],
					format=f'%(asctime)s,%(levelname)s,"%(message)s"', 
					datefmt="%F %T", 
					level=logging.DEBUG)

logging.info('Starting...')

try:
	themeSelect()
except Exception:
	logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

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
	except Exception:
		logging.critical(traceback.format_exc().replace('"', '\''))
	msgBox.setStandardButtons(QMessageBox.Ok)
	msgBox.exec()

def restart():
	QtCore.QCoreApplication.quit()
	QtCore.QProcess.startDetached(sys.executable, sys.argv)

class main(Ui_Main):
	def setupUi(self, main):
		try:
			logging.info(f'{self.__class__.__name__} - setupUI')
			Ui_Main.setupUi(self, main)
			try:
				main.setStyleSheet(styleSheets['WindowStyles']['Main'])
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try: # Добавляю иконку
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
				main.setWindowIcon(icon)
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
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
				x, y, w, h = cgs('Main', 'pushButton_9', 4)
				self.pushButton_9.setGeometry(QtCore.QRect(x, y, w, h))
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
				self.pushButton_9.setFont(ButtonFontPointSize)

				font = QtGui.QFont()
				font.setPointSize(int(geometry['Main']['FontTitle']))
				self.Title.setFont(font)
				font.setPointSize(int(geometry['Main']['FontlabelSelection']))
				self.labelSelection.setFont(font)
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
				self.Title.setStyleSheet(str(styleSheets['Main']['Title']))
				self.labelSelection.setStyleSheet(str(styleSheets['Main']['labelSelection']))
				self.allButton.setStyleSheet(str(styleSheets['Main']['allButton']))
				self.addButton.setStyleSheet(str(styleSheets['Main']['addButton']))
				self.exitButton.setStyleSheet(str(styleSheets['Main']['exitButton']))
				self.settingsButton.setStyleSheet(str(styleSheets['Main']['settingsButton']))
				self.pushButton_1.setStyleSheet(str(styleSheets['Main']['pushButton_1']))
				self.pushButton_2.setStyleSheet(str(styleSheets['Main']['pushButton_2']))
				self.pushButton_3.setStyleSheet(str(styleSheets['Main']['pushButton_3']))
				self.pushButton_4.setStyleSheet(str(styleSheets['Main']['pushButton_4']))
				self.pushButton_5.setStyleSheet(str(styleSheets['Main']['pushButton_5']))
				self.pushButton_6.setStyleSheet(str(styleSheets['Main']['pushButton_6']))
				self.pushButton_7.setStyleSheet(str(styleSheets['Main']['pushButton_7']))
				self.pushButton_8.setStyleSheet(str(styleSheets['Main']['pushButton_8']))
				self.pushButton_9.setStyleSheet(str(styleSheets['Main']['pushButton_9']))
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))
			
			self.addButton.clicked.connect(lambda: self.addFormOpen()) #Добаляю функции к кнопкам
			self.pushButton_1.clicked.connect(lambda: self.selectionClicked(self.pushButton_1.text()))
			self.pushButton_2.clicked.connect(lambda: self.selectionClicked(self.pushButton_2.text()))
			self.pushButton_3.clicked.connect(lambda: self.selectionClicked(self.pushButton_3.text()))
			self.pushButton_4.clicked.connect(lambda: self.selectionClicked(self.pushButton_4.text()))
			self.pushButton_5.clicked.connect(lambda: self.selectionClicked(self.pushButton_5.text()))
			self.pushButton_6.clicked.connect(lambda: self.selectionClicked(self.pushButton_6.text()))
			self.pushButton_7.clicked.connect(lambda: self.selectionClicked(self.pushButton_7.text()))
			self.pushButton_8.clicked.connect(lambda: self.selectionClicked(self.pushButton_8.text()))
			self.pushButton_9.clicked.connect(lambda: self.selectionClicked(self.pushButton_9.text()))
			self.allButton.clicked.connect(lambda: self.selectionClicked(self.allButton.text()))
			self.settingsButton.clicked.connect(lambda: self.settingsOpen())
			self.exitButton.clicked.connect(lambda: self.back())
			
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def retranslateUi(self, main):
		logging.info(f'{self.__class__.__name__} - retranslateUi')
		try:
			Ui_Main.retranslateUi(self, main)
			Main.setWindowTitle("Учёт музейных фондов")
			self.exitButton.setText("Назад")
			self.Title.setText('Учёт музейных фондов')

		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def setTitle(self, name):
		logging.info(f'{self.__class__.__name__} - setTitle')
		Main.setWindowTitle("Учёт музейных фондов - " + name)

	def back(self):
		logging.info(f'{self.__class__.__name__} - back')
		try:
			Main.close()
			winEditDB.close()
			winAddDB.close()
			wineditFormTwo.close()
			wineditForm.close()
			winaddFormTwo.close()
			winForm.close()
			try:
				winSubselection.close()
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))
			try:
				readForm.close()
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			winSingIn.show()
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def selectionClicked(self, selection):
		'''
		Открытие нужного окна
		(если это раздел имеет подраздел, то открывается окно выбора подраздела)
		'''
		try:
			logging.info(f'{self.__class__.__name__} - selectionClicked')
			global winFond
			global winSubselection

			Main.hide()

			if selection == 'Изобразительные памятники' or selection == 'Нумизматика' or selection == 'Предметы этнографии' or selection == 'Предметы печатной продукции':
				winSubselection = QtWidgets.QWidget()
				uiSubselection = UiSubselection()
				uiSubselection.setupUi(winSubselection, selection)
				winSubselection.show()

			elif selection == 'Археология' or selection == 'Оружие' or selection == 'Документы, фотографии' or selection == 'Предметы исторической техники' or selection == 'Все' or 'Прочее':
				winFond = QtWidgets.QWidget()
				uiFond = Fond()
				uiFond.setupUi(winFond, selection)
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def addFormOpen(self):
		try:
			logging.info(f'{self.__class__.__name__} - addFormOpen')
			Main.hide()
			global winForm
			global winaddFormTwo
			global uiaddForm
			global UIaddFormTwo

			winForm = QtWidgets.QWidget()
			uiaddForm = addForm()
			uiaddForm.setupUi(winForm)

			winaddFormTwo = QtWidgets.QWidget()
			UIaddFormTwo = addFormPartTwo()
			UIaddFormTwo.setupUi(winaddFormTwo)

			winForm.show()
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def settingsOpen(self):
		try:
			logging.info(f'{self.__class__.__name__} - settingsOpen')
			global Settings
			Settings = QtWidgets.QWidget()
			winSettings = UiSettings()
			winSettings.setupUi(Settings)
			Settings.show()

		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

class Fond(Ui_Fond):
	def setupUi(self, main, selectionMain='', subselectionMain=''):
		try:
			logging.info(f'{self.__class__.__name__} - setupUi')
			Ui_Fond.setupUi(self, main)
			try:
				main.setStyleSheet(styleSheets['WindowStyles']['Fond'])
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try: # Установка иконки
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
				main.setWindowIcon(icon)
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
				w, h = cgs('Fond', 'Window', 2) # Установка геометрии объектам
				main.resize(w, h)
				main.setMaximumSize(w, h)

				x, y, w, h = cgs('Fond', 'Title', 4)
				self.Title.setGeometry(QtCore.QRect(x, y, w, h))
				x, y, w, h = cgs('Fond', 'listWidget', 4)
				self.listWidget.setGeometry(QtCore.QRect(x, y, w, h))
				x, y, w, h = cgs('Fond', 'search_name_button', 4)
				self.search_name_button.setGeometry(QtCore.QRect(x, y, w, h))
				x, y, w, h = cgs('Fond', 'search_name_line', 4)
				self.search_name_line.setGeometry(QtCore.QRect(x, y, w, h))
				x, y, w, h = cgs('Fond', 'labelSearch', 4)
				self.labelSearch.setGeometry(QtCore.QRect(x, y, w, h))
				x, y, w, h = cgs('Fond', 'backButton', 4)
				self.backButton.setGeometry(QtCore.QRect(x, y, w, h))
				x, y, w, h = cgs('Fond', 'labelSearch_2', 4)
				self.labelSearch_2.setGeometry(QtCore.QRect(x, y, w, h))
				x, y, w, h = cgs('Fond', 'search_num_button', 4)
				self.search_num_button.setGeometry(QtCore.QRect(x, y, w, h))
				x, y, w, h = cgs('Fond', 'search_num_line', 4)
				self.search_num_line.setGeometry(QtCore.QRect(x, y, w, h))
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
				font.setPointSize(int(geometry['Fond']['Fontsearch_name_line']))
				self.search_name_line.setFont(font)
				font.setPointSize(int(geometry['Fond']['Fontsearch_num_line']))
				self.search_num_line.setFont(font)

				self.backButton.setFont(ButtonFontPointSize)
				self.refreshButton.setFont(ButtonFontPointSize)
				self.exporthButton.setFont(ButtonFontPointSize)
				self.importButton.setFont(ButtonFontPointSize)
				self.search_name_button.setFont(ButtonFontPointSize)
				self.search_num_button.setFont(ButtonFontPointSize)
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:	# Установка тем
				self.Title.setStyleSheet(str(styleSheets['Fond']['Title']))
				self.listWidget.setStyleSheet(str(styleSheets['Fond']['listWidget']))
				self.search_name_button.setStyleSheet(str(styleSheets['Fond']['search_name_button']))
				self.search_name_line.setStyleSheet(str(styleSheets['Fond']['search_name_line']))
				self.search_num_button.setStyleSheet(str(styleSheets['Fond']['search_num_button']))
				self.search_num_line.setStyleSheet(str(styleSheets['Fond']['search_num_line']))
				self.labelSearch.setStyleSheet(str(styleSheets['Fond']['labelSearch']))
				self.backButton.setStyleSheet(str(styleSheets['Fond']['backButton']))
				self.labelSearch_2.setStyleSheet(str(styleSheets['Fond']['labelSearch_2']))
				self.refreshButton.setStyleSheet(str(styleSheets['Fond']['refreshButton']))
				self.exporthButton.setStyleSheet(str(styleSheets['Fond']['exporthButton']))
				self.importButton.setStyleSheet(str(styleSheets['Fond']['importButton']))
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			# Добавление функций к объектам
			self.listWidget.itemDoubleClicked.connect(self.openInList)
			self.search_name_button.clicked.connect(lambda: self.search_name(self.search_name_line.text()))
			self.search_num_button.clicked.connect(lambda: self.search_num(self.search_num_line.text()))
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
			self.select = selectionMain
			self.subselect = subselectionMain

			db = cluster['Все']
			collection = db['none']
			
			self.refresh(2)

			global fondSelf
			fondSelf = self
	
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def retranslateUi(self, main):
		logging.info(f'{self.__class__.__name__} - retranslateUi')
		Ui_Fond.retranslateUi(self, main)
		main.setWindowTitle("Список экспонатов")

	def refresh(self, test='1'): # Обновление списка экспонатов
		try:
			logging.info(f'{self.__class__.__name__} - refresh')
			s = []
			if self.select == 'Все':
				nameid = collection.find()
			else:
				nameid = collection.find({'select': self.select, 'subselect': self.subselect})

			if test != '1':
				winFond.show()

			self.dic_Items = {}
			self.listItems = []
			self.listid = []
			try:
				for b in nameid:
					s.append(b)
					self.listItems.append(str(b['Name']))
					self.listid.append(str(b['number']))
				
				self.listWidget.clear()
				for i in range(len(self.listItems)):
					if self.listid[i] != '':
						self.listWidget.addItem(self.listItems[i] + ' №' + self.listid[i])
						self.dic_Items[self.listItems[i] + ' №' + self.listid[i]] = self.listItems[i]
					else:
						self.listWidget.addItem(self.listItems[i])
						self.dic_Items[self.listItems[i]] = self.listItems[i]

			except Exception:
				winFond.close()
				logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл
				messageBox('Ошибка подключения', 'Не удалось открыть базу данных.')
				Main.show()
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def mainOpen(self):
		logging.info(f'{self.__class__.__name__} - mainOpen')
		winFond.hide()
		Main.show()
	
	def	search_name(self, text):
		try:
			logging.info(f'{self.__class__.__name__} - search_name')
			self.listWidget.clear()
			sorted_items = thefuzz_search(self.listItems, text)
			for item in range(len(sorted_items)):
				for b in collection.find({'Name': sorted_items[item]}):
					num = str(b['number'])
					if num != '':
						self.listWidget.addItem(sorted_items[item] + ' №' + num)
					else:
						self.listWidget.addItem(sorted_items[item])
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл
		
	def search_num(self, id): # Открытие через поиск по номеру учю записи
		try:
			logging.info(f'{self.__class__.__name__} - search_num')
			self.listWidget.clear()
			sorted_items = thefuzz_search_id(self.listid, id)
			for item in range(len(sorted_items)):
				for b in collection.find({'number': sorted_items[item]}):
					Name = str(b['Name'])
					self.listWidget.addItem(Name + ' №' + sorted_items[item])
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def openInList(self, item): # Открытие со списка
		try:
			logging.info(f'{self.__class__.__name__} - openInList')
			id = int(self.listWidget.currentRow())
			name = self.dic_Items[item.text()]
			self.open(name)
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def open(self, name): # Открытие окнв с информацией о экспонате
		try:
			logging.info(f'{self.__class__.__name__} - open')
			wineditFormTwo.hide()
			wineditForm.hide()
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
				uiRead.setupUi(readForm, forread)
				readForm.show()
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def getList(self, way): # Получает таблицу exel с базы данных
		try:
			logging.info(f'{self.__class__.__name__} - getList')
			exlName = []
			exlFond = []
			exlSelect = []
			exlSubselect = []
			exlNumber = []
			exlGifter = []
			exlPoint = []
			exlDesc = []

			if self.select == 'Все':
				nameid = collection.find()
			else:
				nameid = collection.find({'select': self.select, 'subselect': self.subselect})
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
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def setList(self, way): # Загружает экспонату с таблицы exel в базу данных
		try:
			logging.info(f'{self.__class__.__name__} - setList')
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
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def selectExel(self): # Выбор файла таблицы exel
		try:
			logging.info(f'{self.__class__.__name__} - selectExel')
			way, _ = QFileDialog.getOpenFileName(None, 'Выбрать файл', './', "Exel таблица (*.xlsx)")
			if way != '':
				thread = threading.Thread(target=self.setList(way))
				thread.start()
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def save(self): # Выбор места сохранения таблицы exel
		try:
			logging.info(f'{self.__class__.__name__} - save')
			way, _ = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File',"Данные экспонатов.xlsx", 'Exel таблица (*.xlsx)')
			if way != '':
				thread = threading.Thread(target=self.getList(way))
				thread.start()
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

class addForm(Ui_addForm):
	def setupUi(self, main):
		try:
			logging.info(f'{self.__class__.__name__} - setupUi')
			Ui_addForm.setupUi(self, main)
			try:
				main.setStyleSheet(styleSheets['WindowStyles']['addForm'])
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try: # Установка иконки
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
				main.setWindowIcon(icon)
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
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
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
				self.Title.setStyleSheet(str(styleSheets['addForm']['Title']))
				self.labelSelection.setStyleSheet(str(styleSheets['addForm']['labelSelection']))
				self.Section.setStyleSheet(str(styleSheets['addForm']['Section']))
				self.labelSubselection.setStyleSheet(str(styleSheets['addForm']['labelSubselection']))
				self.Subselection.setStyleSheet(str(styleSheets['addForm']['Subselection']))
				self.radioButtonFond_1.setStyleSheet(str(styleSheets['addForm']['radioButtonFond_1']))
				self.radioButtonFond_2.setStyleSheet(str(styleSheets['addForm']['radioButtonFond_2']))
				self.nextButton.setStyleSheet(str(styleSheets['addForm']['nextButton']))
				self.backButton.setStyleSheet(str(styleSheets['addForm']['backButton']))
				self.lineEditName.setStyleSheet(str(styleSheets['addForm']['lineEditName']))
				self.labelName.setStyleSheet(str(styleSheets['addForm']['labelName']))
				self.labelNumber.setStyleSheet(str(styleSheets['addForm']['labelNumber']))
				self.lineEditNumber.setStyleSheet(str(styleSheets['addForm']['lineEditNumber']))
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

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
			self.Section.addItem("Прочее")

			self.selectionClicked(self.Section.currentText())
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def retranslateUi(self, main):
		logging.info(f'{self.__class__.__name__} - retranslateUi')
		Ui_addForm.retranslateUi(self, main)
		main.setWindowTitle("Добавление экспоната")

	def selectionClicked(self, selection): # Установка подразделов в выпадающий список, в зависимости от выбранного раздела
		try:
			logging.info(f'{self.__class__.__name__} - selectionClicked')
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
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def next(self): # Переход на следующюю страницу и сохранение текущих характеристик
		try:
			logging.info(f'{self.__class__.__name__} - next')
			selectionAdd = self.Section.currentText()
			subselectionAdd = self.Subselection.currentText()

			if self.radioButtonFond_1.isChecked() == True:
				fondsAdd = 'Основной фонд'
			elif self.radioButtonFond_2.isChecked() == True:
				fondsAdd = 'Научно-вспомогательный фонд'

			nameAdd = self.lineEditName.text()
			numberAdd = self.lineEditNumber.text()

			winForm.hide()
			UIaddFormTwo.selectionAdd = selectionAdd
			UIaddFormTwo.subselectionAdd = subselectionAdd
			UIaddFormTwo.fondsAdd = fondsAdd
			UIaddFormTwo.nameAdd = nameAdd
			UIaddFormTwo.numberAdd = numberAdd
			winaddFormTwo.show()

		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def mainOpen(self):
		logging.info(f'{self.__class__.__name__} - mainOpen')
		winForm.hide()
		Main.show()

class addFormPartTwo(Ui_addFormTwo):
	def setupUi(self, main):
		try:
			logging.info(f'{self.__class__.__name__} - setupUi')
			Ui_addFormTwo.setupUi(self, main)
			try:
				main.setStyleSheet(styleSheets['WindowStyles']['addFormPartTwo'])
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try: # Установка иконки
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
				main.setWindowIcon(icon)
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
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
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
				self.Title.setStyleSheet(str(styleSheets['addFormPartTwo']['Title']))
				self.labelGifter.setStyleSheet(str(styleSheets['addFormPartTwo']['labelGifter']))
				self.lineEditGifter.setStyleSheet(str(styleSheets['addFormPartTwo']['lineEditGifter']))
				self.labelDescription.setStyleSheet(str(styleSheets['addFormPartTwo']['labelDescription']))
				self.textEditDescription.setStyleSheet(str(styleSheets['addFormPartTwo']['textEditDescription']))
				self.labelPoint.setStyleSheet(str(styleSheets['addFormPartTwo']['labelPoint']))
				self.lineEditPoint.setStyleSheet(str(styleSheets['addFormPartTwo']['lineEditPoint']))
				self.saveButton.setStyleSheet(str(styleSheets['addFormPartTwo']['saveButton']))
				self.backButton.setStyleSheet(str(styleSheets['addFormPartTwo']['backButton']))
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			# Добавление функций к кнопкам
			self.backButton.clicked.connect(lambda: self.back())
			self.saveButton.clicked.connect(lambda: self.save())

		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def retranslateUi(self, main):
		logging.info(f'{self.__class__.__name__} - retranslateUi')
		Ui_addFormTwo.retranslateUi(self, main)
		main.setWindowTitle("Добавление экспоната")

	def save(self): # Сохранение экспаната в базу данных
		try:
			logging.info(f'{self.__class__.__name__} - save')
			selection = self.selectionAdd
			subselection = self.subselectionAdd
			fonds = self.fondsAdd
			Name = self.nameAdd
			number = self.numberAdd

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
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def back(self):
		logging.info(f'{self.__class__.__name__} - back')
		winaddFormTwo.hide()
		winForm.show()

	def mainOpen(self):
		logging.info(f'{self.__class__.__name__} - mainOpen')
		winaddFormTwo.hide()
		Main.show()

class UiSubselection(Ui_Subselection):
	def setupUi(self, main, selectionMain=''):
		try:
			logging.info(f'{self.__class__.__name__} - setupUi')
			Ui_Subselection.setupUi(self, main)
			try:
				main.setStyleSheet(styleSheets['WindowStyles']['UiSubselection'])
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try: # Установка иконки
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
				main.setWindowIcon(icon)
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
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
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
				self.Title.setStyleSheet(str(styleSheets['UiSubselection']['Title']))
				self.labelSubselection.setStyleSheet(str(styleSheets['UiSubselection']['labelSubselection']))
				self.backButton.setStyleSheet(str(styleSheets['UiSubselection']['backButton']))
				self.pushButton_1.setStyleSheet(str(styleSheets['UiSubselection']['pushButton_1']))
				self.pushButton_2.setStyleSheet(str(styleSheets['UiSubselection']['pushButton_2']))
				self.pushButton_3.setStyleSheet(str(styleSheets['UiSubselection']['pushButton_3']))
				self.pushButton_4.setStyleSheet(str(styleSheets['UiSubselection']['pushButton_4']))
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

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
			
			self.selectionMain = selectionMain
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def retranslateUi(self, main):
		logging.info(f'{self.__class__.__name__} - retranslateUi')
		Ui_Subselection.retranslateUi(self, main)
		main.setWindowTitle("Учёт музейных фондов")

	def selectionClicked(self, subselection): # Переход к списку экспонатов
		try:
			logging.info(f'{self.__class__.__name__} - selectionClicked')

			winSubselection.hide()

			global winFond
			winFond = QtWidgets.QWidget()
			uiFond = Fond()
			uiFond.setupUi(winFond, self.selectionMain, subselection)

		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def mainOpen(self):
		logging.info(f'{self.__class__.__name__} - mainOpen')
		winSubselection.hide()
		Main.show()

class UiReadForm(Ui_readForm):
	def setupUi(self, main, forread):
		try:
			logging.info(f'{self.__class__.__name__} - setupUi')
			Ui_readForm.setupUi(self, main)
			self.forread = forread
			try:
				main.setStyleSheet(styleSheets['WindowStyles']['UiReadForm'])
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try: # Установка иконки
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
				main.setWindowIcon(icon)
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
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
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
				self.Title.setStyleSheet(str(styleSheets['UiReadForm']['Title']))
				self.titleSelection.setStyleSheet(str(styleSheets['UiReadForm']['titleSelection']))
				self.titleSubselection.setStyleSheet(str(styleSheets['UiReadForm']['titleSubselection']))
				self.labelNumber.setStyleSheet(str(styleSheets['UiReadForm']['labelNumber']))
				self.labelGifter.setStyleSheet(str(styleSheets['UiReadForm']['labelGifter']))
				self.labelDescription.setStyleSheet(str(styleSheets['UiReadForm']['labelDescription']))
				self.labelPoint.setStyleSheet(str(styleSheets['UiReadForm']['labelPoint']))
				self.labelSelection.setStyleSheet(str(styleSheets['UiReadForm']['labelSelection']))
				self.labelSubselection.setStyleSheet(str(styleSheets['UiReadForm']['labelSubselection']))
				self.labelTypeFond.setStyleSheet(str(styleSheets['UiReadForm']['labelTypeFond']))
				self.lableNumber.setStyleSheet(str(styleSheets['UiReadForm']['lableNumber']))
				self.lableGifter.setStyleSheet(str(styleSheets['UiReadForm']['lableGifter']))
				self.lablePoint.setStyleSheet(str(styleSheets['UiReadForm']['lablePoint']))
				self.textBrowserDescription.setStyleSheet(str(styleSheets['UiReadForm']['textBrowserDescription']))
				self.pushButtonDelite.setStyleSheet(str(styleSheets['UiReadForm']['pushButtonDelite']))
				self.pushButtonClose.setStyleSheet(str(styleSheets['UiReadForm']['pushButtonClose']))
				self.pushButtonEdit.setStyleSheet(str(styleSheets['UiReadForm']['pushButtonEdit']))
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			# Добавление функций к кнопкам
			self.pushButtonDelite.clicked.connect(lambda: self.showDialog())
			self.pushButtonClose.clicked.connect(lambda: readForm.close())
			self.pushButtonEdit.clicked.connect(lambda: self.editOpen())

			Ui_readForm.retranslateUi(self, main)
			readForm.setWindowTitle("Данные экспоната")
			self.Title.setText(self.forread[1])
			self.labelSelection.setText(self.forread[6])
			self.labelSubselection.setText(self.forread[7])
			self.labelTypeFond.setText(self.forread[0])
			self.lableNumber.setText(str(self.forread[2]))
			self.lableGifter.setText(self.forread[3])
			self.lablePoint.setText(self.forread[4])
			self.textBrowserDescription.setHtml(self.forread[5])
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def editOpen(self):
		try:
			logging.info(f'{self.__class__.__name__} - editOpen')
			readForm.hide()

			uieditForm.Substitution(self.forread)
			uEFT.Substitution(self.forread)

			wineditForm.show()
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def showDialog(self): # Окно подтверждения о удалении экспоната из базы данных
		try:
			logging.info(f'{self.__class__.__name__} - showDialog')
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText("Вы действительно хотите удалить этот экспонат из базы данных?")
			msgBox.setWindowTitle("Удалить этот экспонат?")
			try:
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
				msgBox.setWindowIcon(icon)

			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			msgBox.setIcon(QMessageBox.Question)
			msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)

			returnValue = msgBox.exec()
			if returnValue == QMessageBox.Yes :
				self.Del()
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def Del(self):  # Удаление экспоната из базы данных
		try:
			logging.info(f'{self.__class__.__name__} - Del')

			db = cluster['Все']
			collection = db['none']
			collection.delete_one({'Name': self.forread[1]})

			fondSelf.refresh()
			readForm.hide()
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

class UiSettings(Ui_Settings):
	def setupUi(self, main):
		try:
			logging.info(f'{self.__class__.__name__} - setupUi')
			Ui_Settings.setupUi(self, main)
			try:
				main.setStyleSheet(styleSheets['WindowStyles']['UiSettings'])
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try: # Установка иконки
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
				main.setWindowIcon(icon)
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
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
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
				self.Title.setStyleSheet(str(styleSheets['UiSettings']['Title']))
				self.appyButton.setStyleSheet(str(styleSheets['UiSettings']['appyButton']))
				self.themeLabel.setStyleSheet(str(styleSheets['UiSettings']['themeLabel']))
				self.themeComboBox.setStyleSheet(str(styleSheets['UiSettings']['themeComboBox']))
				self.geometryComboBox.setStyleSheet(str(styleSheets['UiSettings']['geometryComboBox']))
				self.geometryLabel.setStyleSheet(str(styleSheets['UiSettings']['geometryLabel']))
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			self.themeComboBox.clear() # Устанока списка тем в выпадающий список из папки styles
			self.themeComboBox.addItem(config['Settings']['theme'])
			with os.scandir(os.getcwd() + '\\Resourses\\styles') as listOfEntries:  
						for entry in listOfEntries:
							if entry.is_file() and entry.name[-3:] == 'ini' and entry.name[:-4] != config['Settings']['Theme']:
								self.themeComboBox.addItem(entry.name[:-4])

			self.geometryComboBox.clear() # Установка списка геометрий для объектов в выпадающий список из папки Geometry
			self.geometryComboBox.addItem(config['Settings']['geometry'])
			with os.scandir(os.getcwd() + '\\Resourses\\Geometry') as listOfEntries:  
						for entry in listOfEntries:
							if entry.is_file() and entry.name[-3:] == 'ini' and entry.name[:-4] != config['Settings']['geometry']:
								self.geometryComboBox.addItem(entry.name[:-4])
			
			self.appyButton.clicked.connect(lambda: self.appy()) # Добавление функции сохранения настроек к нопки
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def retranslateUi(self, main):
		logging.info(f'{self.__class__.__name__} - retranslateUi')
		Ui_Settings.retranslateUi(self, main)
		main.setWindowTitle("Настройки")

	def appy(self): # Сохранение настроек
		try:
			logging.info(f'{self.__class__.__name__} - appy')
			config['Settings']['theme'] = self.themeComboBox.currentText()
			config['Settings']['geometry'] = self.geometryComboBox.currentText()

			with open(configWay, 'w+', encoding ="utf8") as configfile:
				config.write(configfile)

			themeSelect()

			messageBox('Перезапуск приложения', 'Для применения настроек\n будет автоматически перезагруженно приложение')

			Main.show()
			Settings.hide()
			restart()

		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

class editForm(Ui_addForm):
	def setupUi(self, main):
		try:
			logging.info(f'{self.__class__.__name__} - setupUi')
			Ui_addForm.setupUi(self, main)
			try:
				main.setStyleSheet(styleSheets['WindowStyles']['addForm'])
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try: # Установка иконки
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
				main.setWindowIcon(icon)
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
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
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
				self.Title.setStyleSheet(str(styleSheets['addForm']['Title']))
				self.labelSelection.setStyleSheet(str(styleSheets['addForm']['labelSelection']))
				self.Section.setStyleSheet(str(styleSheets['addForm']['Section']))
				self.labelSubselection.setStyleSheet(str(styleSheets['addForm']['labelSubselection']))
				self.Subselection.setStyleSheet(str(styleSheets['addForm']['Subselection']))
				self.radioButtonFond_1.setStyleSheet(str(styleSheets['addForm']['radioButtonFond_1']))
				self.radioButtonFond_2.setStyleSheet(str(styleSheets['addForm']['radioButtonFond_2']))
				self.nextButton.setStyleSheet(str(styleSheets['addForm']['nextButton']))
				self.backButton.setStyleSheet(str(styleSheets['addForm']['backButton']))
				self.lineEditName.setStyleSheet(str(styleSheets['addForm']['lineEditName']))
				self.labelName.setStyleSheet(str(styleSheets['addForm']['labelName']))
				self.labelNumber.setStyleSheet(str(styleSheets['addForm']['labelNumber']))
				self.lineEditNumber.setStyleSheet(str(styleSheets['addForm']['lineEditNumber']))
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

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
			self.Section.addItem("Прочее")

			self.selectionClicked(self.Section.currentText())
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def retranslateUi(self, main):
		logging.info(f'{self.__class__.__name__} - retranslateUi')
		Ui_addForm.retranslateUi(self, main)
		main.setWindowTitle("Редактирование экспоната")
		self.Title.setText("Редактировать экспонат")
		self.backButton.setText("Отмена")

	def selectionClicked(self, selection): # Установка подразделов в выпадающий список, в зависимости от выбранного раздела
		try:
			logging.info(f'{self.__class__.__name__} - selectionClicked')
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
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def next(self): # Переход на следующюю страницу и сохранение текущих характеристик
		try:
			logging.info(f'{self.__class__.__name__} - next')
			selectionAdd = self.Section.currentText()
			subselectionAdd = self.Subselection.currentText()

			if self.radioButtonFond_1.isChecked() == True:
				fondsAdd = 'Основной фонд'
			elif self.radioButtonFond_2.isChecked() == True:
				fondsAdd = 'Научно-вспомогательный фонд'

			nameAdd = self.lineEditName.text()
			numberAdd = self.lineEditNumber.text()

			wineditForm.hide()
			uEFT.selectionAdd = selectionAdd
			uEFT.subselectionAdd = subselectionAdd
			uEFT.fondsAdd = fondsAdd
			uEFT.nameAdd = nameAdd
			uEFT.numberAdd = numberAdd
			wineditFormTwo.show()
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def Substitution(self, forread):
		try:
			logging.info(f'{self.__class__.__name__} - Substitution')
			self.Section.setCurrentText(forread[6])
			self.selectionClicked(self.Section.currentText())
			self.Subselection.setCurrentText(forread[7])

			if forread[0] == 'Основной фонд':
				self.radioButtonFond_1.setChecked(True)
			else:
				self.radioButtonFond_2.setChecked(True)

			self.lineEditName.setText(forread[1])
			self.lineEditNumber.setText(str(forread[2]))
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def close(self):
		logging.info(f'{self.__class__.__name__} - close')
		wineditForm.hide()

class editFormPartTwo(Ui_addFormTwo):
	def setupUi(self, main):
		try:
			logging.info(f'{self.__class__.__name__} - setupUi')
			Ui_addFormTwo.setupUi(self, main)
			try:
				main.setStyleSheet(styleSheets['WindowStyles']['addFormPartTwo'])
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try: # Установка иконки
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
				main.setWindowIcon(icon)
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
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
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
				self.Title.setStyleSheet(str(styleSheets['addFormPartTwo']['Title']))
				self.labelGifter.setStyleSheet(str(styleSheets['addFormPartTwo']['labelGifter']))
				self.lineEditGifter.setStyleSheet(str(styleSheets['addFormPartTwo']['lineEditGifter']))
				self.labelDescription.setStyleSheet(str(styleSheets['addFormPartTwo']['labelDescription']))
				self.textEditDescription.setStyleSheet(str(styleSheets['addFormPartTwo']['textEditDescription']))
				self.labelPoint.setStyleSheet(str(styleSheets['addFormPartTwo']['labelPoint']))
				self.lineEditPoint.setStyleSheet(str(styleSheets['addFormPartTwo']['lineEditPoint']))
				self.saveButton.setStyleSheet(str(styleSheets['addFormPartTwo']['saveButton']))
				self.backButton.setStyleSheet(str(styleSheets['addFormPartTwo']['backButton']))
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			# Добавление функций к кнопкам
			self.backButton.clicked.connect(lambda: self.back())
			self.saveButton.clicked.connect(lambda: self.save())
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def retranslateUi(self, main):
		logging.info(f'{self.__class__.__name__} - retranslateUi')
		Ui_addFormTwo.retranslateUi(self, main)
		main.setWindowTitle("Редактирование экспоната")
		self.Title.setText("Редактировать экспонат")
		self.saveButton.setText("Изменить")

	def save(self): # Сохранение экспаната в базу данных
		try:
			logging.info(f'{self.__class__.__name__} - save')
			selection = self.selectionAdd
			subselection = self.subselectionAdd
			fonds = self.fondsAdd
			Name = self.nameAdd
			number = self.numberAdd
			gifter = self.lineEditGifter.text()
			point = self.lineEditPoint.text()
			description = self.textEditDescription.toPlainText()

			db = cluster['Все']
			collection = db['none']

			post = {'fonds': fonds, 'select': selection, 'subselect': subselection , 'Name': Name, 'number': number, 'gifter': gifter, 'point': point, 'description': description}

			if Name != '':
				if str(Name) == str(self.forread[1]):
					collection.update_one({'Name': self.forread[1]}, {'$set': post})
					self.mainOpen()

				elif collection.count_documents({'Name': Name}) == 0:
					collection.update_one({'Name': self.forread[1]}, {'$set': post})
					self.mainOpen()

				else:
					messageBox('Ошибка названия', 'Введено название уже существующего экспоната', QMessageBox.Critical)
			else:
				messageBox('Ошибка названия', 'Не введено название экспонат', QMessageBox.Critical)
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def Substitution(self, forread):
		try:
			logging.info(f'{self.__class__.__name__} - Substitution')
			self.forread = forread
			self.lineEditGifter.setText(forread[3])
			self.lineEditPoint.setText(forread[4])
			self.textEditDescription.setPlainText(forread[5])
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def back(self):
		logging.info(f'{self.__class__.__name__} - back')
		wineditFormTwo.hide()
		wineditForm.show()

	def mainOpen(self):
		logging.info(f'{self.__class__.__name__} - mainOpen')
		wineditFormTwo.hide()
		fondSelf.refresh()

# Sing In	

class wSingIn(Ui_SingIn):
	def setupUi(self, main):
		try:
			logging.info(f'{self.__class__.__name__} - setupUi')
			Ui_SingIn.setupUi(self, main)
			try:
				main.setStyleSheet(styleSheets['WindowStyles']['wSingIn'])
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try: # Установка иконки
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
				main.setWindowIcon(icon)
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
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
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
				self.Title.setStyleSheet(str(styleSheets['wSingIn']['Title']))
				self.listWidget.setStyleSheet(str(styleSheets['wSingIn']['listWidget']))
				self.editButton.setStyleSheet(str(styleSheets['wSingIn']['editButton']))
				self.addButton.setStyleSheet(str(styleSheets['wSingIn']['addButton']))
				self.removeButton.setStyleSheet(str(styleSheets['wSingIn']['removeButton']))
				self.exitButton.setStyleSheet(str(styleSheets['wSingIn']['exitButton']))
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			self.exitButton.clicked.connect(lambda: winSingIn.close())
			self.addButton.clicked.connect(lambda: self.add())
			self.listWidget.itemDoubleClicked.connect(self.open)
			self.editButton.clicked.connect(lambda: self.edit())
			self.removeButton.clicked.connect(lambda: self.showDialog())
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def retranslateUi(self, main):
		try:
			logging.info(f'{self.__class__.__name__} - retranslateUi')
			Ui_SingIn.retranslateUi(self, main)
			main.setWindowTitle("Выбор базы данных")

			self.listWidget.clear()
			for item in config['databases']:
				self.listWidget.addItem(item)
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def add(self):
		logging.info(f'{self.__class__.__name__} - add')
		uADB.setupUi(winAddDB)
		winAddDB.show()

	def showDialog(self): # Окно подтверждения о удалении экспоната из базы данных
		try:
			logging.info(f'{self.__class__.__name__} - showDialog')
			try:
				name = str(self.listWidget.currentItem().text())
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))
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
				except Exception:
					logging.critical(traceback.format_exc().replace('"', '\''))

				msgBox.setIcon(QMessageBox.Question)
				msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)

				returnValue = msgBox.exec()
				if returnValue == QMessageBox.Yes :
					self.remove(name)
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def remove(self, name):
		try:
			logging.info(f'{self.__class__.__name__} - remove')
			del config['databases'][name]

			with open(configWay, 'w+', encoding ="utf8") as configfile:
				config.write(configfile)

			uWSI.retranslateUi(winSingIn)
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def edit(self):
		try:
			logging.info(f'{self.__class__.__name__} - edit')
			name = str(self.listWidget.currentItem().text())
			connect = str(config['databases'][name])

			uEDB.setLabels(name, connect)
			winEditDB.show()
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def open(self, item):
		try:
			logging.info(f'{self.__class__.__name__} - open')
			global cluster

			name = str(item.text())
			connect = str(config['databases'][name])

			test = 'No'
			try:
				cluster = MongoClient(connect)
				cluster.server_info()
				test = 'Ok'

			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))
				messageBox('Не удалось войти в базу данных', 'Проверьте соединение с интернетом и строку подключения на ошибки')

			if test == 'Ok':
				Main.show()
				uimain.setTitle(name)
				winSingIn.close()
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

class wAddDB(Ui_addDB):
	def setupUi(self, main):
		try:
			logging.info(f'{self.__class__.__name__} - setupUi')
			Ui_addDB.setupUi(self, main)
			try:
				main.setStyleSheet(styleSheets['WindowStyles']['wAddDB'])

			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try: # Установка иконки
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
				main.setWindowIcon(icon)
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
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
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
				self.Title.setStyleSheet(str(styleSheets['wAddDB']['Title']))
				self.labelName.setStyleSheet(str(styleSheets['wAddDB']['labelName']))
				self.lineName.setStyleSheet(str(styleSheets['wAddDB']['lineName']))
				self.labelConnect.setStyleSheet(str(styleSheets['wAddDB']['labelConnect']))
				self.lineConnect.setStyleSheet(str(styleSheets['wAddDB']['lineConnect']))
				self.addButton.setStyleSheet(str(styleSheets['wAddDB']['addButton']))
				self.closeButton.setStyleSheet(str(styleSheets['wAddDB']['closeButton']))
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			self.closeButton.clicked.connect(lambda: winAddDB.close())
			self.addButton.clicked.connect(lambda: self.add())
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def retranslateUi(self, main):
		logging.info(f'{self.__class__.__name__} - retranslateUi')
		Ui_addDB.retranslateUi(self, main)
		main.setWindowTitle("Добавление базы данных")

	def add(self):
		try:
			logging.info(f'{self.__class__.__name__} - add')
			name = str(self.lineName.text())
			connect = str(self.lineConnect.text())
			if name.strip() != '' and connect.strip() != '':
				test = 'No'
				try:
					connect.index(":")
					cluster = MongoClient(connect)
					cluster.server_info()
					test = 'Ok'
				except Exception:
					logging.critical(traceback.format_exc().replace('"', '\''))
					messageBox('Не удалось добавить базу данных', 'Проверьте соединение с интернетом и строку подключения на ошибки')

				if test == 'Ok':
					config['databases'][name] = connect
					with open(configWay, 'w+', encoding ="utf8") as configfile:
						config.write(configfile)
					winAddDB.close()
					uWSI.retranslateUi(winSingIn)
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

class wEditDB(Ui_addDB):
	def setupUi(self, main):
		try:
			logging.info(f'{self.__class__.__name__} - setupUi')
			Ui_addDB.setupUi(self, main)
			try:
				main.setStyleSheet(styleSheets['WindowStyles']['wAddDB'])
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try: # Установка иконки
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap(logo), QtGui.QIcon.Selected, QtGui.QIcon.On)
				main.setWindowIcon(icon)
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
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
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			try:
				self.Title.setStyleSheet(str(styleSheets['wAddDB']['Title']))
				self.labelName.setStyleSheet(str(styleSheets['wAddDB']['labelName']))
				self.lineName.setStyleSheet(str(styleSheets['wAddDB']['lineName']))
				self.labelConnect.setStyleSheet(str(styleSheets['wAddDB']['labelConnect']))
				self.lineConnect.setStyleSheet(str(styleSheets['wAddDB']['lineConnect']))
				self.addButton.setStyleSheet(str(styleSheets['wAddDB']['addButton']))
				self.closeButton.setStyleSheet(str(styleSheets['wAddDB']['closeButton']))
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))

			self.closeButton.clicked.connect(lambda: winEditDB.close())
			self.addButton.clicked.connect(lambda: self.edit())
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def retranslateUi(self, main):
		logging.info(f'{self.__class__.__name__} - retranslateUi')
		
		Ui_addDB.retranslateUi(self, main)
		main.setWindowTitle("Изменение записи базы данных")
		self.Title.setText("Измененить запись базы данных")
		self.addButton.setText("Изменить")

	def setLabels(self, name, connect):
		try:
			logging.info(f'{self.__class__.__name__} - setLabels')

			self.name = name
			self.connect = connect
			self.lineName.setText(name)
			self.lineConnect.setText(connect)
		
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

	def edit(self):
		try:
			logging.info(f'{self.__class__.__name__} - edit')

			name = str(self.lineName.text())
			connect = str(self.lineConnect.text())
			test = 'No'
			try:
				connect.index(":")
				cluster = MongoClient(connect)
				cluster.server_info()
				test = 'Ok'
			except Exception:
				logging.critical(traceback.format_exc().replace('"', '\''))
				messageBox('Не удалось изменить базу данных', 'Проверьте соединение с интернетом и строку подключения на ошибки')

			if test == 'Ok':
				del config['databases'][self.name]
				config['databases'][name] = connect

				with open(configWay, 'w+', encoding ="utf8") as configfile:
					config.write(configfile)

				uWSI.retranslateUi(winSingIn)
				winEditDB.close()
	
		except Exception:
			logging.critical(traceback.format_exc().replace('"', '\'')) # Вывожу ошибку в log файл

try:
	logging.info('windows initialization')

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

	winFond = QtWidgets.QWidget()
	uiFond = Fond()

	winSubselection = QtWidgets.QWidget()
	uiSubselection = UiSubselection()
	
	winSingIn.show()

except Exception:
	logging.critical(traceback.format_exc().replace('"', '\''))

sys.exit(app.exec_())