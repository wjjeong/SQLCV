import sys
import psycopg2 as pg2
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from DBaseClass import DBase
import configparser
import os
import logging
import winreg

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')
form_class = uic.loadUiType("dbconnection.ui")[0]

class MyWindow(QMainWindow, form_class, DBase):
    def __init__(self):
        try:
            super().__init__()
            # DBase.__init__(self)
            # self.cur = DBase.cursor(self)
            self.setupUi(self)

            #설정된 경로가 존재하는지 확인하는 함수(있다면 자동연결, 없을 시 환경설정 창 띄우기)
            try:
                key_to_read = r'SOFTWARE\PostgreSQL'
                reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
                k = winreg.OpenKey(reg, key_to_read)
                print(k)
                print("PostgreSQL 설치 확인 완료")

                if os.path.exists("config.ini") :
                    config = configparser.ConfigParser()
                    config.read('config.ini')

                    logging.debug(config['DBINFO']['host'])

                    getHost = config['DBINFO']['host']  # config.ini에 DBINFO 섹션을 읽어옴
                    getDbname = config['DBINFO']['dbname']
                    getPort = config['DBINFO']['port']
                    getUser = config['DBINFO']['user']
                    getPassword = config['DBINFO']['password']

                    self.lineEdit.setText(getHost)  # 읽어온 DBINFO 섹션정보를 텍스트박스에 세팅함
                    self.lineEdit_2.setText(getDbname)
                    self.lineEdit_3.setText(getPort)
                    self.lineEdit_4.setText(getUser)
                    self.lineEdit_5.setText(getPassword)

                    print("config.ini 파일 있음")

                else :
                    fw = open('config.ini', 'w')
                    fw.write('[DBINFO]\n')
                    fw.write('host = localhost\n')
                    fw.write('dbname = postgres\n')
                    fw.write('port = 5432\n')
                    fw.write('user = postgres\n')
                    fw.write('password = 1234\n')
                    fw.close

                    self.lineEdit.setText("localhost")  # 읽어온 DBINFO 섹션정보를 텍스트박스에 세팅함
                    self.lineEdit_2.setText("postgres")
                    self.lineEdit_3.setText("5432")
                    self.lineEdit_4.setText("postgres")
                    self.lineEdit_5.setText("1234")

                    print("config.ini 파일 없어서 새로 생성")
            except:
                print("PostgreSQL 설치 안됨")
                QMessageBox.about(self, "오류", "PostgreSQL이 설치되어 있지 않습니다.")

            self.pushButton.clicked.connect(self.dbconnect)
        except:
            print("DB 접속 실패")
            QMessageBox.about(self, "오류", "설정정보가 올바르지 않습니다.")

    def dbconnect(self):
        try:
            inputHost = self.lineEdit.text()    # 텍스트박스에 있는 정보들을 변수에 저장함
            inputDbname = self.lineEdit_2.text()
            inputPort = self.lineEdit_3.text()
            inputUser = self.lineEdit_4.text()
            inputPassword = self.lineEdit_5.text()
            conn_string = "host='" + inputHost + "' dbname='" + inputDbname + "' port='" + inputPort + "' user='" + inputUser + "' password='" + inputPassword + "'"
            self._db_connection = pg2.connect(conn_string)     # 저장된 변수를 이용해 DB접속

            config = configparser.ConfigParser()
            config.read('config.ini')
            config.remove_section('DBINFO')     # 현재 config.ini에 저장되어 있는 DBINFO 섹션 삭제
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

            config.add_section('DBINFO')     # 새로 입력한 접속정보를 config.ini의 DBINFO 섹션에 저장
            config.set('DBINFO', 'host', inputHost)
            config.set('DBINFO', 'dbname', inputDbname)
            config.set('DBINFO', 'port', inputPort)
            config.set('DBINFO', 'user', inputUser)
            config.set('DBINFO', 'password', inputPassword)
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

            print("DB 접속 성공")
            QMessageBox.about(self, "성공", "DB 접속 성공")

            #창 종료
            #myWindow.close()
            #의문사항 : 창 종료하면서 Connect 정보를 가져가는지??어떻게?

        except:
            print("DB 접속 실패")
            QMessageBox.about(self, "오류", "DB 정보가 올바르지 않습니다.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()