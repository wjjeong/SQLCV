import sys
import psycopg2 as pg2
import psycopg2.extras
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from DBaseClass import DBase
import configparser
import os
import logging
import winreg

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')
#form_class = uic.loadUiType("dbconnection.ui")[0]
ui_folder = os.path.abspath(os.path.dirname('__ui__/'))
form_class = uic.loadUiType(os.path.join(ui_folder, "DBConnectionInfo.ui"))[0]

class MyWindow(QMainWindow, form_class, DBase):
    def __init__(self):
        try:
            super().__init__()
            # DBase.__init__(self)
            # self.cur = DBase.cursor(self)
            self.setupUi(self)

            #설정된 경로가 존재하는지 확인하는 함수(있다면 자동연결, 없을 시 환경설정 창 띄우기)
            if os.path.exists("config.ini"):
                config = configparser.ConfigParser()
                config.read('config.ini')

                logging.debug(config['DBINFO']['host'])

                getHost = config['DBINFO']['host']  # config.ini에 DBINFO 섹션을 읽어옴
                getDbname = config['DBINFO']['dbname']
                getPort = config['DBINFO']['port']
                getUser = config['DBINFO']['user']
                getPassword = config['DBINFO']['password']

                self.leConnServer.setText(getHost)  # 읽어온 DBINFO 섹션정보를 텍스트박스에 세팅함
                self.leConnDbname.setText(getDbname)
                self.leConnPort.setText(getPort)
                self.leConnUsername.setText(getUser)
                self.leConnPasswd.setText(getPassword)

                print("config.ini 파일 있음")

            else:
                fw = open('config.ini', 'w')
                fw.write('[DBINFO]\n')
                fw.write('host = localhost\n')
                fw.write('dbname = postgres\n')
                fw.write('port = 5432\n')
                fw.write('user = postgres\n')
                fw.write('password = \n')
                fw.close

                self.leConnServer.setText("localhost")
                self.leConnDbname.setText("postgres")
                self.leConnPort.setText("5432")
                self.leConnUsername.setText("postgres")
                self.leConnPasswd.setText("")

                print("config.ini 파일 없어서 새로 생성")

            self.btnSave.clicked.connect(self.dbconnect)
        except:
            print("DB 접속 실패")
            QMessageBox.about(self, "오류", "설정정보가 올바르지 않습니다.")

    def dbconnect(self):
        try:
            inputHost = self.leConnServer.text()    # 텍스트박스에 있는 정보들을 변수에 저장함
            inputDbname = self.leConnDbname.text()
            inputPort = self.leConnPort.text()
            inputUser = self.leConnUsername.text()
            inputPassword = self.leConnPasswd.text()
            conn_string = "host='" + inputHost + "' dbname='" + inputDbname + "' port='" + inputPort + "' user='" + inputUser + "' password='" + inputPassword + "'"
            db_connection = pg2.connect(conn_string)     # 저장된 변수를 이용해 DB접속

            try:
                #con = dbconn.createConnection('PGS')
                cur = db_connection.cursor(cursor_factory=pg2.extras.RealDictCursor)

                qrystr = """select 1"""
                print(qrystr)
                cur.execute(qrystr)

                config = configparser.ConfigParser()
                config.read('config.ini')
                config.remove_section('DBINFO')  # 현재 config.ini에 저장되어 있는 DBINFO 섹션 삭제
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)

                config.add_section('DBINFO')  # 새로 입력한 접속정보를 config.ini의 DBINFO 섹션에 저장
                config.set('DBINFO', 'host', inputHost)
                config.set('DBINFO', 'dbname', inputDbname)
                config.set('DBINFO', 'port', inputPort)
                config.set('DBINFO', 'user', inputUser)
                config.set('DBINFO', 'password', inputPassword)
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)

                print("DB 접속 성공")
                QMessageBox.about(self, "성공", "DB 접속정보가 저장되었습니다.")

            except Exception as e:
                print("Exception 발생 : ", e)
                #QMessageBox.about(self, "오류", "PostgreSQL이 설치되지 않았습니다.")
                sys.exit(app.exec())

        except:
            print("DB 접속 실패")
            QMessageBox.warning(self, "오류", "DB 접속정보가 올바르지 않습니다.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()