import sys
import os
# import pyodbc
# import jpype
# import jaydebeapi
import psycopg2
import re
import logging


#log mode
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')

#global variable

#sql_wrd저장리스트
v_r_sql_text = []
#sql structure 저장리스트
v_ScQrStr = []
# 현재 seq 저장
v_set_seq_stack = []
# 괄호시작 저장
v_set_br_stack = []

j_max = 0



class DtB2enScSqlWrd(object):
    def __init__(self, file_nm=None, sql_id=None, line=None, seq=None, sql_text=None, cmnt_yn=None, set_lvl=None,
                 set_seq=None, select_cnt=None, bracket_pm=None, bracket_acm=None, bracket_stack=None,
                 bracket_stack_desc=None, desc1=None, desc2=None, pr_tab=None, tab=None, tab_als=None, tab_type=None,
                 col_alias_nm=None, column_nm=None, clsf=None, tab_scm=None):
        self.file_nm = file_nm
        self.sql_id = sql_id
        self.line = line
        self.seq = seq
        self.sql_text = sql_text
        self.cmnt_yn = cmnt_yn
        self.set_lvl = set_lvl
        self.set_seq = set_seq
        self.select_cnt = select_cnt
        self.bracket_pm = bracket_pm
        self.bracket_acm = bracket_acm
        self.bracket_stack = bracket_stack
        self.bracket_stack_desc = bracket_stack_desc
        self.desc1 = desc1
        self.desc2 = desc2
        self.pr_tab = pr_tab
        self.tab = tab
        self.tab_als = tab_als
        self.tab_type = tab_type
        self.col_alias_nm = col_alias_nm
        self.column_nm = column_nm
        self.clsf = clsf
        self.tab_scm = tab_scm

    def insert_db(self,p_conn,p_cur):

        # 분석 테이블 INSERT (테이블 , INLINE VIEW등의 PARENT 관계 등)
        insert_sql = """INSERT INTO B2EN_SC_SQL_WRD (  file_nm,sql_id,line,seq,sql_text
                                                    ,cmnt_yn,set_lvl,set_seq,select_cnt,bracket_pm
                                                    ,bracket_acm,bracket_stack,bracket_stack_desc,desc1,desc2
                                                    ,pr_tab,tab,tab_als,tab_type,col_alias_nm
                                                    ,column_nm,clsf,tab_scm) VALUES 
                                                  (  '"""+self.file_nm.replace("'","''")+"""'
                                                    ,'"""+self.sql_id.replace("'","''")+"""'
                                                    ,"""+ifnull(str(self.line),"NULL") +"""
                                                    ,"""+ifnull(str(self.seq),"NULL")+"""
                                                    ,'"""+self.sql_text.replace("'","''")+"""'
                                                    ,'"""+self.cmnt_yn+"""'
                                                    ,"""+ifnull(str(self.set_lvl) ,"NULL")+"""
                                                    ,"""+ifnull(str(self.set_seq) ,"NULL")+"""
                                                    ,"""+ifnull(str(self.select_cnt),"NULL")+"""
                                                    ,"""+ifnull(str(self.bracket_pm) ,"NULL")+"""
                                                    ,"""+ifnull(str(self.bracket_acm) ,"NULL")+"""
                                                    ,"""+ifnull(str(self.bracket_stack) ,"NULL")+"""
                                                    ,'"""+self.bracket_stack_desc+"""'
                                                    ,'"""+self.desc1+"""'
                                                    ,'"""+self.desc2+"""'
                                                    ,"""+ifnull(str(self.pr_tab) ,"NULL")+"""
                                                    ,'"""+self.tab.replace("'","''")+"""'
                                                    ,'"""+self.tab_als+"""'
                                                    ,'"""+self.tab_type+"""'
                                                    ,'"""+self.col_alias_nm.replace("'","''")+"""'
                                                    ,'"""+self.column_nm.replace("'","''")+"""'
                                                    ,'"""+self.clsf+"""'
                                                    ,'"""+self.tab_scm.replace("'","''")+"""'
                                                  )"""

        insert_sql = """INSERT INTO B2EN_SC_SQL_WRD (  file_nm,sql_id,line,seq,sql_text
                                                            ,cmnt_yn,set_lvl,set_seq,select_cnt,bracket_pm
                                                            ,bracket_acm,bracket_stack,bracket_stack_desc,desc1,desc2
                                                            ,pr_tab,tab,tab_als,tab_type,col_alias_nm
                                                            ,column_nm,clsf,tab_scm) VALUES 
                                                          (  %s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                            ,%s
                                                          )"""
        # print(insert_sql)
        p_cur.execute(insert_sql, (   self.file_nm.replace("'", "''") , self.sql_id.replace("'", "''") , ifnull(str(self.line), "0") , ifnull(str(self.seq), "0") , self.sql_text , self.cmnt_yn , ifnull(str(self.set_lvl), "0")
                                     ,ifnull(str(self.set_seq), "0") , ifnull(str(self.select_cnt), "0") , ifnull(str(self.bracket_pm), "NULL") , ifnull(str(self.bracket_acm), "0") , ifnull(str(self.bracket_stack), "0")
                                     ,self.bracket_stack_desc , self.desc1 , self.desc2 , ifnull(str(self.pr_tab), "0") , self.tab.replace("'", "''")
                                     ,self.tab_als , self.tab_type , self.col_alias_nm.replace("'", "''") , self.column_nm.replace("'", "''") , self.clsf
                                     ,self.tab_scm.replace("'", "''")))
        p_conn.commit()

        # p_cur.execute("INSERT INTO B2EN_SC_SQL_WRD WHERE FILE_NM = " + self.file_nm + "  AND SQL_ID = " + self.sql_id + "")
        # print(self.file_nm)

class DtB2enScSqlWrdRst(object):
    def __init__(self, file_nm=None, sql_id=None, line=None, seq=None, sql_text=None
                     , sql_text_rst=None, cmnt_yn=None, set_lvl=None,set_seq=None, select_cnt=None
                     , bracket_pm=None, bracket_acm=None, bracket_stack=None, bracket_stack_desc=None, desc1=None
                     , desc2=None, pr_tab=None, tab=None, tab_als=None, tab_type=None
                     , col_alias_nm=None, column_nm=None, clsf=None, tab_scm=None):

        self.file_nm = file_nm
        self.sql_id = sql_id
        self.line = line
        self.seq = seq
        self.sql_text = sql_text

        self.sql_text_rst = sql_text_rst
        self.cmnt_yn = cmnt_yn
        self.set_lvl = set_lvl
        self.set_seq = set_seq
        self.select_cnt = select_cnt

        self.bracket_pm = bracket_pm
        self.bracket_acm = bracket_acm
        self.bracket_stack = bracket_stack
        self.bracket_stack_desc = bracket_stack_desc
        self.desc1 = desc1

        self.desc2 = desc2
        self.pr_tab = pr_tab
        self.tab = tab
        self.tab_als = tab_als
        self.tab_type = tab_type

        self.col_alias_nm = col_alias_nm
        self.column_nm = column_nm
        self.clsf = clsf
        self.tab_scm = tab_scm


    def insert_db(self,p_conn,p_cur):

        # 분석 테이블 INSERT (테이블 , INLINE VIEW등의 PARENT 관계 등)
        insert_sql = """INSERT INTO B2EN_SC_SQL_WRD_RST (file_nm, sql_id, line, seq, sql_text 
                                                    , sql_text_rst, cmnt_yn, set_lvl, set_seq, select_cnt
                                                    , bracket_pm, bracket_acm, bracket_stack, bracket_stack_desc, desc1
                                                    , desc2, pr_tab, tab, tab_als, tab_type
                                                    , col_alias_nm, column_nm, clsf, tab_scm) VALUES 
                                                  (  '"""+self.file_nm.replace("'","''")+"""'
                                                    ,'"""+self.sql_id.replace("'","''")+"""'
                                                    ,"""+ifnull(str(self.line),"NULL") +"""
                                                    ,"""+ifnull(str(self.seq),"NULL")+"""
                                                    ,'"""+self.sql_text.replace("'","''")+"""'
                                                    ,'"""+self.sql_text_rst.replace("'","''")+"""'
                                                    ,'"""+self.cmnt_yn+"""'
                                                    ,"""+ifnull(str(self.set_lvl) ,"NULL")+"""
                                                    ,"""+ifnull(str(self.set_seq) ,"NULL")+"""
                                                    ,"""+ifnull(str(self.select_cnt),"NULL")+"""
                                                    ,"""+ifnull(str(self.bracket_pm) ,"NULL")+"""
                                                    ,"""+ifnull(str(self.bracket_acm) ,"NULL")+"""
                                                    ,"""+ifnull(str(self.bracket_stack) ,"NULL")+"""
                                                    ,'"""+self.bracket_stack_desc+"""'
                                                    ,'"""+self.desc1+"""'
                                                    ,'"""+self.desc2+"""'
                                                    ,"""+ifnull(str(self.pr_tab) ,"NULL")+"""
                                                    ,'"""+self.tab.replace("'","''")+"""'
                                                    ,'"""+self.tab_als+"""'
                                                    ,'"""+self.tab_type+"""'
                                                    ,'"""+self.col_alias_nm.replace("'","''")+"""'
                                                    ,'"""+self.column_nm.replace("'","''")+"""'
                                                    ,'"""+self.clsf+"""'
                                                    ,'"""+self.tab_scm.replace("'","''")+"""'
                                                  )"""

        # print(ifnull(str(self.pr_tab) ,"NULL"))
        logging.debug(insert_sql)
        p_cur.execute(insert_sql)
        p_conn.commit()


