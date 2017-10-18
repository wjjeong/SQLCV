import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

import ColumnMapping
import SqlConversion
import TableMapping
import dbconnection


class MainWindow(QMainWindow):
    count = 0

    def __init__(self):
        super().__init__()
        #X,Y,W,H
        self.setGeometry(300, 40, 900, 900)
        #full window
        #screen=QtGui.QDesktopWidget().screenGeometry()
        #self.setGeometry(0,0,screen.width(),screen.height())
        #self.setWindowState(Qt.WindowMaximized)
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        bar = self.menuBar()

        file1 = bar.addMenu("파일")
        file1.addAction("나가기")

        file2 = bar.addMenu("환경설정")
        file2.addAction("접속정보")

        file3 = bar.addMenu("기준정보")
        file3.addAction("테이블매핑")
        file3.addAction("컬럼매핑")

        file4 = bar.addMenu("SQL정보")
        # file4.addAction("SQL등록")
        file4.addAction("SQL변환")

        file5 = bar.addMenu("윈도우")
        file5.addAction("Cascade")
        file5.addAction("Tiled")

        file1.triggered[QAction].connect(self.windowaction)
        file2.triggered[QAction].connect(self.windowaction)
        file3.triggered[QAction].connect(self.windowaction)
        file4.triggered[QAction].connect(self.windowaction)
        file5.triggered[QAction].connect(self.windowaction)

        self.setWindowTitle("SDC")
        self.setWindowIcon(QIcon("__ui__"+os.path.sep+"img"+os.path.sep+"database_sql01.png"))

        #SQL 변환을 기본으로 띄운다.
        MainWindow.count = MainWindow.count + 1
        sub = QMdiSubWindow()

        myWindow = SqlConversion.MyWindow()
        sub.setWidget(myWindow)
        # sub.setWindowTitle("컬럼매핑" + str(MainWindow.count))
        sub.setWindowTitle("SQL변환")
        self.mdi.addSubWindow(sub)

        sub.show()
        sub.showMaximized()

    def windowaction(self, q):
        print("triggered")

        if q.text() == "나가기":
            QCoreApplication.instance().quit()

        if q.text() == "접속정보":
            MainWindow.count = MainWindow.count + 1
            sub = QMdiSubWindow()

            myWindow = dbconnection.MyWindow()
            sub.setWidget(myWindow)
            # sub.setWindowTitle("테이블매핑" + str(MainWindow.count))
            sub.setWindowTitle("접속정보")
            self.mdi.addSubWindow(sub)

            sub.show()
            sub.showMaximized()


        if q.text() == "테이블매핑":
            MainWindow.count = MainWindow.count + 1
            sub = QMdiSubWindow()

            myWindow = TableMapping.MyWindow()
            sub.setWidget(myWindow)
            #sub.setWindowTitle("테이블매핑" + str(MainWindow.count))
            sub.setWindowTitle("테이블매핑")
            self.mdi.addSubWindow(sub)

            sub.show()
            sub.showMaximized()

        if q.text() == "컬럼매핑":
            MainWindow.count = MainWindow.count + 1
            sub = QMdiSubWindow()

            myWindow = ColumnMapping.MyWindow()
            sub.setWidget(myWindow)
            #sub.setWindowTitle("컬럼매핑" + str(MainWindow.count))
            sub.setWindowTitle("컬럼매핑")
            self.mdi.addSubWindow(sub)

            sub.show()
            sub.showMaximized()

        if q.text() == "SQL변환":
            MainWindow.count = MainWindow.count + 1
            sub = QMdiSubWindow()

            myWindow = SqlConversion.MyWindow()
            sub.setWidget(myWindow)
            # sub.setWindowTitle("컬럼매핑" + str(MainWindow.count))
            sub.setWindowTitle("SQL변환")
            self.mdi.addSubWindow(sub)

            sub.show()
            sub.showMaximized()

            # if q.text() == "SQL등록":
            #     MainWindow.count = MainWindow.count + 1
            #     sub = QMdiSubWindow()
            #
            #     myWindow = SQLMapping.MyWindow()
            #     sub.setWidget(myWindow)
            #     #sub.setWindowTitle("컬럼매핑" + str(MainWindow.count))
            #     sub.setWindowTitle("SQL등록")
            #     self.mdi.addSubWindow(sub)
            #
            #     sub.show()
            #     sub.showMaximized()



        if q.text() == "Cascade":
            self.mdi.cascadeSubWindows()

        if q.text() == "Tiled":
            self.mdi.tileSubWindows()

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()