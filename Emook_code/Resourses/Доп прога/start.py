import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic
import configparser

styleSheets = configparser.ConfigParser()

NullFile = 0

def gg(object, list, i = 4):
	if i != 4:
		width = object.geometry().width()
		height = object.geometry().height()

		list.append(str(width) + ', ' + str(height))
	else:
		x = object.geometry().x()
		y = object.geometry().y()
		width = object.geometry().width()
		height = object.geometry().height()

		list.append(str(x) + ', ' + str(y) + ', ' + str(width) + ', ' + str(height))

class Main(QWidget):
	def __init__(self):
		super().__init__()
		try:
			uic.loadUi("Workspace/Main.ui", self)

			global gMain
			gMain = []
			gg(self, gMain, 2)
			gg(self.Title, gMain)
			gg(self.labelSelection, gMain)
			gg(self.allButton, gMain)
			gg(self.addButton, gMain)
			gg(self.exitButton, gMain)
			gg(self.pushButton_1, gMain)
			gg(self.pushButton_2, gMain)
			gg(self.pushButton_3, gMain)
			gg(self.pushButton_4, gMain)
			gg(self.pushButton_5, gMain)
			gg(self.pushButton_6, gMain)
			gg(self.pushButton_7, gMain)
			gg(self.pushButton_8, gMain)
			gg(self.pushButton_9, gMain)
			gg(self.settingsButton, gMain)

			gMain.append(str(self.Title.font().pointSize()))
			gMain.append(str(self.labelSelection.font().pointSize()))

			global styleSheets
			styleSheets['Main'] = {
			'Title': self.Title.styleSheet(),
			'labelSelection': self.labelSelection.styleSheet(),
			'allButton': self.allButton.styleSheet(),
			'addButton': self.addButton.styleSheet(),
			'exitButton': self.exitButton.styleSheet(),
			'pushButton_1': self.pushButton_1.styleSheet(),
			'pushButton_2': self.pushButton_2.styleSheet(),
			'pushButton_3': self.pushButton_3.styleSheet(),
			'pushButton_4': self.pushButton_4.styleSheet(),
			'pushButton_5': self.pushButton_5.styleSheet(),
			'pushButton_6': self.pushButton_6.styleSheet(),
			'pushButton_7': self.pushButton_7.styleSheet(),
			'pushButton_8': self.pushButton_8.styleSheet(),
			'pushButton_9': self.pushButton_9.styleSheet(),
			'settingsButton': self.settingsButton.styleSheet()
			}
			global WSL
			WSL = []
			WSL.append(self.styleSheet())
		except:
			global NullFile
			NullFile = 1
			print('Ошибка файла "Main.ui"')

class Fond(QWidget):
	def __init__(self):
		super().__init__()
		try:
			uic.loadUi("Workspace/Fond.ui", self)

			global gFont
			gFont = []
			gg(self, gFont, 2)
			gg(self.Title, gFont)
			gg(self.listWidget, gFont)
			gg(self.search_name_button, gFont)
			gg(self.search_name_line, gFont)
			gg(self.labelSearch, gFont)
			gg(self.backButton, gFont)
			gg(self.labelSearch_2, gFont)
			gg(self.search_num_button, gFont)
			gg(self.search_num_line, gFont)
			gg(self.refreshButton, gFont)
			gg(self.exporthButton, gFont)
			gg(self.importButton, gFont)

			gFont.append(str(self.Title.font().pointSize()))
			gFont.append(str(self.labelSearch.font().pointSize()))
			gFont.append(str(self.labelSearch_2.font().pointSize()))
			gFont.append(str(self.listWidget.font().pointSize()))
			gFont.append(str(self.search_name_line.font().pointSize()))
			gFont.append(str(self.search_num_line.font().pointSize()))

			styleSheets['Fond'] = {
			'Title': self.Title.styleSheet(),
			'listWidget': self.listWidget.styleSheet(),
			'search_name_button': self.search_name_button.styleSheet(),
			'search_name_line': self.search_name_line.styleSheet(),
			'search_num_button': self.search_name_button.styleSheet(),
			'search_num_line': self.search_name_line.styleSheet(),
			'labelSearch': self.labelSearch.styleSheet(),
			'backButton': self.backButton.styleSheet(),
			'labelSearch_2': self.labelSearch_2.styleSheet(),
			'refreshButton': self.refreshButton.styleSheet(),
			'exporthButton': self.exporthButton.styleSheet(),
			'importButton': self.importButton.styleSheet()
			}

			WSL.append(self.styleSheet())
		except:
			global NullFile
			NullFile = 1
			print('Ошибка файла "Fond.ui"')

