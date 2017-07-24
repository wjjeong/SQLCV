# -*- coding: utf-8 -*-

import os

import psycopg2
import psycopg2.extras
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTableWidgetItem, QFileDialog, QMessageBox, QAbstractItemView)
from openpyxl import (load_workbook)

from utils import dbconn

ui_folder = os.path.abspath(os.path.dirname('__ui__/'))
form_class = uic.loadUiType(os.path.join(ui_folder, "SqlConversion.ui"))[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #action 트리거 정의
        #self.actionTableMapp.triggered.connect(self.selMenuMapp)
        #self.actionColumnMapp.triggered.connect(self.selMenuMapp)
        #self.actionSqlMng.triggered.connect(self.selMenuSqlMng)

        #button 클릭 정의
        self.btnSqlMngSearch.clicked.connect(self.searchSql)
        self.btnExcelOpen.clicked.connect(self.openSqlInsertExcel)

        #TableWidget 클릭 연결
        self.tblwSqlMngSqlList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tblwSqlMngSqlList.itemClicked.connect(self.handleItemClicked)
        self.tblwSqlMngSqlList.doubleClicked.connect(self.handleItemDoubleClicked)

    def selMenuSqlMng(self):
        if self.sqlMngFrame.setVisible == False:
            self.sqlMngFrame.setVisible(True);

        if(self.tblwSqlMngSqlList.rowCount() == 0):
            self.searchSql()

    def selMenuMapp(self):
        self.sqlMngFrame.setVisible(False);

    def setColortoRow(self, table, rowIndex, color):
        for j in range(table.columnCount()):
            table.item(rowIndex, j).setBackground(color)

    def searchSql(self):
        tblSqlList = self.tblwSqlMngSqlList
        tblSqlList.setRowCount(0)

        valQryCl   = self.cbSqlMngQryCl.currentText()
        valSqlId   = self.leSqlMngSqlId.text()
        valConYn   = self.cbSqlMngConYn.currentText()
        valConDate = self.cbSqlMngConDate.currentText()

        if valQryCl   == "전체": valQryCl = "";
        if valConYn   == "전체": valConYn = "";
        if valConDate == "전체": valConDate = "";

        try:
            con = dbconn.createConnection('PGS')
            cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            qrystr = """SELECT 
	                        A.file_nm, A.sql_id, A.job_cl, A.qry_cl, 
                            (CASE A.wk_stat_cd WHEN 'C' THEN 'Y' ELSE 'N' END) AS convert_yn,
	                        TO_CHAR(A.rgs_dttm, 'YYYY.MM.DD HH24:MI') as rgs_dttm
	                    FROM
	                    	B2EN_SC_SQL_LIST A
	                    where 1=1"""
            if valQryCl != "":
                qrystr += " and A.qry_cl = '{0}'".format(valQryCl);

            if valSqlId != "":
                qrystr += " and A.sql_id = '{0}'".format(valSqlId);

            if valConYn == "Y":
                qrystr += " and A.wk_stat_cd = 'C'";
            elif valConYn == "N":
                qrystr += " and A.wk_stat_cd != 'C'";

            if valConDate != "":
                # 어떤 조건이 포함되어야 하는지 확인 필요
                qrystr += " and 1=1";

            print(qrystr)

            cur.execute(qrystr)
            rows = cur.fetchall()
        except Exception as e:
            print("Exception 발생 : ", e);
            sys.exit(app.exec())
        finally:
            con.close()
            con = None

        # itemList = [ \
        #     {'fileName': 'selx.xml', 'sqlId': 'selx.selUserList', 'sqlCl': 'SELECT', 'conversionYN': 'Y',
        #      'conversionDate': '2017.06.23 14:30'}, \
        #     {'fileName': 'selx.xml', 'sqlId': 'selx.insUser', 'sqlCl': 'INSERT', 'conversionYN': 'N',
        #      'conversionDate': ''} \
        #     ];

        # itemList를 filtering할 경우
        # if valSqlCl != "":
        #     itemList = [item for item in itemList if item.get("sqlcl") == valSqlCl]
        # if valSqlId != "":
        #     itemList = [item for item in itemList if item.get("sqlid") == valSqlId]
        tblSqlList.setRowCount(len(rows))
        rownum = 0
        for row in rows:
            item_0 = QTableWidgetItem("")
            item_0.setFlags(QtCore.Qt.ItemIsUserCheckable |
                            QtCore.Qt.ItemIsEnabled)
            item_0.setCheckState(QtCore.Qt.Unchecked)

            tblSqlList.setItem(rownum, 0, item_0)
            tblSqlList.setItem(rownum, 1, QTableWidgetItem(row.get("file_nm")))
            tblSqlList.setItem(rownum, 2, QTableWidgetItem(row.get("sql_id")))
            tblSqlList.setItem(rownum, 3, QTableWidgetItem(row.get("qry_cl")))
            tblSqlList.setItem(rownum, 4, QTableWidgetItem(row.get("convert_yn")))
            tblSqlList.setItem(rownum, 5, QTableWidgetItem(row.get("rgs_dttm")))

            rownum += 1

        tblSqlList.resizeColumnsToContents()

        # Edit하지 않도록 수정(default로 수정 가능함)
        tblSqlList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # tblSqlList.resizeRowsToContents()

    def handleItemClicked(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            # print("체크되었네요", item.row())
            self.setColortoRow(self.tblwSqlMngSqlList, item.row(), QtGui.QColor(85,170,255))
        else:
            # print("체크되지 않았네요")
            self.setColortoRow(self.tblwSqlMngSqlList, item.row(), QtGui.QColor(255, 255, 255))

            file_nm = self.tblwSqlMngSqlList.item(item.row(), 1).text()
            sql_id  = self.tblwSqlMngSqlList.item(item.row(), 2).text()

            try:
                con = dbconn.createConnection('PGS')
                cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

                qrystr = """select 
                            A.file_nm, A.sql_id, 
                            string_agg(A.sql_text, chr(10) order by A.line asc) as asis_sql,
                            string_agg(B.sql_text, chr(10) order by B.line asc) as tobe_sql
                        from
                            B2EN_SC_SQL_TEXT A
                            left outer join B2EN_SC_SQL_TEXT_RST B on A.file_nm = B.file_nm and A.sql_id = B.sql_id and A.line = B.line
                        where
                            A.file_nm = '{0}' and A.sql_id = '{1}'
                        group by A.file_nm, A.sql_id""".format(file_nm, sql_id)
                print(qrystr)

                cur.execute(qrystr)
                rows = cur.fetchall()
            except Exception as e:
                print("Exception 발생 : ", e);
                sys.exit(app.exec())
            finally:
                con.close()
                con = None

            self.txbSqlMngAsisSQL.setText(rows[0].get("asis_sql"))
            self.txbSqlMngTobeSQL.setText(rows[0].get("tobe_sql"))

    def handleItemDoubleClicked(self, item):
        print(item.row(),"가 더블클릭 되었습니다")

    #SQL 엑셀 업로드
    def openSqlInsertExcel(self):
        fname = QFileDialog.getOpenFileName(self, '엑셀파일 선택', '', '');

        if fname[0]:
            wb = load_workbook(filename=fname[0])
            colDict = [\
                            {'colName': 'fileNm', 'colMandatoryYN': 'Y', 'colMaxLength': '100'}, \
                            {'colName': 'sqlId',  'colMandatoryYN': 'Y', 'colMaxLength': '100'}, \
                            {'colName': 'jobCl',  'colMandatoryYN': 'N', 'colMaxLength': '1'}, \
                            {'colName': 'sqlText', 'colMandatoryYN': 'Y', 'colMaxLength': '100'} \
                ]
            excelRows = self.getExcelData(wb, colDict)

            sqlList = []
            lineNum = 1
            for excelRow in excelRows:
                sqlRec = {'fileNm': excelRow['fileNm'], 'sqlId': excelRow['sqlId'], 'jobCl': excelRow['jobCl']};
                if sqlRec not in sqlList:
                    sqlList.append(sqlRec)
                    print(
                        "insert into B2EN_SC_SQL_LIST (file_nm, sql_id, job_cl) values ('{0}','{1}','{2}')".format(
                            excelRow['fileNm'], excelRow['sqlId'], excelRow['jobCl']))
                    lineNum = 1
                print("insert into B2EN_SC_SQL_TEXT (file_nm, sql_id, line, sql_text) values ('{0}','{1}','{2}', '{3}')"
                      .format(excelRow['fileNm'], excelRow['sqlId'], lineNum, excelRow['sqlText']))
                lineNum += 1

    def getExcelData(self, workbook, columnDictionary, SheetName='Sheet1'):
        ws = workbook.get_sheet_by_name(SheetName)
        last_row = ws.max_row

        #반환 리스트
        recList = []

        #엑셀 정합성 체크
        validExcel = True;
        errType = 0;
        errColumns = ""
        for xlrow in ws.iter_rows(row_offset=1):
            if xlrow[0].row > last_row:break;
            else:
                col_idx = 0
                for cell in xlrow:
                    if columnDictionary[col_idx]['colMandatoryYN'] == 'Y' and (cell.value == None or cell.value == ''):
                        validExcel = False
                        errType = 1
                        errColumns += ", " + cell.column + str(cell.row)
                    elif int(columnDictionary[col_idx]['colMaxLength']) > 0 and len(cell.value) > int(columnDictionary[col_idx]['colMaxLength']):
                        validExcel = False
                        errType = 2
                        errColumns += ", " + cell.column + str(cell.row)

                    col_idx += 1

        if validExcel == False:
            if errType == 1:
                QMessageBox.warning(None, "엑셀파일 에러",
                                  "엑셀업로드에 에러가 발생하였습니다.\n\n"
                                  "{0} Cell은 빈값을 허용하지 않습니다.".format(errColumns[2:]),
                                  QMessageBox.Close)
            elif errType == 2:
                QMessageBox.warning(None, "엑셀파일 에러",
                                    "엑셀업로드에 에러가 발생하였습니다.\n\n"
                                    "{0} Cell의 값이 허용길이를 초과하였습니다".format(errColumns[2:]),
                                    QMessageBox.Close)

        else:
            for xlrow in ws.iter_rows(row_offset=1):
                if xlrow[0].row > last_row: break;
                else:
                    col_idx = 0
                    # 리스트에 추가될 레코드
                    record = {}
                    for cell in xlrow:
                        record[columnDictionary[col_idx]['colName']] = cell.value
                        col_idx += 1
                    recList.append(record)


        return recList

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mywin = MyWindow()
    mywin.show()
    sys.exit(app.exec())