class DtB2enScSqlTextRst(object):

    def __init__(self, file_nm=None, sql_id=None, line=None, sql_text=None, job_cl=None):
        self.file_nm = file_nm
        self.sql_id = sql_id
        self.line = line
        self.sql_text = sql_text
        self.job_cl = job_cl

    def insert_db(self,p_conn,p_cur):
        insert_sql = """INSERT INTO B2EN_SC_SQL_TEXT_RST (file_nm, sql_id, line, sql_text, job_cl) VALUES
                                                      (  '""" + self.file_nm.replace("'", "''") + """'
                                                        ,'""" + self.sql_id.replace("'", "''") + """'
                                                        ,""" + ifnull(str(self.line), "NULL") + """
                                                        ,'""" + self.sql_text.replace("'", "''") + """'
                                                        ,'""" + self.job_cl.replace("'", "''") + """'
                                                      )"""

        p_cur.execute(insert_sql)
        p_conn.commit()

class DtB2enScQrStr(object):
    def __init__(self, file_nm=None, sql_id=None, st_seq=None, col_end_seq=None, end_seq=None, cont=None, set_lvl=None, ct_clsf=None,ct_seq=None, ct_nm=None,st_alias=None, alias=None, nm_seq=None,rel_set=None,prior_set=None, mix_yn=None):
        self.file_nm = file_nm
        self.sql_id = sql_id
        self.st_seq = st_seq
        self.col_end_seq = col_end_seq
        self.end_seq = end_seq
        self.cont = cont
        self.set_lvl = set_lvl
        self.ct_clsf = ct_clsf
        self.ct_seq = ct_seq
        self.ct_nm = ct_nm
        self.st_alias = st_alias
        self.alias = alias
        self.nm_seq = nm_seq
        self.rel_set = rel_set
        self.prior_set = prior_set
        self.mix_yn= mix_yn

    def insert_db(self, p_conn, p_cur):
        #따옴표가 짤릴경우 에러가남 바인드변수 처리시 해결될듯
        v_cont = self.cont.replace("'", "''")[0:99]
        v_cnt = len(v_cont) - len(v_cont.replace("'",""))
        if divmod(v_cnt,2) == 1 :
            v_cont = v_cont + "'"

        # logging.debug("st_seq :"+str(self.st_seq)+" , "+self.alias)

        insert_sql = """INSERT INTO B2EN_SC_QRY_STR ( file_nm,sql_id,st_seq,col_end_seq,end_seq,cont,set_lvl,ct_clsf,ct_seq,ct_nm,st_alias,alias,nm_seq,rel_set,prior_set,mix_yn) VALUES
                                                      (  '""" + self.file_nm.replace("'", "''") + """'
                                                        ,'""" + self.sql_id.replace("'", "''") + """'
                                                        ,""" + ifnull(str(self.st_seq), "NULL") + """
                                                        ,""" + ifnull(str(self.col_end_seq), "NULL") + """
                                                        ,""" + ifnull(str(self.end_seq), "NULL") + """
                                                        ,'""" + v_cont  + """'
                                                        ,""" + ifnull(str(self.set_lvl), "NULL") + """
                                                        ,'""" + self.ct_clsf.replace("'", "''") + """'
                                                        ,""" + ifnull(str(self.ct_seq), "NULL") + """
                                                        ,'""" + self.ct_nm.replace("'", "''") + """'
                                                        ,'""" + self.st_alias.replace("'", "''") + """'
                                                        ,'""" + self.alias.replace("'", "''") + """'
                                                        ,""" + ifnull(str(self.nm_seq), "NULL") + """
                                                        ,""" + ifnull(str(self.rel_set), "NULL") + """
                                                        ,""" + ifnull(str(self.prior_set), "NULL") + """
                                                        ,'""" + self.mix_yn.replace("'", "''") + """'                                                        
                                                      )"""

        # logging.debug(insert_sql)
        p_cur.execute(insert_sql)
        p_conn.commit()


#정수 확인함수
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

#null 처리함수
def ifnull(var, val):
  if var in (None,'','None'):
    return val
  return var

# 문자 확인 함수
def get_cflag(p_str):
    if p_str == ' ':  # '  '
        cc_cflag = 'blank'
    elif p_str == "'":  # ''
        cc_cflag = 'const'
    elif p_str == "/":  # /* */
        cc_cflag = 'comment'
    # elif p_str == "(":  # (+)
    #     cc_cflag = 'ora_out_sign'
    elif p_str == "-":  # 주석 or 연산자
        cc_cflag = 'minus'
    elif p_str == "\n":  # 주석 or 연산자
        cc_cflag = 'newline'
    elif p_str == "*":  # 연산자 or A.*
        cc_cflag = 'all_col'
    elif p_str == "*":  # 연산자 or A.*
        cc_cflag = 'all_col'
    else:
        cc_cflag = 'other'

    return cc_cflag

#sql list add
def run_sc(p_file_nm,p_sql_id):
    # 1. split_sql & analize sql
    analyze_sql(p_file_nm, p_sql_id, split_sql(p_file_nm, p_sql_id))

    # 2. mapping_sql
    mapping_sql(p_file_nm, p_sql_id)

    # 3. 작업상태 업데이트

    # print(1)



def get_conn(p_db_type):
    conn = ''
    if p_db_type == '':
        p_db_type = 'TIB'

    if p_db_type == 'TIB':
        JDBC_DRIVER = os.environ["JAVA_HOME"] + "\\lib\\tibero5-jdbc.jar"
        JDBC_LIBS = os.environ["JAVA_HOME"] + "\\lib"
        conn = jaydebeapi.connect("com.tmax.tibero.jdbc.TbDriver", "jdbc:tibero:thin:@localhost:7069:DBTBROT",["sys", "tibero"], JDBC_DRIVER, [])
        print(JDBC_DRIVER)

    if p_db_type == 'PGS':

        conn = psycopg2.connect(dbname="postgres", user="postgres", password="", host="localhost", port="5432")

    return conn


def split_sql(p_file_nm,p_sql_id):

    try:
        conn = get_conn('PGS')

        curs = conn.cursor()
        logging.debug(p_file_nm+" "+p_sql_id)
        query = """ SELECT sql_text
                       FROM B2EN_SC_SQL_TEXT
                      WHERE FILE_NM = '"""+p_file_nm+"""'
                        AND SQL_ID  = '"""+p_sql_id+"""'
                     ORDER BY line """
        # query = """ SELECT sql_text
        #                        FROM B2EN_SC_SQL_TEXT
        #                       WHERE FILE_NM = %(str)&
        #                          AND SQL_ID  = %(str)&
        #                      ORDER BY line
        #                      """

        # print(query)

        # curs.prepare(query)

        # print(query)
        curs.execute(query)





        # print(curs.fetchone())

        rows = []
        # rows = curs.fetchall()
        # rows = [item[0] for item in curs.fetchall()]
        for item in curs.fetchall():
            rows.append(item[0])
        # rows = [item[0] ]

        # print(rows)


    except Exception as e:
        print(e)


    # sql = "".join(rows)
    t = []
    # sql이 없는
    for i in rows:
        if i is not None:  # if i == None is also valid but slower and not recommended by PEP8
            # t.append("None")
        # else:
            t.append(i)
    rows = t

    sql =  "\n".join(rows)
    # print("\n".join(filter(None, rows)))
    # print(sql)