class addForm(QWidget):
	def __init__(self):
		super().__init__()
		try:
			uic.loadUi("Workspace/addForm.ui", self)

			global gaddForm
			gaddForm = []
			gg(self, gaddForm, 2)
			gg(self.Title, gaddForm)
			gg(self.labelSelection, gaddForm)
			gg(self.Section, gaddForm)
			gg(self.labelSubselection, gaddForm)
			gg(self.Subselection, gaddForm)
			gg(self.radioButtonFond_1, gaddForm)
			gg(self.radioButtonFond_2, gaddForm)
			gg(self.nextButton, gaddForm)
			gg(self.backButton, gaddForm)
			gg(self.lineEditName, gaddForm)
			gg(self.labelName, gaddForm)
			gg(self.labelNumber, gaddForm)
			gg(self.lineEditNumber, gaddForm)

			gaddForm.append(str(self.Title.font().pointSize()))
			gaddForm.append(str(self.labelSelection.font().pointSize()))
			gaddForm.append(str(self.Section.font().pointSize()))
			gaddForm.append(str(self.labelSubselection.font().pointSize()))
			gaddForm.append(str(self.Subselection.font().pointSize()))
			gaddForm.append(str(self.radioButtonFond_1.font().pointSize()))
			gaddForm.append(str(self.radioButtonFond_2.font().pointSize()))
			gaddForm.append(str(self.lineEditName.font().pointSize()))
			gaddForm.append(str(self.labelName.font().pointSize()))
			gaddForm.append(str(self.labelNumber.font().pointSize()))
			gaddForm.append(str(self.lineEditNumber.font().pointSize()))

			styleSheets['addForm'] = {
			'Title': self.Title.styleSheet(),
			'labelSelection': self.labelSelection.styleSheet(),
			'Section': self.Section.styleSheet(),
			'labelSubselection': self.labelSubselection.styleSheet(),
			'Subselection': self.Subselection.styleSheet(),
			'radioButtonFond_1': self.radioButtonFond_1.styleSheet(),
			'radioButtonFond_2': self.radioButtonFond_2.styleSheet(),
			'nextButton': self.nextButton.styleSheet(),
			'backButton': self.backButton.styleSheet(),
			'lineEditName': self.lineEditName.styleSheet(),
			'labelName': self.labelName.styleSheet(),
			'labelNumber': self.labelNumber.styleSheet(),
			'lineEditNumber': self.lineEditNumber.styleSheet(),
			}

			WSL.append(self.styleSheet())
		except:
			global NullFile
			NullFile = 1
			print('Ошибка файла "addForm.ui"')

class addFormPartTwo(QWidget):
	def __init__(self):
		super().__init__()
		try:
			uic.loadUi("Workspace/addFormPartTwo.ui", self)

			global gAFT
			gAFT = []
			gg(self, gAFT, 2)
			gg(self.Title, gAFT)
			gg(self.labelGifter, gAFT)
			gg(self.lineEditGifter, gAFT)
			gg(self.labelDescription, gAFT)
			gg(self.textEditDescription, gAFT)
			gg(self.labelPoint, gAFT)
			gg(self.lineEditPoint, gAFT)
			gg(self.saveButton, gAFT)
			gg(self.backButton, gAFT)

			gAFT.append(str(self.Title.font().pointSize()))
			gAFT.append(str(self.labelGifter.font().pointSize()))
			gAFT.append(str(self.lineEditGifter.font().pointSize()))
			gAFT.append(str(self.labelDescription.font().pointSize()))
			gAFT.append(str(self.textEditDescription.font().pointSize()))
			gAFT.append(str(self.labelPoint.font().pointSize()))
			gAFT.append(str(self.lineEditPoint.font().pointSize()))

			styleSheets['addFormPartTwo'] = {
			'Title': self.Title.styleSheet(),
			'labelGifter': self.labelGifter.styleSheet(),
			'lineEditGifter': self.lineEditGifter.styleSheet(),
			'labelDescription': self.labelDescription.styleSheet(),
			'textEditDescription': self.textEditDescription.styleSheet(),
			'labelPoint': self.labelPoint.styleSheet(),
			'lineEditPoint': self.lineEditPoint.styleSheet(),
			'saveButton': self.saveButton.styleSheet(),
			'backButton': self.backButton.styleSheet()
			}

			WSL.append(self.styleSheet())
		except:
			global NullFile
			NullFile = 1
			print('Ошибка файла "addFormPartTwo.ui"')

