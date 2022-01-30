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
			gg(self.comboBoxSearch, gFont)
			gg(self.labelSearch, gFont)
			gg(self.backButton, gFont)
			gg(self.labelSearch_2, gFont)
			gg(self.comboBoxSearch_2, gFont)
			gg(self.refreshButton, gFont)
			gg(self.exporthButton, gFont)
			gg(self.importButton, gFont)

			gFont.append(str(self.Title.font().pointSize()))
			gFont.append(str(self.labelSearch.font().pointSize()))
			gFont.append(str(self.labelSearch_2.font().pointSize()))
			gFont.append(str(self.listWidget.font().pointSize()))
			gFont.append(str(self.comboBoxSearch.font().pointSize()))
			gFont.append(str(self.comboBoxSearch_2.font().pointSize()))


			styleSheets['Fond'] = {
			'Title': self.Title.styleSheet(),
			'listWidget': self.listWidget.styleSheet(),
			'comboBoxSearch': self.comboBoxSearch.styleSheet(),
			'labelSearch': self.labelSearch.styleSheet(),
			'backButton': self.backButton.styleSheet(),
			'labelSearch_2': self.labelSearch_2.styleSheet(),
			'comboBoxSearch_2': self.comboBoxSearch_2.styleSheet(),
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

	f.write('''[Main]
Window = {}
Title = {}
labelSelection = {}
allButton = {}
addButton = {}
exitButton = {}
pushButton_1 = {}
pushButton_2 = {}
pushButton_3 = {}
pushButton_4 = {}
pushButton_5 = {}
pushButton_6 = {}
pushButton_7 = {}
pushButton_8 = {}
settingsButton = {}

FontTitle = {}
FontlabelSelection = {}

[Fond]
Window = {}
Title = {}
listWidget = {}
comboBoxSearch = {}
labelSearch = {}
backButton = {}
labelSearch_2 = {}
comboBoxSearch_2 = {}
refreshButton = {}
exporthButton = {}
importButton = {}

FontTitle = {}
FontlabelSearch = {}
FontlabelSearch_2 = {}
FontlistWidget = {}
FontcomboBoxSearch = {}
FontcomboBoxSearch_2 = {}

[addForm]
Window = {}
Title = {}
labelSelection = {}
Section = {}
labelSubselection = {}
Subselection = {}
radioButtonFond_1 = {}
radioButtonFond_2 = {}
nextButton = {}
backButton = {}
lineEditName = {}
labelName = {}
labelNumber = {}
lineEditNumber = {}

FontTitle = {}
FontlabelSelection = {}
FontSection = {}
FontlabelSubselection = {}
FontSubselection = {}
FontradioButtonFond_1 = {}
FontradioButtonFond_2 = {}
FontlineEditName = {}
FontlabelName = {}
FontlabelNumber = {}
FontlineEditNumber = {}

[addFormPartTwo]
Window = {}
Title = {}
labelGifter = {}
lineEditGifter = {}
labelDescription = {}
textEditDescription = {}
labelPoint = {}
lineEditPoint = {}
saveButton = {}
backButton = {}

FontTitle = {}
FontlabelGifter = {}
FontlineEditGifter = {}
FontlabelDescription = {}
FonttextEditDescription = {}
FontlabelPoint = {}
FontlineEditPoint = {}

[UiSubselection]
Window = {}
Title = {}
labelSubselection = {}
backButton = {}
pushButton_1 = {}
pushButton_2 = {}
pushButton_3 = {}
pushButton_4 = {}

FontTitle = {}
FontlabelSubselection = {}

[UiReadForm]
Window = {}
Title = {}
titleSelection = {}
titleSubselection = {}
labelNumber = {}
labelGifter = {}
labelDescription = {}
labelPoint = {}
labelSelection = {}
labelSubselection = {}
labelTypeFond = {}
lableNumber = {}
lableGifter = {}
lablePoint = {}
textBrowserDescription = {}
pushButtonDelite = {}
pushButtonClose = {}
pushButtonEdit = {}

FontTitle = {}
FonttitleSelection = {}
FonttitleSubselection = {}
FontlabelNumber = {}
FontlabelGifter = {}
FontlabelDescription = {}
FontlabelPoint = {}
FontlabelSelection = {}
FontlabelSubselection = {}
FontlabelTypeFond = {}
FontlableNumber = {}
FontlableGifter = {}
FontlablePoint = {}
FonttextBrowserDescription = {}

[UiSettings]
Window = {}
Title = {}
appyButton = {}
themeLabel = {}
themeComboBox = {}
geometryComboBox = {}
geometryLabel = {}

FontTitle = {}
FontthemeLabel = {}
FontthemeComboBox = {}
FontgeometryLabel = {}
FontgeometryComboBox = {}

[wSingIn]
Window = {}
Title = {}
listWidget = {}
editButton = {}
addButton = {}
removeButton = {}
exitButton = {}

FontTitle = {}
FontlistWidget = {}

[wAddDB]
Window = {}
Title = {}
labelName = {}
lineName = {}
labelConnect = {}
lineConnect = {}
addButton = {}
closeButton = {}

FontTitle = {}
FontlabelName = {}
FontlineName = {}
FontlabelConnect = {}
FontlineConnect = {}

[Additions]
ButtonFontPointSize = {}'''.format\
(gMain[0], gMain[1], gMain[2], gMain[3], gMain[4], gMain[5], gMain[6], gMain[7], gMain[8], gMain[9], gMain[10], gMain[11], gMain[12], gMain[13], gMain[14], gMain[15], gMain[16],\
	gFont[0], gFont[1], gFont[2], gFont[3], gFont[4], gFont[5], gFont[6], gFont[7], gFont[8], gFont[9], gFont[10], gFont[11], gFont[12], gFont[13], gFont[14],gFont[15], gFont[16],\
	gaddForm[0], gaddForm[1], gaddForm[2], gaddForm[3], gaddForm[4], gaddForm[5], gaddForm[6], gaddForm[7], gaddForm[8], gaddForm[9], gaddForm[10], gaddForm[11], gaddForm[12], gaddForm[13], gaddForm[14], gaddForm[15], gaddForm[16], gaddForm[17], gaddForm[18], gaddForm[19], gaddForm[20], gaddForm[21], gaddForm[22], gaddForm[23], gaddForm[24],\
	gAFT[0], gAFT[1], gAFT[2], gAFT[3], gAFT[4], gAFT[5], gAFT[6], gAFT[7], gAFT[8], gAFT[9], gAFT[10], gAFT[11], gAFT[12], gAFT[13], gAFT[14], gAFT[15], gAFT[16],\
	gSS[0], gSS[1], gSS[2], gSS[3], gSS[4], gSS[5], gSS[6], gSS[7], gSS[8], gSS[9],\
	gRF[0], gRF[1], gRF[2], gRF[3], gRF[4], gRF[5], gRF[6], gRF[7], gRF[8], gRF[9], gRF[10], gRF[11], gRF[12], gRF[13], gRF[14], gRF[15], gRF[16], gRF[17], gRF[18], gRF[19], gRF[20], gRF[21], gRF[22], gRF[23], gRF[24], gRF[25], gRF[26], gRF[27], gRF[28], gRF[29], gRF[30], gRF[31],\
	gSettings[0], gSettings[1], gSettings[2], gSettings[3], gSettings[4], gSettings[5], gSettings[6], gSettings[7], gSettings[8], gSettings[9], gSettings[10], gSettings[11],\
	gSI[0],gSI[1],gSI[2],gSI[3],gSI[4],gSI[5],gSI[6],gSI[7],gSI[8],\
	gADB[0],gADB[1],gADB[2],gADB[3],gADB[4],gADB[5],gADB[6],gADB[7],gADB[8],gADB[9],gADB[10],gADB[11],gADB[12],\
	buttonPointSize))
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