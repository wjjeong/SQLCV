# -*- coding: utf-8 -*-
import os

import psycopg2
import psycopg2.extras
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import (QApplication, QDialog, QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt

from utils import (dbconn, commfunc)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

ui_folder = os.path.abspath(os.path.dirname('__ui__/'))
form_class = uic.loadUiType(os.path.join(ui_folder, "DialogCompareQuery.ui"))[0]

class CompareQueryWindow(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # btn 연결
        self.btnCloseCompareWindow.clicked.connect(self.closeWindow)

        # TableWidget 클릭 연결
        self.tblSqlCompare.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tblSqlCompare.itemClicked.connect(self.handleItemClicked)

    def viewCompareQuery(self, file_nm, sql_id):
        self.file_nm = file_nm
        self.sql_id  = sql_id
        rows = []
        try:
            con = dbconn.createConnection('PGS')
            cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            qrystr = """select 
                            A.sql_text as "asis_sql_text", A.line||' ' as "sql_line", B.sql_text as "tobe_sql_text"
                        from
                            B2EN_SC_SQL_TEXT A
                            inner join B2EN_SC_SQL_TEXT_RST B on A.file_nm = B.file_nm and A.sql_id = B.sql_id and A.line = B.line
                        where
                            A.file_nm = '{0}' and A.sql_id = '{1}'""".format(file_nm, sql_id)
            #print(qrystr)

            cur.execute(qrystr)
            rows = cur.fetchall()
        except Exception as e:
            print("Exception 발생 : ", e);
        finally:
            con.close()
            con = None

        self.tblSqlCompare.setRowCount(len(rows))

        #print(rows)
        rownum = 0
        for row in rows:
            self.tblSqlCompare.setItem(rownum, 0, QTableWidgetItem(row.get("asis_sql_text")))
            self.tblSqlCompare.setItem(rownum, 1, QTableWidgetItem(row.get("sql_line")))
            self.tblSqlCompare.setItem(rownum, 2, QTableWidgetItem(row.get("tobe_sql_text")))

            rownum += 1

        # Edit하지 않도록 수정(default로 수정 가능함)
        self.tblSqlCompare.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblSqlCompare.resizeColumnsToContents()

    def handleItemClicked(self, item):
        # print("체크되었네요", item.row())
        if item.checkState() == QtCore.Qt.Checked:
            commfunc.setTableWidgetRowColor(self.tblSqlCompare, item.row(), QtGui.QColor(85,170,0))
        else:
            commfunc.setTableWidgetRowColor(self.tblSqlCompare, item.row(), QtGui.QColor(255, 255, 255))

    def closeWindow(self):
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mywin = CompareQueryWindow()
    mywin.show()
    sys.exit(app.exec())