#     sql = """SELECT     -- ZhnSql.xml : getJuminInfo
#         'A'     AS FLG
#       , ZHMA_NAME
#       , ZHMA_JUMIN_NO
#     FROM  TBZHMAST TZM
#    WHERE  TZM.ZHMA_MATCH_GB IN('0', '1', '3', '4')
# union all
# SELECT     -- ZhnSql.xml : getJuminInfo
#         'B'     AS FLG
#       , ZHER_NAME
#       , ZHER_JUMIN_NO1||ZHER_JUMIN_NO2 ZHER_JUMIN_NO
#     FROM  TBZHEROR TZM
# union all
# SELECT     -- ZhnSql.xml : getJuminInfo
#         'C'     AS FLG
#       , ZHER_NAME
#       , ZHER_JUMIN_NO1||ZHER_JUMIN_NO2 ZHER_JUMIN_NO
#     FROM  TBZHEROR TZM
# order by FLG,ZHMA_NAME,ZHMA_JUMIN_NO
#    """
#

    logging.debug(sql)
    tmp = ''
    deli = [' ','\n', ',', '(', ')', '!', '<', '>', '=', '*', '/', '-', '|', '+', "'", '?']
    tmp_sql = []
    tmp_list = []
    cc_cflag = ''
    cc_sflag = ''
    cc_eflag = ''
    prv_c = ''

    # split sqlp
    for c in sql:
        # print (c)
        if c in deli:
            if tmp != '':
                tmp_sql.append(tmp)
                tmp = ''

            tmp_sql.append(c)

        else:

            tmp += c


    # 마지막 단어 append
    tmp_sql.append(tmp)

    # 정상
    # print(tmp_sql)

    tmp = ''
    # concat sql
    for c in tmp_sql:

        # 단어 처리 ( 주석, 상수 제외 )
        if len(c) > 1 and cc_sflag not in ('comment', 'comment2','const'):

            # 끝나기전 이전값 할당(아래 동일한 로직 태우기)
            if tmp != '':

                tmp_list.append([tmp, cc_sflag])

            if c[0:1] == ':':
                tmp_list.append([c, 'const'])
            else:
                tmp_list.append([c, 'wrd'])
            tmp = ''
            cc_sflag = ''
            # cc_eflag = 'wrd'

        else:
            #현재값에 대한 정보 할당
            cc_cflag = get_cflag(c)

            #새로운 flag
            if cc_sflag == '':

                cc_sflag = cc_cflag

                tmp += c

                # 위조건에 해당하지 않는것 연산자 , 등은 바로 입력
                if cc_cflag == 'other' and tmp != '':
                    tmp_list.append([tmp, 'normal'])
                    tmp = ''
                    cc_sflag = ''

            else:
                # 값을 할당해야하는 경우 eflag 에 해당 값 할당 마지막에 append
                ## /* 같은 종류의 flag인경우 add 다른 종류가 나오면 list에 append */
                if cc_sflag == 'blank':
                    # black 종료조건 : sflag가 blank 인것중  cflank가 바뀌는 경우
                    if cc_cflag != cc_sflag:
                        cc_eflag = cc_sflag
                    else:
                        tmp += c

                # 'const' 상수 처리
                # 상수의 2번째 char 부터 처리
                elif cc_sflag == 'const' :
                    #상수 종료조건 : sflag가 상수 + c == "'" 인경우
                    if c == "'":
                        cc_eflag = cc_sflag
                    tmp += c

                elif cc_sflag == 'newline':
                    if cc_cflag == cc_sflag:
                        tmp += c
                    else:
                        cc_eflag = cc_sflag
                elif cc_sflag == 'comment' :
                    if prv_c == '*' and c == "/":
                        cc_eflag = cc_sflag
                    tmp += c

                elif cc_sflag == 'minus' and prv_c == '-':
                    cc_cflag = 'comment2'
                    cc_sflag = 'comment2'
                    tmp += c
                elif cc_sflag == 'comment2' :
                    if c == '\n':
                        cc_eflag = cc_sflag
                    tmp += c
                # elif cc_sflag == 'all_col':

                elif cc_sflag == 'other':
                    if cc_cflag == cc_sflag:
                        # tmp += c
                        cc_eflag = 'other'
                    else:
                        cc_eflag = cc_sflag

                elif cc_sflag == 'all_col':
                    if cc_cflag == cc_sflag:
                        tmp += c
                    else:
                        cc_eflag = cc_sflag

                # 종료조건. sql wrd list 에 쓰기
                if cc_eflag != '':
                    if cc_eflag in ("const","comment","comment2"):
                        tmp_list.append([tmp, cc_eflag])
                        tmp = ''
                        cc_sflag = ''
                        cc_eflag = ''
                    else:
                        tmp_list.append([tmp, cc_eflag])
                        tmp = c
                        cc_sflag = cc_cflag
                        cc_eflag = ''

        # 이전값 할당
        prv_c = c

    #마지막 단어 append
    # tmp_list.append([c, ''])

    #float 상수 처리
    tmp_list2 = tmp_list
    i = 0
    for t in tmp_list2:
        if isfloat(t[0]) :
            t[1] = 'const'
        tmp_list[i] = t
        i+=1

    logging.debug(tmp_sql)
    logging.debug(tmp_list)

    return tmp_list


