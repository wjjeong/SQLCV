# -*- coding: utf-8 -*-
import psycopg2
import configparser
import os
from PyQt5.QtWidgets import QMessageBox


def createConnection(p_db_type):
    if p_db_type == 'None' or p_db_type == '' : p_db_type = 'PGS'

    if os.path.exists("config.ini"):
        config = configparser.ConfigParser()
        config.read('config.ini')
        vHost = config['DBINFO']['host']  # config.ini에 DBINFO 섹션을 읽어옴
        vDbname = config['DBINFO']['dbname']
        vPort = config['DBINFO']['port']
        vUser = config['DBINFO']['user']
        vPassword = config['DBINFO']['password']

    try:
        if p_db_type == 'PGS':
            dbconn = psycopg2.connect(dbname=vDbname, user=vUser, password=vPassword, host=vHost, port=vPort)
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