class UiSubselection(QWidget):
	def __init__(self):
		super().__init__()
		try:
			uic.loadUi("Workspace/Subselection.ui", self)

			global gSS
			gSS = []
			gg(self, gSS, 2)
			gg(self.Title, gSS)
			gg(self.labelSubselection, gSS)
			gg(self.backButton, gSS)
			gg(self.pushButton_1, gSS)
			gg(self.pushButton_2, gSS)
			gg(self.pushButton_3, gSS)
			gg(self.pushButton_4, gSS)

			gSS.append(str(self.Title.font().pointSize()))
			gSS.append(str(self.labelSubselection.font().pointSize()))

			styleSheets['UiSubselection'] = {
			'Title': self.Title.styleSheet(),
			'labelSubselection': self.labelSubselection.styleSheet(),
			'backButton': self.backButton.styleSheet(),
			'pushButton_1': self.pushButton_1.styleSheet(),
			'pushButton_2': self.pushButton_2.styleSheet(),
			'pushButton_3': self.pushButton_3.styleSheet(),
			'pushButton_4': self.pushButton_4.styleSheet()
			}

			WSL.append(self.styleSheet())
		except:
			global NullFile
			NullFile = 1
			print('Ошибка файла "Subselection.ui"')

class UiReadForm(QWidget):
	def __init__(self):
		super().__init__()
		try:
			uic.loadUi("Workspace/readFond.ui", self)

			global gRF
			gRF = []
			gg(self, gRF, 2)
			gg(self.Title, gRF)
			gg(self.titleSelection, gRF)
			gg(self.titleSubselection, gRF)
			gg(self.labelNumber, gRF)
			gg(self.labelGifter, gRF)
			gg(self.labelDescription, gRF)
			gg(self.labelPoint, gRF)
			gg(self.labelSelection, gRF)
			gg(self.labelSubselection, gRF)
			gg(self.labelTypeFond, gRF)
			gg(self.lableNumber, gRF)
			gg(self.lableGifter, gRF)
			gg(self.lablePoint, gRF)
			gg(self.textBrowserDescription, gRF)
			gg(self.pushButtonDelite, gRF)
			gg(self.pushButtonClose, gRF)
			gg(self.pushButtonEdit, gRF)

			gRF.append(str(self.Title.font().pointSize()))
			gRF.append(str(self.titleSelection.font().pointSize()))
			gRF.append(str(self.titleSubselection.font().pointSize()))
			gRF.append(str(self.labelNumber.font().pointSize()))
			gRF.append(str(self.labelGifter.font().pointSize()))
			gRF.append(str(self.labelDescription.font().pointSize()))
			gRF.append(str(self.labelPoint.font().pointSize()))
			gRF.append(str(self.labelSelection.font().pointSize()))
			gRF.append(str(self.labelSubselection.font().pointSize()))
			gRF.append(str(self.labelTypeFond.font().pointSize()))
			gRF.append(str(self.lableNumber.font().pointSize()))
			gRF.append(str(self.lableGifter.font().pointSize()))
			gRF.append(str(self.lablePoint.font().pointSize()))
			gRF.append(str(self.textBrowserDescription.font().pointSize()))

			styleSheets['UiReadForm'] = {
			'Title': self.Title.styleSheet(),
			'titleSelection': self.titleSelection.styleSheet(),
			'titleSubselection': self.titleSubselection.styleSheet(),
			'labelNumber': self.labelNumber.styleSheet(),
			'labelGifter': self.labelGifter.styleSheet(),
			'labelDescription': self.labelDescription.styleSheet(),
			'labelPoint': self.labelPoint.styleSheet(),
			'labelSelection': self.labelSelection.styleSheet(),
			'labelSubselection': self.labelSubselection.styleSheet(),
			'labelTypeFond': self.labelTypeFond.styleSheet(),
			'lableNumber': self.lableNumber.styleSheet(),
			'lableGifter': self.lableGifter.styleSheet(),
			'lablePoint': self.lablePoint.styleSheet(),
			'textBrowserDescription': self.textBrowserDescription.styleSheet(),
			'pushButtonDelite': self.pushButtonDelite.styleSheet(),
			'pushButtonClose': self.pushButtonClose.styleSheet(),
			'pushButtonEdit': self.pushButtonEdit.styleSheet()
			}

			WSL.append(self.styleSheet())
		except:
			global NullFile
			NullFile = 1
			print('Ошибка файла "readFond.ui"')