def analyze_sql(p_file_nm,p_sql_id,p_sql_list):
    def init_var():
        v_st_seq = 0
        v_col_end_seq = 0
        v_end_seq = 0
        v_cont = ''
        v_set_lvl = 0
        v_seq = 0
        v_ct_clsf = ''
        v_alias = ''
        v_nm_seq = 0
        return v_st_seq, v_col_end_seq ,v_end_seq ,v_cont ,v_set_lvl ,v_seq ,v_ct_clsf ,v_alias ,v_nm_seq

    if len(p_sql_list) == 0:
        exit

    v_r2_sql_text = []
    v_r_sql_text = []

    m = 0
    i = 0

    v_start_tm = ''
    v_err_msg = ''
    v_step_nm = ''

    set_lvl = 0

    k = 0
    l = 0
    m = 0
    n = 0

    v_cur_val = 0
    v_clause = ''

    v_file_nm = ''
    v_sql_id = ''

    v_targ_job_nm = ''
    v_proc_nm = ''

    v_line = 1
    v_set_lvl = 0
    v_set_seq = 0
    v_select_cnt = 0
    v_bracket_pm = 0
    v_bracket_acm = 0
    v_bracket_stack = 0
    v_bracket_stack_desc = ''
    v_desc1 = ''
    v_desc2 = ''
    v_pr_tab = 0
    v_tab = ''
    v_tab_als = ''
    v_tab_type = ''
    v_rsrv_wrd = ''
    v_type = ''
    v_col_alias_nm = ''
    v_column_nm = ''
    v_clsf = ''
    v_tab_scm = ''
    v_cmnt_yn = ''

    # 괄호 시작점 seq
    v_br_stack = []
    # blank 아닌 이전 항목의 seq 0부터 시작
    v_nb_stack = []

    v_brk_top = 0
    v_nb_top = 0
    v_nb_top_prv = 0
    v_set_seq_max = 0
    v_set_seq_prv = 0
    v_sql_text = ''
    v_sql_text_u = ''


    #     v_r_sql_text = v_i_sql_text

    # try:

    logging.debug("step2-1 analyze sql")
    # logging.debug("analyze sql wrd count : " + str(len(p_sql_list)))
    conn = get_conn("PGS")

    # 데이터가 있는경우
    for c in p_sql_list:

        v_clsf = ''

        # set seq
        #          v_r2_sql_text.append([i,c[0],c[1]])
        if c[1] in ('comment', 'comment2'):
            v_cmnt_yn = 'Y'
        elif c[1] == 'const':
            v_cmnt_yn = 'N'
            v_clsf = 'CONST'
        else:
            v_cmnt_yn = 'N'
        # print(c)
        v_r_sql_text.append(
            DtB2enScSqlWrd(p_file_nm,p_sql_id, i, 'i', c[0], v_cmnt_yn, '', '', '', '', '', '', '', c[1], '', '', '',
                           '', '', '', '', v_clsf, ''))


        v_r_sql_text[i].seq = i

        v_select_cnt = 0
        v_bracket_pm = 0
        v_set_seq_prv = 0
        v_pr_tab = ''

        v_bracket_stack = ''
        v_bracket_stack_desc = ''
        v_desc1 = ''
        v_desc2 = ''
        v_tab = ''
        v_tab_als = ''

        v_col_alias_nm = ''
        v_column_nm = ''
        v_rsrv_wrd = ''

        v_tab_scm = ''
        v_type = ''
        v_sql_text_u = v_r_sql_text[i].sql_text.upper()
        v_sql_text = v_r_sql_text[i].sql_text
        v_cmnt_yn = v_r_sql_text[i].cmnt_yn

        # 주석은 제외하고 처리
        if v_r_sql_text[i].cmnt_yn != 'Y' :
            if len(v_sql_text_u.replace('    ', '').strip()) > 0:

                # select절  설정
                if v_sql_text_u == 'SELECT':

                    v_clause = 'SELECT'

                    v_set_lvl = v_set_lvl + 1
                    v_desc1 = v_desc1 + ' set_lvl+1'

                    v_set_seq_max = v_set_seq_max + 1
                    v_set_seq = v_set_seq_max
                    v_desc1 = v_desc1 + ',set_seq+1'

                    # 최근 괄호정보 가져조회
                    if len(v_br_stack) > 0:
                        # v_brk_top = v_br_stack[0]
                        v_brk_top = v_br_stack[len(v_br_stack) - 1]

                        if v_r_sql_text[v_brk_top].desc2 in ('SELECT','WHERE'):
                            v_r_sql_text[v_brk_top].clsf = 'BR_SUBQ'

                            v_r_sql_text[v_brk_top].select_cnt = v_r_sql_text[v_brk_top].set_lvl
                            v_r_sql_text[v_brk_top].bracket_pm = v_r_sql_text[v_brk_top].set_seq


                        #                            v_tab_type = 'S_SUBQ'
                        else:
                            v_r_sql_text[v_brk_top].clsf = 'BR_INVW'

                            v_r_sql_text[v_brk_top].select_cnt = v_r_sql_text[v_brk_top].set_lvl
                            v_r_sql_text[v_brk_top].bracket_pm = v_r_sql_text[v_brk_top].set_seq


                        v_r_sql_text[v_brk_top].desc1 = '괄호_뷰시작'





                # from절  설정
                elif v_sql_text_u == 'FROM':
                    v_clause = 'FROM'

                # where 절  설정
                elif v_sql_text_u == 'WHERE':
                    v_clause = 'WHERE'
                # order by 절 설정
                elif v_sql_text_u == 'ORDER':
                    v_clause = 'WHERE'
                # group by 절 설정
                elif v_sql_text_u == 'GROUP':
                    v_clause = 'WHERE'
                # insert by 절 설정
                elif v_sql_text_u == 'INSERT':
                    v_clause = 'INSERT'
                # update문 설정
                elif v_sql_text_u == 'UPDATE':
                    v_clause = 'FROM'
                # set 절 설정
                elif v_sql_text_u == 'SET':
                    v_clause = 'WHERE'

                # 예약어 처리, 예약어인경우 type에 예약어 정보 넣기
                if v_r_sql_text[i].clsf != 'CONST':
                    # try:

                    curs = conn.cursor()
                    sql = "select type rsrv_type  from b2en_sc_rsrv_wrd where rsrv_wrd = trim(%s)"

                    # logging.debug(v_sql_text_u)
                    curs.execute(sql,(v_sql_text_u,))

                    for item in curs.fetchall():
                        v_type = item[0]


                        # print(v_type)

                    # except Exception as e:
                    #     print(e)
                    # finally:
                    #     curs.close()
                    #     conn.close()


                # 예약어인 경우 처리
                if v_type != '':
                    # 괄호 처리(view or subquery 시작)
                    if v_sql_text_u == '(':

                        v_br_stack.append(v_r_sql_text[i].seq)

                        #                              v_clsf = '괄호시작'+' : '+v_r_sql_text[i].seq
                        v_desc1 = '괄호시작' + ' : ' + str(v_r_sql_text[i].seq)
                        #                          v_clsf = 'BR_ST'
                        # 이전 clsf 가 컬럼이면 함수로 변경함
                        # v_nb_top = v_nb_stack[0]
                        v_nb_top = v_nb_stack[len(v_nb_stack) - 1]

                        if v_r_sql_text[v_nb_top].clsf == 'COLUMN':
                            v_r_sql_text[v_nb_top].clsf = 'FUNCTION'
                            v_r_sql_text[v_nb_top].column_nm = ''
                            v_clsf = 'BR_FUNCTION'
                            v_r_sql_text[i].clsf = 'BR_FUNCTION'

                        elif v_r_sql_text[v_nb_top].clsf == 'TABLE':

                            v_clsf = 'BR_VALUES'
                            v_clause = 'SELECT'

                        if v_r_sql_text[v_nb_top].clsf == 'FUNCTION':
                            v_r_sql_text[v_nb_top].column_nm = ''
                            v_clsf = 'BR_FUNCTION'
                            v_r_sql_text[i].clsf = 'BR_FUNCTION'

                    # 괄호 종료(view or subquery 종료)
                    elif v_sql_text_u == ')':

                        v_brk_top = v_br_stack[len(v_br_stack) - 1]
                        # 시작괄호가 뷰시작일 경우 set_lvl - 1

                        if v_brk_top > 0:
                            if v_r_sql_text[v_brk_top].desc1 == '괄호_뷰시작':
                                #                                    v_set_lvl = v_set_lvl - 1
                                v_set_seq_prv = v_set_seq
                                #                                    v_set_seq = v_set_lvl

                                # v_set_lvl = v_r_sql_text[v_brk_top].select_cnt
                                v_set_lvl = v_r_sql_text[v_brk_top].set_lvl
                                v_set_seq = v_r_sql_text[v_brk_top].set_seq



                                v_clause = v_r_sql_text[v_brk_top].desc2
                                v_clsf = v_r_sql_text[v_brk_top].clsf
                                v_tab_type = ''

                            if v_r_sql_text[v_brk_top].clsf == 'BR_FUNCTION':
                                v_clsf = 'BR_FUNCTION'
                                v_r_sql_text[i].clsf = 'BR_FUNCTION'

                            v_br_stack.pop()

                        v_desc1 = '괄호종료' + ' : ' + str(v_brk_top)

                    else:
                        v_clsf = v_type

                        if len(v_nb_stack) > 0:
                            v_nb_top = v_nb_stack[len(v_nb_stack)-1]
                            # v_nb_top = v_nb_stack[0]

                        if v_sql_text_u in ('OUTER', 'INNER'):
                            v_r_sql_text[v_nb_top].clsf = 'JOIN'
                            v_clause = 'FROM'

                        if v_sql_text_u in ('ON'):
                            v_clause = 'WHERE'

                        if v_sql_text_u == 'UR':


                            v_r_sql_text[v_nb_top].clsf = 'WITH UR'
                            v_clsf = 'WITH UR'
                        elif (v_sql_text_u == 'FETCH') and (v_r_sql_text[v_nb_top].sql_text == 'FOR'):
                            v_r_sql_text[v_nb_top].clsf = 'FOR FETCH ONLY'
                            v_clsf = 'FOR FETCH ONLY'
                        elif (v_sql_text_u == 'ONLY') and (v_r_sql_text[v_nb_top].clsf == 'FOR FETCH ONLY'):
                            v_clsf = 'FOR FETCH ONLY'
                        elif (v_sql_text_u == 'FIRST') and (v_r_sql_text[v_nb_top].sql_text.upper() == 'FETCH'):
                            v_r_sql_text[v_nb_top].clsf = 'FFNRO'
                            v_clsf = 'FFNRO2'
                        elif ((v_r_sql_text[v_nb_top].clsf == 'CONST') and (v_sql_text_u in ('ROWS','ROW'))) :
                            v_clsf = 'FFNRO4'
                            v_r_sql_text[v_nb_top].clsf ='FFRNO3'
                        elif  v_r_sql_text[v_nb_top].clsf == 'FFNRO4' and v_sql_text_u  == 'ONLY':
                            v_clsf = 'FFNRO5'

                # 예약어가 아닌경우 처리(table,column,function 등등)
                else:

                    # 예약어가 아닌경우
                    # 1. select 절 where 절 처리
                    if (v_clause == 'SELECT') or (v_clause == 'WHERE'):

                        if v_clsf == '':
                            v_clsf = 'COLUMN'

                            if v_sql_text_u.find('.') > -1:
                                v_column_nm = v_sql_text_u[v_sql_text_u.find('.') + 1:]
                                # v_tab_als = v_sql_text_u[0:v_sql_text_u.find('.') - 1]
                                v_tab_als = v_sql_text_u[0:v_sql_text_u.find('.') ]

                            else:
                                v_column_nm = v_sql_text_u

                        if len(v_nb_stack) > 0:
                            # v_nb_top = v_nb_stack[0]
                            v_nb_top = v_nb_stack[len(v_nb_stack) - 1]


                        if (v_r_sql_text[v_nb_top].clsf == 'AS'):

                            v_clsf = 'COL_ALIAS'

                            # 이전 데이터 보기
                            v_nb_top_prv = v_nb_top
                            v_nb_stack.pop()
                            if len(v_nb_stack) > 0:
                                # v_nb_top = v_nb_stack[0]
                                v_nb_top = v_nb_stack[len(v_nb_stack) - 1]
                            v_r_sql_text[v_nb_top].col_alias_nm = v_sql_text_u

                            v_nb_stack.append(v_nb_top_prv)
                        elif (v_r_sql_text[v_nb_top].clsf == 'ROWNUM'):

                            v_clsf = 'COL_ALIAS'
                            # 이전 데이터 보기
                            v_nb_top_prv = v_nb_top
                            v_nb_stack.pop()
                            if len(v_nb_stack) > 0:
                                # v_nb_top = v_nb_stack[0]
                                v_nb_top = v_nb_stack[len(v_nb_stack) - 1]
                            v_r_sql_text[v_nb_top].col_alias_nm = v_column_nm
                            v_nb_stack.append(v_nb_top_prv)


                        elif (v_r_sql_text[v_nb_top].clsf == 'COLUMN') or (v_r_sql_text[v_nb_top].clsf == 'END'):
                            v_clsf = 'COL_ALIAS'
                            v_r_sql_text[v_nb_top].col_alias_nm = v_column_nm

                        elif v_r_sql_text[v_nb_top].sql_text == ')':
                            #  괄호의 특성에 따라 (함수,서브쿼리) 구분필요?
                            v_clsf = 'COL_ALIAS'
                            v_r_sql_text[v_nb_top].col_alias_nm = v_column_nm
                        elif v_r_sql_text[v_nb_top].clsf == 'BR_SUBQ':
                            #  괄호의 특성에 따라 (함수,서브쿼리) 구분필요?
                            v_clsf = 'COL_ALIAS'
                            v_r_sql_text[v_nb_top].col_alias_nm = v_column_nm
                        elif v_r_sql_text[v_nb_top].clsf == 'CONST':
                            #  괄호의 특성에 따라 (함수,서브쿼리) 구분필요?
                            v_clsf = 'COL_ALIAS'
                        elif v_r_sql_text[v_nb_top].clsf == 'HCD':
                            v_clsf = 'COL_ALIAS'


                        if v_cmnt_yn != 'N':
                            v_clsf = v_cmnt_yn

                    elif (v_clause == 'FROM'):

                        v_column_nm = ''
                        # dbms_output.put_line('seq3 : '+i+' , sqltext : '+v_r_sql_text[i].sql_text+' , clsf : '+v_clsf )
                        # 1. 테이블 정의
                        if v_r_sql_text[i].cmnt_yn != 'N':
                            v_clsf = v_r_sql_text[i].cmnt_yn

                        if v_clsf == '':
                            v_clsf = 'TABLE'



                            # view alias 처리
                        if len(v_nb_stack) > 0:
                            # v_nb_top = v_nb_stack[0]
                            v_nb_top = v_nb_stack[len(v_nb_stack) - 1]

                        if v_r_sql_text[v_nb_top].clsf == 'TABLE':
                            v_clsf = 'TAB_ALIAS'
                        elif v_r_sql_text[v_nb_top].clsf == 'BR_INVW':
                            v_clsf = 'VIEW_ALIAS'
                            v_pr_tab = v_r_sql_text[v_nb_top].set_lvl  # set_seq -> set_lvl
                            v_tab_als = v_sql_text_u
                        elif v_r_sql_text[v_nb_top].clsf == 'BR_SUBQ':
                            v_clsf = 'COL_ALIAS'
                            v_tab = v_r_sql_text[v_nb_top].set_seq

                        if v_clsf == 'TABLE':
                            v_tab = v_sql_text_u
                        # v_tab_als  = v_sql_text_u
                        # 1. table schema 확인
                        if v_sql_text_u.find('.') > -1:
                            v_tab = v_sql_text_u[v_sql_text_u.find('.') + 1:]
                            v_tab_scm = v_sql_text_u[0:v_sql_text_u.find('.')]
                            # v_tab_als  = ''

                        v_column_nm = ''


                        # 1. 테이블 정의
                        if v_clsf == '':
                            v_clsf = 'TABLE'



                            # view alias 처리
                        # v_nb_top = v_nb_stack[0]
                        v_nb_top = v_nb_stack[len(v_nb_stack) - 1]

                        if (v_r_sql_text[v_nb_top].clsf == 'TABLE'):
                            v_clsf = 'TAB_ALIAS'

                        if v_clsf == 'TABLE':
                            v_tab = v_sql_text_u
                        # v_tab_als = v_sql_text_u
                        # 1. table schema 확인
                        if v_sql_text_u.find('.') > -1:
                            v_tab = v_sql_text_u[v_sql_text_u.find('.') + 1:]
                            v_tab_scm = v_sql_text_u[0: v_sql_text_u.find('.') ]
                            #                                     v_tab_als  = ''


                            # funcion conversion
                            # 1.

                # 기타 처리

                # tab alias table에 붙이기
                if v_clsf == 'TAB_ALIAS':
                    v_r_sql_text[v_nb_stack[len(v_nb_stack) - 1]].tab_als = v_sql_text_u

                if v_clsf not in ('TABLE', 'VIEW_ALIAS'):
                    v_tab = ''

                # blank 아닌 이전 항목seq
                v_nb_stack.append(i)

            else:
                v_clsf = 'B'

        v_desc2 = v_clause

        if (v_sql_text_u == ')') and (v_clsf in ('BR_INVW', 'BR_SUBQ')):
            v_r_sql_text[i].set_lvl = v_set_lvl
            v_r_sql_text[i].set_seq = v_set_seq
        else:
            v_r_sql_text[i].set_lvl = v_set_lvl
            v_r_sql_text[i].set_seq = v_set_seq

        if v_sql_text_u == '\n':
            v_sql_text = ''
            v_sql_text_U = ''
            v_line += 1

        v_r_sql_text[i].line = v_line
        v_r_sql_text[i].sql_text = v_sql_text
        v_r_sql_text[i].select_cnt = v_select_cnt
        v_r_sql_text[i].bracket_pm = v_bracket_pm
        v_r_sql_text[i].bracket_acm = v_bracket_acm
        v_r_sql_text[i].bracket_stack = v_bracket_stack
        v_r_sql_text[i].bracket_stack_desc = v_bracket_stack_desc
        v_r_sql_text[i].desc1 = v_desc1
        v_r_sql_text[i].desc2 = v_desc2
        v_r_sql_text[i].pr_tab = v_pr_tab
        v_r_sql_text[i].tab = v_tab
        v_r_sql_text[i].tab_als = v_tab_als
        v_r_sql_text[i].tab_type = v_tab_type
        v_r_sql_text[i].col_alias_nm = v_col_alias_nm
        v_r_sql_text[i].column_nm = v_column_nm
        v_r_sql_text[i].clsf = v_clsf
        v_r_sql_text[i].tab_scm = v_tab_scm


        # print(v_r_sql_text[i].seq)
        i += 1


    # except Exception as e:
    #     print(e)


    logging.debug("step2-2 insert analyze sql")
    # insert analyzed data
    conn = get_conn("PGS")

    i = 0

    # if len(v_r_sql_text) ==0:
    #     return

    curs = conn.cursor()
    curs.execute("DELETE FROM B2EN_SC_SQL_WRD  WHERE FILE_NM = '" + v_r_sql_text[i].file_nm + "'  AND SQL_ID = '" + v_r_sql_text[i].sql_id + "'")

    conn.commit()

    curs = conn.cursor()

    v_prc_yn = 'N'

    logging.debug("step2-3 문법처리 추가로직")
    #문법처리 추가로직
    for c in v_r_sql_text:

        #결과 테이블에 insert
        v_r_sql_text[i].insert_db(conn,curs)
        i += 1



    conn.commit()

    analyze_sql_step2(p_file_nm,p_sql_id)


