from PyQt5 import QtCore, QtWidgets
from os.path import basename, splitext, exists
import os

from UI import UiTranslog, show_error, show_info

from modules.Ulog import convert_ulog2csv as ulgtocsv
from modules.Txtlog import txttocsv


class TranslogWindow(QtWidgets.QMainWindow, UiTranslog):
    """
    Translog processing
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Select.clicked.connect(self.selectf)
        self.selectout.clicked.connect(self.selecoutd)
        self.Save.clicked.connect(self.saving)
        self.patch = ''
        self.outdirect = None
        self.patches = None
        self.savetype = 0

    def _on_radio_button_clicked(self, button):
        """
        Обработка нажатия на кнопку
        :param button:
        :return:
        """
        self.savetype = button.objectName()

    def selecoutd(self):
        """
        Выбор папки сохранения csv файла
        :return:
        """
        _translate = QtCore.QCoreApplication.translate
        self.outdirect = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выберите папку')
        if self.outdirect != '':
            self.Outfile.setText(_translate("Translog", self.outdirect))

    def selectf(self):
        """
        Выбор файла/файлов, проверка на правильность формата файла
        :return:
        """
        _translate = QtCore.QCoreApplication.translate
        getpatch = QtWidgets.QFileDialog.getOpenFileNames(self, "Выбор текстового файла", "",
                                                          "TEXT (*.txt *.DAT *.ulg)")
        self.patches = getpatch[0]
        self.outdirect = os.path.split(getpatch[0][0])[0]
        self.Outfile.setText(_translate("Translog", self.outdirect))
        if len(self.patches) > 0:
            for patch in self.patches:
                name, ext = splitext(basename(patch))
                if ext == '.txt' or ext == '.ulg':
                    _translate = QtCore.QCoreApplication.translate
                    self.curfile.setText(_translate("Translog", "Выбрано файлов: " + str(len(self.patches))))
                elif ext == '.DAT':
                    self.patches = ''
                    show_error("Программа не поддерживает DAT формат.\nДля DAT используйте Translog - DatCon.")
                else:
                    self.patches = ''
                    show_error("Выберите текстовый файл TXT, ULG")
        else:
            show_error("Выберите текстовый файл TXT, ULG")

    def saving(self):
        """
        Обработка логов, выбор режима обработки, сохранение csv файла
        :return:
        """
        error = False
        if self.patches is not None and self.patches != '':
            if self.outdirect is not None and self.outdirect != '':
                for patch in self.patches:
                    name, ext = splitext(basename(patch))
                    datpatcher = os.path.split(patch)[0]

                    datpatch = ""
                    count_files = 0
                    while True:
                        if self.savetype == "opt":
                            datpatch = self.outdirect + '/' + str(name) \
                                       + '_OPT' \
                                       + ' (' + str(count_files) + ')' + '.csv '
                        elif self.savetype == "full":
                            datpatch = self.outdirect + '/' + str(name) \
                                       + '_FULL' \
                                       + ' (' + str(count_files) + ')' + '.csv'

                        if exists(datpatch):
                            count_files += 1
                        else:
                            break
                    if self.savetype == "opt":
                        if ext == ".ulg":
                            ulgtocsv(str(datpatcher) + '/' + name + ext, None, self.outdirect, ';', False, count_files)
                        elif ext == ".txt":
                            txttocsv(str(datpatcher) + '/' + name + ext, self.outdirect, ';', False, count_files)
                        else:
                            show_error("Неправильный формат файла")
                            error = True
                    elif self.savetype == "full":
                        if ext == ".ulg":
                            ulgtocsv(str(datpatcher) + '/' + name + ext, None, self.outdirect, ';', True, count_files)
                        elif ext == ".txt":
                            txttocsv(str(datpatcher) + '/' + name + ext, self.outdirect, ';', True, count_files)
                        else:
                            show_error("Неправильный формат файла")
                            error = True
                    else:
                        show_error("Выберите тип сборки")
                        error = True
                if not error:
                    show_info('Завершено')
            else:
                show_error("Выберите папку для выхода")
        else:
            show_error("Выберите текстовый файл TXT, ULG")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    translog = TranslogWindow()
    translog.show()
    sys.exit(app.exec_())