class UiSettings(QWidget):
	def __init__(self):
		super().__init__()
		try:
			uic.loadUi("Workspace/Settings.ui", self)

			global gSettings
			gSettings = []
			gg(self, gSettings, 2)
			gg(self.Title, gSettings)
			gg(self.appyButton, gSettings)
			gg(self.themeLabel, gSettings)
			gg(self.themeComboBox, gSettings)
			gg(self.geometryComboBox, gSettings)
			gg(self.geometryLabel, gSettings)

			gSettings.append(str(self.Title.font().pointSize()))
			gSettings.append(str(self.themeLabel.font().pointSize()))
			gSettings.append(str(self.themeComboBox.font().pointSize()))
			gSettings.append(str(self.geometryLabel.font().pointSize()))
			gSettings.append(str(self.geometryComboBox.font().pointSize()))

			styleSheets['UiSettings'] = {
			'Title': self.Title.styleSheet(),
			'appyButton': self.appyButton.styleSheet(),
			'themeLabel': self.themeLabel.styleSheet(),
			'themeComboBox': self.themeComboBox.styleSheet(),
			'geometryComboBox': self.geometryComboBox.styleSheet(),
			'geometryLabel': self.geometryLabel.styleSheet()
			}

			WSL.append(self.styleSheet())
		except:
			global NullFile
			NullFile = 1
			print('Ошибка файла "Settings.ui"') 

class wSingIn(QWidget):
	def __init__(self):
		super().__init__()
		try:
			uic.loadUi("Workspace/singin.ui", self)

			global gSI
			gSI = []
			gg(self, gSI, 2)
			gg(self.Title, gSI)
			gg(self.listWidget, gSI)
			gg(self.editButton, gSI)
			gg(self.addButton, gSI)
			gg(self.removeButton, gSI)
			gg(self.exitButton, gSI)

			gSI.append(str(self.Title.font().pointSize()))
			gSI.append(str(self.listWidget.font().pointSize()))

			styleSheets['wSingIn'] = {
			'Title': self.Title.styleSheet(),
			'listWidget': self.listWidget.styleSheet(),
			'editButton': self.editButton.styleSheet(),
			'addButton': self.addButton.styleSheet(),
			'removeButton': self.removeButton.styleSheet(),
			'exitButton': self.exitButton.styleSheet()
			}

			WSL.append(self.styleSheet())
		except:
			global NullFile
			NullFile = 1
			print('Ошибка файла "singin.ui"')

class wAddDB(QWidget):
	def __init__(self):
		super().__init__()
		try:
			uic.loadUi("Workspace/addDB.ui", self)

			global gADB
			gADB = []
			gg(self, gADB, 2)
			gg(self.Title, gADB)
			gg(self.labelName, gADB)
			gg(self.lineName, gADB)
			gg(self.labelConnect, gADB)
			gg(self.lineConnect, gADB)
			gg(self.addButton, gADB)
			gg(self.closeButton, gADB)

			gADB.append(str(self.Title.font().pointSize()))
			gADB.append(str(self.labelName.font().pointSize()))
			gADB.append(str(self.lineName.font().pointSize()))
			gADB.append(str(self.labelConnect.font().pointSize()))
			gADB.append(str(self.lineConnect.font().pointSize()))

			styleSheets['wAddDB'] = {
			'Title': self.Title.styleSheet(),
			'labelName': self.labelName.styleSheet(),
			'lineName': self.lineName.styleSheet(),
			'labelConnect': self.labelConnect.styleSheet(),
			'lineConnect': self.lineConnect.styleSheet(),
			'addButton': self.addButton.styleSheet(),
			'closeButton': self.closeButton.styleSheet()
			}

			WSL.append(self.styleSheet())
		except:
			global NullFile
			NullFile = 1
			print('Ошибка файла "addDB.ui"')