def analyze_sql_step2(p_file_nm,p_sql_id):
    logging.debug("step3-1 qry_str 작업시작")
    v_file_nm = p_file_nm
    v_sql_id  = p_sql_id
    # insert analyzed data
    conn = get_conn("PGS")

    i = 0

    curs = conn.cursor()

    curs.execute(
         "DELETE FROM B2EN_SC_QRY_STR  WHERE FILE_NM = '" + p_file_nm + "'  AND SQL_ID = '" + p_sql_id + "'")


    sql = """        SELECT *                      
                      FROM B2EN_SC_SQL_WRD A 
                    WHERE A.FILE_NM = '"""+p_file_nm+"""'
                      AND A.SQL_ID = '"""+p_sql_id+"""'  
                    ORDER BY A.SEQ """
    logging.debug(sql)
    curs.execute(sql)

    fetchall = curs.fetchall()

    logging.debug(fetchall[0])

    global v_r_sql_text
    global v_ScQrStr
    global v_set_seq_stack
    global v_set_br_stack
    global j_max

    i=0
    for c in fetchall:
        v_r_sql_text.append(DtB2enScSqlWrd(c[0]	,c[1]	,c[2]	,c[3]	,c[4],c[5]	,c[6]	,c[7]	,c[8]	,c[9]	,c[10]	,c[11]	,c[12]	,c[13]	,c[14]	,c[15]	,c[16]	,c[17]	,c[18]	,c[19]	,c[20]	,c[21]	,c[22]))
        i+=1;


    v_end_pos = len(v_r_sql_text)


    # insert analyzed data
    conn = get_conn("PGS")

    i = 0

    curs = conn.cursor()

    curs.execute("DELETE FROM B2EN_SC_QRY_STR  WHERE FILE_NM = '" + v_r_sql_text[i].file_nm + "'  AND SQL_ID = '" + v_r_sql_text[i].sql_id + "'")

    conn.commit()

    # 분석결과를 테이블에 저장

    #global
    # 초기값설정
    v_ScQrStr = []
    # 현재 seq 저장
    v_set_seq_stack = []
    # 괄호시작 저장
    v_set_br_stack = []
    j_max = -1





    curs = conn.cursor()
    v_sql_lines = len(v_r_sql_text)



    def anal_set_str(p_file_nm,p_sql_id,i,j_2,p_end_pos,p_prior_set):


        v_end_pos = p_end_pos
        v_prior_set = p_prior_set
        v_file_nm = p_file_nm
        v_sql_id = p_sql_id

        #global 변수 사용
        global v_r_sql_text
        global v_ScQrStr
        global v_set_seq_stack
        global v_set_br_stack
        global j_max

        v_r_sql_text_len = len(v_r_sql_text)

        v_st_seq = 0
        v_col_end_seq = 0
        v_end_seq = 0
        v_cont = ''
        v_set_lvl = 0
        v_seq = 0
        v_ct_clsf = ''
        v_tab_alias = ''
        v_tab_scm = ''

        v_alias = ''
        v_nm_seq = 0

        cc_cflag = ''
        cc_sflag = ''
        cc_eflag = ''

        v_func = ''
        # v_rel_set = 0

        v_mix_cnt = 0
        v_mix_yn = ''

        v_sql_lines = 0

        if j_2 > 0 :
            j = j_2
        else:
            j = 0 - 1

        i = i


        k = 0
        v_add_qr_str = ''


        while i < v_end_pos:

            if v_r_sql_text[i].cmnt_yn == 'N':
                # print(i)

                # 1. SELECT 절 처리
                # 현재 set 확인
                v_set_lvl = v_r_sql_text[i].set_lvl
                v_set_seq = v_r_sql_text[i].set_seq
                v_sql_text_u = v_r_sql_text[i].sql_text.upper()
                v_sql_text = v_r_sql_text[i].sql_text
                v_desc2 = v_r_sql_text[i].desc2
                v_clsf = v_r_sql_text[i].clsf
                v_tab_alias = v_r_sql_text[i].tab_als
                v_tab_scm   = v_r_sql_text[i].tab_scm

                # set_seq > 0 인경우만 처리
                if v_set_seq > 0:

                    # SELECT 시작점
                    if v_desc2 in ( 'SELECT','WHERE'):
                        # if v_sql_text_u in ('SELECT', ','):



                        # SELECT 시작할 경우 현재 LVL STACK에 추가, 새로운 컬럼 시작
                        if v_sql_text_u == 'SELECT':
                            v_set_seq_stack.append(v_set_seq)
                            cc_sflag = 'COLUMN'
                            v_ct_clsf = 'CL'

                            v_set_seq = v_r_sql_text[i].set_seq
                            v_st_seq = i + 1

                            v_add_qr_str = 'add'
                        elif v_sql_text_u == 'WHERE':
                            cc_sflag = 'COLUMN'
                            v_ct_clsf = 'CL'
                            v_add_qr_str = 'add'

                        # ,가 올경우 현재 컬럼 종료 처리, 새로운 컬럼 시작
                        elif v_sql_text_u == ',' and v_func != 'FUNCTION':
                            if v_mix_cnt > 0:
                                v_ScQrStr[j].mix_yn = 'Y'
                                v_mix_cnt = 0

                            v_ScQrStr[j].end_seq = i - 1
                            v_st_seq = i + 1

                            # 완료처리후 신규 등록
                            v_add_qr_str = 'add'





                        # 컬럼 속성 지정
                        elif cc_sflag == 'COLUMN':

                            if v_r_sql_text[i].clsf == 'B':

                                if v_ScQrStr[j].st_seq == i:
                                    v_ScQrStr[j].st_seq += 1
                            if v_clsf not in ('COLUMN', 'COL_ALIAS', 'B','AS'):
                                v_mix_cnt += 1

                            if v_r_sql_text[i].clsf == 'COLUMN':
                                v_ScQrStr[j].st_alias = v_tab_alias
                                v_ScQrStr[j].ct_nm =  v_r_sql_text[i].column_nm
                                v_ScQrStr[j].ct_seq = v_r_sql_text[i].seq
                                # v_ScQrStr[j].prior_set = v_prior_set


                                    # 컬럼 서브쿼리 시작
                        elif v_clsf == 'BR_SUBQ' and v_sql_text_u == '(':
                            print('start br_subq')

                        # 컬럼과 alias 처리
                        if v_r_sql_text[i].clsf == 'COL_ALIAS':
                            v_ScQrStr[j].alias = v_sql_text_u

                        # 함수처리(함수가 나누어지지 않도록 처리)
                        if v_clsf == 'FUNCTION':
                            v_func = 'FUNCTION'
                            v_ScQrStr[j].mix_yn = 'Y'
                        elif v_clsf == 'BR_FUNCTION' and v_sql_text_u == ')':
                            v_func = ''


                    # 2. FROM 절 처리
                    elif v_desc2 == 'FROM':
                        # select 절 마무리


                        # ,가 올경우 현재 컬럼 종료 처리, 새로운 컬럼 시작
                        if v_sql_text_u == 'FROM':

                            cc_sflag = 'TAB'

                            v_ct_clsf = 'TB'

                            v_ScQrStr[j].end_seq = i - 1
                            v_st_seq = i + 1
                            if v_mix_cnt > 0:
                                v_ScQrStr[j].mix_yn = 'Y'
                                v_mix_cnt = 0

                            # 완료처리후 신규 등록
                            v_add_qr_str = 'add'

                        elif v_sql_text_u == '(':
                            v_sql_text_u = '('

                        # ,가 올경우 현재 컬럼 종료 처리, 새로운 컬럼 시작
                        elif v_sql_text_u == ',':
                            v_ScQrStr[j].end_seq = i - 1
                            v_st_seq = i + 1
                            if v_mix_cnt > 0:
                                v_ScQrStr[j].mix_yn = 'Y'
                                v_mix_cnt = 0

                            v_add_qr_str = 'add'

                        # 컬럼 시작조건 설정
                        if cc_sflag == 'TAB' and v_r_sql_text[i].clsf == 'B':

                            if i == v_st_seq:
                                v_ScQrStr[j].st_seq += 1


                        if v_r_sql_text[i].clsf == 'TABLE':
                            v_ScQrStr[j].st_alias = v_tab_scm
                            v_ScQrStr[j].ct_nm = v_r_sql_text[i].tab
                            v_ScQrStr[j].ct_seq = v_r_sql_text[i].seq

                        # 컬럼과 alias 처리
                        if v_r_sql_text[i].clsf == 'TAB_ALIAS':
                            v_ScQrStr[j].alias = v_sql_text_u
                        elif v_r_sql_text[i].clsf == 'TABLE':
                            v_ScQrStr[j].end_seq = i
                        elif v_r_sql_text[i].clsf == 'VIEW_ALIAS':
                            v_ScQrStr[j].alias = v_r_sql_text[i].tab_als

                    # 인라인뷰 테이블 종료 시퀀스 지정
                    if v_sql_text_u == ')' and v_r_sql_text[i].clsf in ('BR_INVW', 'BR_SUBQ'):
                        v_ScQrStr[v_set_br_stack[len(v_set_br_stack) - 1]].end_seq = i
                        # if v_r_sql_text[i].clsf == 'BR_SUBQ':
                        #     v_ScQrStr[v_set_br_stack[len(v_set_br_stack) - 1]].end_seq

                        # v_ScQrStr[j].end_seq = i
                        v_set_seq = v_r_sql_text[i-1].set_seq

                        return i , j_2, v_sql_text_u,v_set_seq
                        # return i + 1, j_2, v_sql_text_u, v_set_seq



                    # 인라인뷰 처리
                    if v_sql_text_u == '(' and v_r_sql_text[i].clsf in ('BR_INVW','BR_SUBQ'):
                        v_set_br_stack.append(j)
                        logging.debug("( 처리 seq : " + str(i) + " , j_2 : " + str(j))


                        if v_r_sql_text[i].clsf =='BR_SUBQ':
                            v_prior_set = v_r_sql_text[i-1].set_seq

                        i ,j,v_sql_text_u,v_rel_set = anal_set_str(v_file_nm,v_sql_id,i+1,j, v_end_pos,v_prior_set)

                        logging.debug(") 처리 seq : "+str(i)+" , j_2 : "+str(j))
                        if v_r_sql_text_len < i :
                            i = v_r_sql_text_len



                        if i > 0 and  v_r_sql_text[i].clsf == 'BR_INVW':
                            logging.debug("v_ScQrStr[j]: " + str(j))
                            v_ScQrStr[j].rel_set = v_rel_set

                        # v_prior_set = 0

                        v_ScQrStr[j].mix_yn = 'Y'





                    # DtB2enScQrStr 구조 추가
                    if v_add_qr_str == 'add':
                        if v_sql_text_u != 'SELECT':
                            v_ScQrStr[j].prior_set = v_prior_set
                            v_prior_set = 0
                        v_nm_seq = k

                        v_ScQrStr.append(DtB2enScQrStr(v_file_nm, v_sql_id, v_st_seq, v_col_end_seq, v_end_seq, v_cont, v_set_seq,v_ct_clsf,0,'', v_tab_alias,v_alias, v_nm_seq,0,0, v_mix_yn))
                        j_max += 1
                        j = j_max
                        k += 1
                        v_add_qr_str = ''
                        v_mix_yn = ''


            i += 1


        return i,j,v_sql_text_u,v_set_seq


    i,j,v_sql_text_u,v_rel_set = anal_set_str(v_file_nm,v_sql_id,0,0, v_end_pos,0)

    v_ScQrStr[j].end_seq = i - 1

    j = 0

    # cont 내용 추가(100자 미만으로 추가)
    m = 0
    v_cont = ''
    for c in v_ScQrStr:
        # if v_ScQrStr[j].end_seq - v_ScQrStr[j].st_seq >= 0:
        #     for i in range(v_ScQrStr[j].st_seq, v_ScQrStr[j].end_seq + 1):
        #
        #         logging.debug('i : '+str(i))
        #         v_cont += v_r_sql_text[i].sql_text
        #
        # v_ScQrStr[j].cont = v_cont[0:100]

        v_cont = ''
        if v_ScQrStr[j].mix_yn == 'Y':
            v_ScQrStr[j].ct_nm = ''
        v_ScQrStr[j].insert_db(conn, curs)
        j += 1

    conn.commit()


    sql = """        select a.file_nm,a.sql_id,a.set_lvl,case when a.rel_set = '' then '0' else a.rel_set end rel_set,coalesce(prior_set,0)
    					  from (
    					select a.file_nm,a.sql_id,a.set_lvl,ARRAY_TO_STRING(ARRAY_AGG(b.rel_set ORDER BY B.rel_set),',') as rel_set,c.prior_set
    					  from (select distinct file_nm,sql_id,set_lvl
    					  from B2EN_SC_QRY_STR  
    					 where file_nm = '"""+v_file_nm+"""' 
    					   and sql_id = '"""+v_sql_id+"""'
    					 ) a left outer join (select distinct file_nm,sql_id,set_lvl,rel_set
					    					    from B2EN_SC_QRY_STR  
					    					   where file_nm = '"""+v_file_nm+"""' 
					    					     and sql_id = '"""+v_sql_id+"""'
					    					     and rel_set > 0) b on a.file_nm= b.file_nm and a.sql_id= b.sql_id and a.set_lvl = b.set_lvl
					    	 left outer join (select distinct file_nm,sql_id,set_lvl,prior_set
											    from b2en_sc_qry_str
											   where prior_set > 0) c on a.file_nm= c.file_nm and a.sql_id= c.sql_id and a.set_lvl = c.set_lvl
    					group by a.file_nm,a.sql_id,a.set_lvl,c.prior_set
    					) a
    					order by a.set_lvl desc

             """

    logging.debug(sql)
    curs.execute(sql)

    fetchall = curs.fetchall()

    logging.debug(fetchall[0])
    i = 0

    sql = """delete from b2en_sc_qry_col_src where file_nm = '"""+v_file_nm+"""' and sql_id = '"""+v_sql_id+"""' """
    curs.execute(sql)

    for c in fetchall:

        sql = """ insert into b2en_sc_qry_col_src
            --컬럼추출   (tab alias 있는 경우 해당 집합에서 정확하게 추출 가능. tab alias 가 있지만 쿼리에 해당 tab 이 없는경우?(고려하지 않음 -정상적이지않은 sql))
            select a.file_nm,a.sql_id
                  ,a.set_seq
                  ,a.seq
                  ,a.desc2
                  ,case when b.ct_nm = '' then c.src_tab else b.ct_nm end src_tab 
                  ,case when b.ct_nm = '' then c.src_col else a.column_nm end src_col      
                  ,case when a.col_alias_nm ='' then a.column_nm else a.col_alias_nm end col_alias
                  ,1 set_ord
                  ,null mix_yn
              from B2EN_SC_SQL_WRD a left outer join  B2EN_SC_QRY_STR b on a.file_nm = b.file_nm and a.sql_id = b.sql_id and b.set_lvl in ("""+str(c[4])+""" , a.set_seq )  and a.tab_als = b.alias and b.ct_clsf = 'TB'
                                    left outer join (select distinct a.file_nm, a.sql_id,col_alias,alias,b.src_tab,b.src_col
                                                      from B2EN_SC_QRY_STR a  left outer join b2en_sc_qry_col_src b on a.file_nm = b.file_nm and a.sql_id = b.sql_id and a.rel_set in ("""+str(c[4])+""" , b.set_lvl)
                                                     where a.file_nm = '"""+v_file_nm+"""'
                                                       and a.sql_id = '"""+v_sql_id+"""'
                                                       and a.set_lvl = """+str(c[2])+"""
                                                       and ct_clsf  = 'TB'
                                                       and a.mix_yn = 'Y' ) c on a.file_nm = b.file_nm and a.sql_id = b.sql_id and b.ct_nm = '' and a.column_nm = c.col_alias and  a.tab_als = c.alias 
             where a.file_nm = '"""+v_file_nm+"""' 
               and a.sql_id = '"""+v_sql_id+"""'
               and a.set_seq = """+str(c[2])+"""
               and a.clsf = 'COLUMN'
               and tab_als <> ''   
            union all   
               --컬럼추출   (tab alias 지정 없는 경우 해당 집합의 전체 테이블 대상으로 컬럼 맵핑)  
            select a.file_nm,a.sql_id
                  ,a.set_seq
                  ,a.seq
                  ,a.desc2
                  ,d.ct_nm src_tab 
                  ,a.column_nm src_col
                  ,case when a.col_alias_nm ='' then a.column_nm else a.col_alias_nm end col_alias
                  ,case when d.set_lvl = a.set_seq then 1 
                        when d.set_lvl < a.set_seq then 2
                        else 3 end set_ord
                  ,d.mix_yn
              from B2EN_SC_SQL_WRD a left outer join ( --같은 레벨에 존재하는 테이블의 컬럼 매핑
                                                       select  b.file_nm, b.sql_id, b.set_lvl, b.ct_clsf,c.asis_col,c.asis_col alias,b.ct_nm,b.mix_yn
                                                       from B2EN_SC_QRY_STR b left outer join b2en_sc_col_map c on b.ct_nm = c.asis_tab
                                                      where b.file_nm = '"""+v_file_nm+"""'
                                                       and b.sql_id = '"""+v_sql_id+"""'
                                                       and b.set_lvl in ( """+str(c[4])+""" ,"""+str(c[2])+""" )                                                       
                                                     union 
                                                     -- 관계테이블의 경우 해당 집합이 col, tab으로 명확하게 나와있음.
                                                     select a.file_nm,a.sql_id,a.set_lvl,'TB',case when a.mix_yn = 'Y' then alias else a.ct_nm end ct_nm,case when a.alias= '' then a.ct_nm else a.alias end  alias,b.src_tab  ,case when b.mix_yn= 'Y' then 'Y'  when ct_nm<>case when a.alias= '' then a.ct_nm else a.alias end then 'Y' else a.mix_yn end mix_yn        
                                                       from  B2EN_SC_QRY_STR a left outer join b2en_sc_qry_col_src b on a.file_nm = b.file_nm and a.sql_id = b.sql_id AND a.set_lvl = b.set_lvl and case when a.alias= '' then a.ct_nm else a.alias end = b.col_alias and b.claus = 'SELECT'  and a.mix_yn= ''
                                                       where a.file_nm = '"""+v_file_nm+"""' 
                                                       and a.sql_id = '"""+v_sql_id+"""'                                                      
                                                       and a.set_lvl in ("""+str(c[3])+""") --rel_set                                                     
                                                    ) d on a.file_nm = d.file_nm and a.sql_id = d.sql_id and  d.ct_clsf = 'TB' and a.column_nm = d.alias 
             where a.file_nm = '"""+v_file_nm+"""'
               and a.sql_id = '"""+v_sql_id+"""'
               and a.set_seq = """+str(c[2])+"""
               and a.clsf = 'COLUMN'
               and tab_als = ''
            """

        logging.debug(sql)
        curs.execute(sql)


        i += 1;

    conn.commit()

    sql = """delete from b2en_sc_SQL_WRD_RST where file_nm = '""" + v_file_nm + """' and sql_id = '""" + v_sql_id + """' """
    curs.execute(sql)

    # 매핑결과 Insert
    sql = """INSERT into b2en_sc_sql_wrd_rst  (FILE_NM,SQL_ID,LINE,SEQ,SQL_TEXT,SQL_TEXT_RST)
            select FILE_NM,SQL_ID,LINE,SEQ,SQL_TEXT
                  ,case when CLSF = 'COLUMN' then TOBE_COL2
                        when CLSF = 'TABLE' then TOBE_TAB2
                        when CLSF = 'FUNCTION' then TOBE_FNC
                        else SQL_TEXT end SQL_TEXT_RST
              from (
            select a.file_nm,a.sql_id,a.line,a.seq,a.sql_text,A.CLSF                 
                  ,b.tobe_col
                  ,case when position('.'in a.sql_text) > 0 and A.CLSF = 'COLUMN' then split_part(a.sql_text,'.',1)||'.'||b.tobe_col
                        when b.mix_yn = 'Y' then a.sql_text
                        else b.tobe_col end TOBE_COL2
                  ,B.tobe_TAB
                  ,case when position('.'in a.sql_text) > 0 and A.CLSF = 'TABLE' then split_part(a.sql_text,'.',1)||'.'||C.tobe_TAB2
                        else C.tobe_TAB2 end tobe_TAB2
                  ,coalesce(d.TOBE_FNC,a.sql_text) TOBE_FNC
              from b2en_sc_sql_wrd a left outer join (select file_nm,sql_id,seq,src_tab,src_col,b.tobe_tab,coalesce(b.tobe_col,'/* SC - '||src_col||' : No Mapping Info*/') tobe_col,mix_yn
                                                            ,row_number() over(partition by file_nm,sql_id,seq order by set_ord) set_ord      
                                                        from b2en_sc_qry_col_src a left outer join b2en_sc_col_map b on a.src_tab = b.asis_tab and a.src_col = b.asis_col
                                                     ) b on a.file_nm = b.file_nm and a.sql_id = b.sql_id and a.seq = b.seq and a.clsf = 'COLUMN' and b.set_ord = 1
                                    left outer join (select   ASIS_TAB
                                                             ,TOBE_TAB[1] tobe_tab
                                                             ,case when DUP_CNT > 1 then TOBE_TAB[1]||' '||DUP_CMMT
                                                                   else TOBE_TAB[1] end tobe_tab2
                                                             ,DUP_CNT
                                                             ,DUP_YN
                                                             ,DUP_CMMT
                                                          from (
                                                        select  B.ASIS_TAB
                                                               ,ARRAY_AGG(b.TOBE_TAB ORDER BY B.COL_CNT DESC) as TOBE_TAB 
                                                               ,COUNT(*) DUP_CNT
                                                               ,CASE WHEN COUNT(*) > 1 THEN 'Y' ELSE 'N' END DUP_YN
                                                               ,'/* SC 테이블 중복확인 : '|| ARRAY_TO_STRING(ARRAY_AGG(b.TOBE_TAB ORDER BY B.COL_CNT DESC ),',')||' */' DUP_CMMT
                                                          from b2en_sc_tab_map  b
                                                         group by B.asis_tab											 
                                                         ) c ) c on a.tab = c.asis_tab and a.clsf = 'TABLE'
                                     left outer join B2EN_SC_FNC_MAP d ON  A.CLSF = 'FUNCTION' AND upper(A.SQL_TEXT) = D.ASIS_FNC AND D.CNV_YN = 'Y'
             where a.file_nm = '"""+v_file_nm+"""'
               and a.sql_id = '"""+v_sql_id+"""'
             order by 1,2,3,4
            )  A"""

    logging.debug(sql)
    curs.execute(sql)

    conn.commit()

    # mapping_sql(v_file_nm, v_sql_id)







    #함수 로직
    return 0

