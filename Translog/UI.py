from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QButtonGroup, QMessageBox


def show_error(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(text)
    msg.setWindowTitle("Ошибка")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def show_info(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle("Сообщение")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


class UiTranslog(object):
    def __init__(self):
        self.type_full = None
        self.type_opt = None
        self.type_group = None
        self.Save = None
        self.Outfile = None
        self.selectout = None
        self.curfile = None
        self.Select = None
        self.centralwidget = None

    def setupUi(self, translog):
        translog.setObjectName("Translog")
        translog.resize(520, 420)
        self.setFixedSize(520, 420)
        self.centralwidget = QtWidgets.QWidget(translog)
        self.centralwidget.setObjectName("centralwidget")
        self.Select = QtWidgets.QPushButton(self.centralwidget)
        self.Select.setGeometry(QtCore.QRect(20, 50, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Select.setFont(font)
        self.Select.setObjectName("pushButton")
        self.curfile = QtWidgets.QLabel(self.centralwidget)
        self.curfile.setGeometry(QtCore.QRect(200, 50, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.curfile.setFont(font)
        self.curfile.setObjectName("label")

        self.selectout = QtWidgets.QPushButton(self.centralwidget)
        self.selectout.setGeometry(QtCore.QRect(20, 140, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.selectout.setFont(font)
        self.selectout.setObjectName("pushButton2")
        self.Outfile = QtWidgets.QLabel(self.centralwidget)
        self.Outfile.setGeometry(QtCore.QRect(200, 140, 270, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Outfile.setFont(font)
        self.Outfile.setObjectName("label2")

        self.type_opt = QtWidgets.QRadioButton(self.centralwidget)
        self.type_opt.setGeometry(QtCore.QRect(50, 230, 195, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.type_opt.setFont(font)
        self.type_opt.setObjectName("opt")
        self.type_full = QtWidgets.QRadioButton(self.centralwidget)
        self.type_full.setGeometry(QtCore.QRect(320, 230, 90, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.type_full.setFont(font)
        self.type_full.setObjectName("full")

        self.type_group = QButtonGroup()
        self.type_group.addButton(self.type_opt)
        self.type_group.addButton(self.type_full)

        self.type_group.buttonClicked.connect(self._on_radio_button_clicked)

        self.Save = QtWidgets.QPushButton(self.centralwidget)
        self.Save.setGeometry(QtCore.QRect(160, 320, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.Save.setFont(font)
        self.Save.setObjectName("pushButton_2")
        translog.setCentralWidget(self.centralwidget)

        self.retranslateUi(translog)
        QtCore.QMetaObject.connectSlotsByName(translog)

    def retranslateUi(self, translog):
        _translate = QtCore.QCoreApplication.translate
        translog.setWindowTitle(_translate("Translog", "Translog"))
        self.Select.setText(_translate("Translog", "Выбрать"))
        self.selectout.setText(_translate("Translog", "Выбрать"))
        self.curfile.setText(_translate("Translog", "Файл не выбран"))
        self.Outfile.setText(_translate("Translog", "Папка выхода"))
        self.type_opt.setText(_translate("Translog", "Оптимизированный"))
        self.type_full.setText(_translate("Translog", "Полный"))
        self.Save.setText(_translate("Translog", "Сохранить"))
        
