# -*- coding: utf-8 -*-
import os
import logo_rc

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import (QApplication, QDialog)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

#ui_folder = os.path.abspath(os.path.dirname('__ui__/'))
form_class = uic.loadUiType("DialogAbout.ui")[0]

class AboutWindow(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # btn 연결
        self.btnOk.clicked.connect(self.closeWindow)
        self.lblHomepage.setOpenExternalLinks(True)

    def closeWindow(self):
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mywin = AboutWindow()
    mywin.show()
    sys.exit(app.exec())