def mapping_sql(p_file_nm,p_sql_id):
    conn = get_conn("PGS")

    curs = conn.cursor()




    #4. 최종 결과 처리

    # curs.execute("""  DELETE FROM B2EN_SC_SQL_WRD_RST A WHERE A.FILE_NM = '"""+p_file_nm+"""'  AND A.SQL_ID = '"""+p_sql_id+"""' """)
    curs.execute("""  DELETE FROM B2EN_SC_SQL_TEXT_RST A WHERE A.FILE_NM = '""" + p_file_nm + """'  AND A.SQL_ID = '""" + p_sql_id + """' """)
    # sql = """  INSERT INTO B2EN_SC_SQL_WRD_RST
    sql = """        SELECT distinct A.FILE_NM
                          ,A.SQL_ID
                          ,A.LINE
                          ,A.SEQ
                          ,A.SQL_TEXT
                          ,CASE A.CLSF  WHEN 'COLUMN' THEN COALESCE(A.TAB_ALS||case when A.TAB_ALS != '' then '.' else '' end ||COALESCE(B.TOBE_COL ,COLUMN_NM||'/* SC : NO COL MAP INFO */'),A.SQL_TEXT)
                                        WHEN 'TABLE' THEN COALESCE(C.TOBE_TAB || CASE WHEN C.DUP_CNT > 1 THEN C.DUP_CMMT END ,A.TAB||' /* SC : NO TAB MAP INFO */')
                                        WHEN 'FUNCTION' THEN COALESCE(D.TOBE_FNC,A.SQL_TEXT)
                                        ELSE A.SQL_TEXT
                                        END SQL_TEXT_RST  
                          ,A.CMNT_YN
                          ,A.SET_LVL
                          ,A.SET_SEQ
                          ,A.SELECT_CNT
                          ,A.BRACKET_PM
                          ,A.BRACKET_ACM
                          ,A.BRACKET_STACK
                          ,A.BRACKET_STACK_DESC
                          ,A.DESC1
                          ,A.DESC2
                          ,A.PR_TAB
                          ,A.TAB
                          ,A.TAB_ALS
                          ,A.TAB_TYPE
                          ,A.COL_ALIAS_NM
                          ,A.COLUMN_NM
                          ,A.CLSF
                          ,A.TAB_SCM                      
                      FROM B2EN_SC_SQL_WRD A LEFT OUTER JOIN  B2EN_SC_COL_MAP_LOW_RST  B
                                                          ON  A.FILE_NM = B.FILE_NM
                                                          AND A.SQL_ID = B.SQL_ID
                                                          AND A.SEQ = B.SEQ
                                                          AND B.ORD = 1
                                             LEFT OUTER JOIN B2EN_SC_TAB_MAP_RST C
                                                          ON  A.FILE_NM = C.FILE_NM
                                                          AND A.SQL_ID = C.SQL_ID
                                                          AND A.SEQ = C.SEQ
                                             LEFT OUTER JOIN B2EN_SC_FNC_MAP D
                                                          ON  A.CLSF = 'FUNCTION'
                                                          AND A.SQL_TEXT = D.ASIS_FNC    
                                                          AND D.CNV_YN = 'Y'
                    WHERE A.FILE_NM = '"""+p_file_nm+"""'
                      AND A.SQL_ID = '"""+p_sql_id+"""'  
                    ORDER BY A.SEQ """

    sql = """select a.file_nm,a.sql_id,a.line,a.seq,a.sql_text,b.sql_text_rst,a.cmnt_yn,a.set_lvl,a.set_seq,a.select_cnt,a.bracket_pm,a.bracket_acm,a.bracket_stack,a.bracket_stack_desc,a.desc1,a.desc2,a.pr_tab,a.tab,a.tab_als,a.tab_type,a.col_alias_nm,a.column_nm,a.clsf,a.tab_scm,a.set_blk
             from B2EN_SC_SQL_WRD a ,B2EN_SC_SQL_WRD_RST b 
            WHERE a.file_nm = b.file_nm 
              and a.sql_id = b.sql_id 
              and a.seq = b.seq 
              and A.FILE_NM = '"""+p_file_nm+"""'
              AND A.SQL_ID = '"""+p_sql_id+"""' 
              order by seq"""

    logging.debug(sql)
    curs.execute(sql)

    fetchall = curs.fetchall()


    v_cur_rst = []
    v_cur_text_rst = []
    v_sql_text_rst = ''
    i=0

    for c in fetchall:
        v_cur_rst.append(DtB2enScSqlWrdRst(c[0]	,c[1]	,c[2]	,c[3]	,c[4],c[5]	,c[6]	,c[7]	,c[8]	,c[9]	,c[10]	,c[11]	,c[12]	,c[13]	,c[14]	,c[15]	,c[16]	,c[17]	,c[18]	,c[19]	,c[20]	,c[21]	,c[22],c[23]))
        # v_cur_rst[i].insert_db(conn, curs)
        i+=1



    # conn.commit()

    # DB2 문법처리(FETCH FIRST n ROSW ONLY 등)
    # 추가작업 db2 문법 변환
    v_oprt_stack = []


    j = 0
    i = 0

    if len(v_cur_rst) > 0:

        for c in v_cur_rst:

            # 매핑후 처리 fetch first n rows only 처리 , with ur 제거
            # 이전 operation 저장 stack에
            if v_cur_rst[i].clsf in ('AND', 'WHERE', 'ORDER', 'BY', 'GROUP', 'FROM', 'BR_INVW', 'VIEW_ALIAS', ''):
                v_oprt_stack.append(i)

            if v_cur_rst[i].clsf in ('FFNRO','FFNRO2','FFNRO4','FFNRO5'):
                v_cur_rst[i].sql_text_rst = ''

            if v_cur_rst[i].clsf == 'FFRNO3':

                # 1. 변환가능성 찾기
                v_oprt_pos = v_oprt_stack[len(v_oprt_stack) - 1]

                if v_cur_rst[v_oprt_pos].clsf in ('FROM', 'WHERE', 'AND', 'VIEW_ALIAS', 'BR_INVW', ''):

                    # 2. 상수 찾기
                    # v_ffnro_num = regexp_substr(v_cur_rst[i].sql_text, '[0-9]+', 1, 1, 'i')
                    m = int(v_cur_rst[i].sql_text)
                    # m = re.search('[0-9]+', v_cur_rst[i].sql_text)
                    # v_ffnro_num = m.group(0)
                    v_ffnro_num = m

                    if v_cur_rst[v_oprt_pos].clsf in ('FROM', 'BR_INVW', 'VIEW_ALIAS', ''):
                        v_cur_rst[i].sql_text_rst = 'WHERE ROWNUM <= ' + str(v_ffnro_num)

                    elif v_cur_rst[v_oprt_pos].clsf == 'WHERE':
                        v_cur_rst[i].sql_text_rst = 'AND ROWNUM <= ' + str(v_ffnro_num)
                    elif v_cur_rst[v_oprt_pos].clsf == 'AND':
                        v_cur_rst[i].sql_text_rst = 'AND ROWNUM <= ' + str(v_ffnro_num)




            elif v_cur_rst[i].clsf == 'HCD':

                v_cur_rst[i].sql_text_rst = 'TO_DATE(SYSDATE,''YYYYMMDD'')'

            elif (v_cur_rst[i].clsf == 'FUNCTION') and (v_cur_rst[i].sql_text == 'HEX') and ( 'LLOG' in v_cur_rst[i].col_alias_nm  ):
                # llog가
                v_cur_rst[i].sql_text_rst = ''

            elif v_cur_rst[i].clsf == 'WITH UR':
                v_cur_rst[i].sql_text_rst = ''

            v_line = v_cur_rst[i].line

            if (i > 0) and (v_cur_rst[i].line != v_cur_rst[i - 1].line):
                v_cur_text_rst.append(DtB2enScSqlTextRst(v_cur_rst[i].file_nm,v_cur_rst[i].sql_id,v_cur_rst[i-1].line,v_sql_text_rst,''))
                v_cur_text_rst[j].insert_db(conn, curs)

                # v_cur_text_rst[j].file_nm = v_file_nm
                # v_cur_text_rst[j].sql_id = v_sql_id
                # v_cur_text_rst[j].line = v_line
                # v_cur_text_rst[j].sql_text = v_sql_text_rst
                v_sql_text_rst = ''

                j = j + 1

            # sql_text 조합
            v_sql_text_rst = v_sql_text_rst + ifnull(v_cur_rst[i].sql_text_rst,"")
            i += 1

    v_cur_text_rst.append(DtB2enScSqlTextRst(v_cur_rst[i-1].file_nm, v_cur_rst[i-1].sql_id, v_cur_rst[i - 2].line, v_sql_text_rst, ''))
    v_cur_text_rst[j].insert_db(conn, curs)


    #작업상태 완료 업데이트


    update_sql = """update b2en_sc_sql_list set wk_stat_cd = 'C'
                   where file_nm = '"""+p_file_nm+"""' and sql_id = '"""+p_sql_id+"""'"""

    # print(ifnull(str(self.pr_tab) ,"NULL"))
    logging.debug(update_sql)
    curs.execute(update_sql)
    conn.commit()







# main process

# analyze_sql('w_insa_1_tong' ,'d_insa_1_tong3',split_sql('w_insa_1_tong' ,'d_insa_1_tong3'))
#run_sc('ZhnSql.xml' ,'getJuminInfo')

# mapping_sql('w_insa_1_tong' ,'d_insa_1_tong3')



