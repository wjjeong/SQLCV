# -*- coding: utf-8 -*-
# 작성자 : 김근호
# 모듈 : 디비접속 클래스

import sys
import psycopg2 as pg2

class DBase:

    def __init__(self, dbname, user, host, passwd):
        try:
            #다른 메서드에서도 사용할수 있도록 하기 위하여 self 처리
            self._db_connection = pg2.connect('dbname=%s user=%s host=%s password=%s' %(dbname, user, host, passwd))
        except:
            print("db connection failed")
            sys.exit()

    def cursor(self):
        self._db_cur = self._db_connection.cursor()
        return self._db_cur

    def commit(self):
        try:
            self._db_connection.commit()
        except:
            print("commit failed")
            self._db_connection.rollback()
            sys.exit()

    def rollback(self):
        try:
            self._db_connection.rollback()
        except:
            print("rollback failed")
            sys.exit()

    def __del__(self):
        if self._db_connection:
            self._db_connection.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._db_connection:
            self._db_connection.close()