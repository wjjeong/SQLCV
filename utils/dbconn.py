# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

import psycopg2

# 동작하지 않음.
def __createConnection():
    result = QSqlDatabase.isDriverAvailable('QPSQL')
    print("result ================>" ,result);
    db = QSqlDatabase.addDatabase("QPSQL", "postgresql")
    cname = db.connectionName()
    print("db.connectionName() = ", cname)
    print("db.lastError:", db.lastError().text())
    db.setHostName("localhost")
    db.setPort(5432)
    db.setDatabaseName("postgres")
    db.setUserName("postgres")
    print("######")
    db.setPassword("")
    ok = db.open()

    print("ok ==============>", ok)
    if ok == False:
        QMessageBox.critical(None, "Cannot open database",
                             "데이터베이스에 연결할 수 없습니다.\n"
                             "이 프로그램은 PostgreSQL DB연결이 필요합니다.\n\n"
                             "Cancel을 눌러 프로그램을 종료하세요.",
                             QMessageBox.Cancel)
        return False

    return True;

def createConnection(p_db_type):
    if p_db_type == 'None' or p_db_type == '' : p_db_type = 'PGS'

    try:
        if p_db_type == 'PGS':
            dbconn = psycopg2.connect(dbname="postgres", user="postgres", password="", host="localhost", port="5432")
            return dbconn
    except Exception as e:
        QMessageBox.critical(None, "Cannot open database",
                             "데이터베이스에 연결할 수 없습니다.\n"
                             "이 프로그램은 PostgreSQL DB연결이 필요합니다.\n\n"
                             "Cancel을 눌러 프로그램을 종료하세요.",
                             QMessageBox.Cancel)
    return None

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