app = QApplication(sys.argv)
MainWin = Main()
FondWin = Fond()
addFormWin = addForm()
addFormPartTwoWin = addFormPartTwo()
UiSubselectionWin = UiSubselection()
UiReadFormWin = UiReadForm()
UiSettingsWin = UiSettings()
wSingInWin = wSingIn()
wAddDBWin = wAddDB()

if NullFile == 0:
	name = input('Введите название геометрии: ')

	ok = 0
	while ok == 0:
		try:
			buttonPointSize = int(input('Размер шрифта у всех кнопок: '))
			ok = 1
		except:
			print('Размер шрифта должен содержать только цифры (1, 2, 3, 4, 5 ...)')

	f = open('' + name + '_Geometry.ini', 'w', encoding ="utf8")

	f.write(f'''[Main]
Window = {gMain[0]}
Title = {gMain[1]}
labelSelection = {gMain[2]}
allButton = {gMain[3]}
addButton = {gMain[4]}
exitButton = {gMain[5]}
pushButton_1 = {gMain[6]}
pushButton_2 = {gMain[7]}
pushButton_3 = {gMain[8]}
pushButton_4 = {gMain[9]}
pushButton_5 = {gMain[10]}
pushButton_6 = {gMain[11]}
pushButton_7 = {gMain[12]}
pushButton_8 = {gMain[13]}
pushButton_9 = {gMain[14]}
settingsButton = {gMain[15]}

FontTitle = {gMain[16]}
FontlabelSelection = {gMain[17]}

[Fond]
Window = {gFont[0]}
Title = {gFont[1]}
listWidget = {gFont[2]}
search_name_button = {gFont[3]}
search_name_line = {gFont[4]}
labelSearch = {gFont[5]}
backButton = {gFont[6]}
labelSearch_2 = {gFont[7]}
search_num_button = {gFont[8]}
search_num_line = {gFont[9]}
refreshButton = {gFont[10]}
exporthButton = {gFont[11]}
importButton = {gFont[12]}

FontTitle = {gFont[13]}
FontlabelSearch = {gFont[14]}
FontlabelSearch_2 = {gFont[15]}
FontlistWidget = {gFont[16]}
Fontsearch_name_line = {gFont[17]}
Fontsearch_num_line = {gFont[18]}

[addForm]
Window = {gaddForm[0]}
Title = {gaddForm[1]}
labelSelection = {gaddForm[2]}
Section = {gaddForm[3]}
labelSubselection = {gaddForm[4]}
Subselection = {gaddForm[5]}
radioButtonFond_1 = {gaddForm[6]}
radioButtonFond_2 = {gaddForm[7]}
nextButton = {gaddForm[8]}
backButton = {gaddForm[9]}
lineEditName = {gaddForm[10]}
labelName = {gaddForm[11]}
labelNumber = {gaddForm[12]}
lineEditNumber = {gaddForm[13]}

FontTitle = {gaddForm[14]}
FontlabelSelection = {gaddForm[15]}
FontSection = {gaddForm[16]}
FontlabelSubselection = {gaddForm[17]}
FontSubselection = {gaddForm[18]}
FontradioButtonFond_1 = {gaddForm[19]}
FontradioButtonFond_2 = {gaddForm[20]}
FontlineEditName = {gaddForm[21]}
FontlabelName = {gaddForm[22]}
FontlabelNumber = {gaddForm[23]}
FontlineEditNumber = {gaddForm[24]}

[addFormPartTwo]
Window = {gAFT[0]}
Title = {gAFT[1]}
labelGifter = {gAFT[2]}
lineEditGifter = {gAFT[3]}
labelDescription = {gAFT[4]}
textEditDescription = {gAFT[5]}
labelPoint = {gAFT[6]}
lineEditPoint = {gAFT[7]}
saveButton = {gAFT[8]}
backButton = {gAFT[9]}

FontTitle = {gAFT[10]}
FontlabelGifter = {gAFT[11]}
FontlineEditGifter = {gAFT[12]}
FontlabelDescription = {gAFT[13]}
FonttextEditDescription = {gAFT[14]}
FontlabelPoint = {gAFT[15]}
FontlineEditPoint = {gAFT[16]}

[UiSubselection]
Window = {gSS[0]}
Title = {gSS[1]}
labelSubselection = {gSS[2]}
backButton = {gSS[3]}
pushButton_1 = {gSS[4]}
pushButton_2 = {gSS[5]}
pushButton_3 = {gSS[6]}
pushButton_4 = {gSS[7]}

FontTitle = {gSS[8]}
FontlabelSubselection = {gSS[9]}

[UiReadForm]
Window = {gRF[0]}
Title = {gRF[1]}
titleSelection = {gRF[2]}
titleSubselection = {gRF[3]}
labelNumber = {gRF[4]}
labelGifter = {gRF[5]}
labelDescription = {gRF[6]}
labelPoint = {gRF[7]}
labelSelection = {gRF[8]}
labelSubselection = {gRF[9]}
labelTypeFond = {gRF[10]}
lableNumber = {gRF[11]}
lableGifter = {gRF[12]}
lablePoint = {gRF[13]}
textBrowserDescription = {gRF[14]}
pushButtonDelite = {gRF[15]}
pushButtonClose = {gRF[16]}
pushButtonEdit = {gRF[17]}

FontTitle = {gRF[18]}
FonttitleSelection = {gRF[19]}
FonttitleSubselection = {gRF[20]}
FontlabelNumber = {gRF[21]}
FontlabelGifter = {gRF[22]}
FontlabelDescription = {gRF[23]}
FontlabelPoint = {gRF[24]}
FontlabelSelection = {gRF[25]}
FontlabelSubselection = {gRF[26]}
FontlabelTypeFond = {gRF[27]}
FontlableNumber = {gRF[28]}
FontlableGifter = {gRF[29]}
FontlablePoint = {gRF[30]}
FonttextBrowserDescription = {gRF[31]}

[UiSettings]
Window = {gSettings[0]}
Title = {gSettings[1]}
appyButton = {gSettings[2]}
themeLabel = {gSettings[3]}
themeComboBox = {gSettings[4]}
geometryComboBox = {gSettings[5]}
geometryLabel = {gSettings[6]}

FontTitle = {gSettings[7]}
FontthemeLabel = {gSettings[8]}
FontthemeComboBox = {gSettings[9]}
FontgeometryLabel = {gSettings[10]}
FontgeometryComboBox = {gSettings[11]}

[wSingIn]
Window = {gSI[0]}
Title = {gSI[1]}
listWidget = {gSI[2]}
editButton = {gSI[3]}
addButton = {gSI[4]}
removeButton = {gSI[5]}
exitButton = {gSI[6]}

FontTitle = {gSI[7]}
FontlistWidget = {gSI[8]}

[wAddDB]
Window = {gADB[0]}
Title = {gADB[1]}
labelName = {gADB[2]}
lineName = {gADB[3]}
labelConnect = {gADB[4]}
lineConnect = {gADB[5]}
addButton = {gADB[6]}
closeButton = {gADB[7]}

FontTitle = {gADB[8]}
FontlabelName = {gADB[9]}
FontlineName = {gADB[10]}
FontlabelConnect = {gADB[11]}
FontlineConnect = {gADB[12]}

[Additions]
ButtonFontPointSize = {buttonPointSize}''')
	f.close()

	styleSheets['WindowStyles'] = {
	'Main': WSL[0],
	'Fond': WSL[1],
	'addForm': WSL[2],
	'addFormPartTwo': WSL[3],
	'UiSubselection': WSL[4],
	'UiReadForm': WSL[5],
	'UiSettings': WSL[6],
	'wSingIn': WSL[7],
	'wAddDB': WSL[8]
	}

	with open('' + name + '_Style.ini', 'w+', encoding ="utf8") as configfile:
		styleSheets.write(configfile)

input('\nНажмите "Enter", чтобы закрыть программу...\n')