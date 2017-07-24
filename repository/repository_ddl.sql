CREATE TABLE public.b2en_sc_col_alias (
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	column_nm varchar(100) NULL,
	set_lvl int4 NULL,
	set_seq float8 NULL,
	clsf varchar(50) NULL
)
WITH (
	OIDS=FALSE
) ;

CREATE INDEX b2en_sc_col_alias_pk ON public.b2en_sc_col_alias (file_nm DESC,sql_id DESC,column_nm DESC,set_lvl DESC,set_seq DESC) ;

CREATE TABLE public.b2en_sc_col_map (
	asis_tab varchar(100) NULL,
	asis_col varchar(100) NULL,
	tobe_tab varchar(100) NULL,
	tobe_col varchar(200) NULL,
	rgs_dttm timestamp NULL,
	asis_logical_tab varchar(100) NULL,
	asis_logical_col varchar(100) NULL,
	tobe_logical_tab varchar(100) NULL,
	tobe_logical_col varchar(100) NULL
)
WITH (
	OIDS=FALSE
) ;
CREATE UNIQUE INDEX b2en_sc_col_map_pk ON public.b2en_sc_col_map (asis_tab DESC,asis_col DESC,tobe_tab DESC,tobe_col DESC) ;

CREATE TABLE public.b2en_sc_col_map_low_rst (
	seq int4 NULL,
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	set_lvl int4 NULL,
	set_seq int4 NULL,
	asis_tab varchar(4000) NULL,
	asis_col varchar(50) NULL,
	tobe_tab varchar(4000) NULL,
	tobe_col varchar(4000) NULL,
	ord float8 NULL,
	tab_alias varchar(50) NULL,
	col_alias_nm varchar(50) NULL,
	tab_type varchar(10) NULL,
	subq_yn varchar(1) NULL,
	ord1 float8 NULL,
	ord2 float8 NULL,
	ord3 float8 NULL
)
WITH (
	OIDS=FALSE
) ;
CREATE INDEX ix01_b2en_sc_col_map_low_rst ON public.b2en_sc_col_map_low_rst (file_nm DESC,sql_id DESC,seq DESC) ;

CREATE TABLE public.b2en_sc_col_map_rst (
	seq int4 NULL,
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	set_lvl int4 NULL,
	set_seq int4 NULL,
	asis_tab varchar(4000) NULL,
	asis_col varchar(50) NULL,
	tobe_col varchar(4000) NULL,
	col_alias_nm varchar(50) NULL,
	tab_type varchar(10) NULL,
	subq_yn varchar(1) NULL
)
WITH (
	OIDS=FALSE
) ;

CREATE TABLE public.b2en_sc_col_map_test (
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	set_lvl int4 NULL,
	src_tab varchar(200) NULL,
	src_col varchar(200) NULL,
	col_alias varchar NULL
)
WITH (
	OIDS=FALSE
) ;

CREATE TABLE public.b2en_sc_fnc_map (
	asis_fnc varchar(100) NULL,
	tobe_fnc varchar(100) NULL,
	cnv_yn varchar(1) NULL
)
WITH (
	OIDS=FALSE
) ;

CREATE TABLE public.b2en_sc_func_cnv (
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	seq int4 NULL,
	fn_nm varchar(100) NULL,
	clsf varchar(100) NULL,
	clsf_seq int4 NULL,
	src_seq int4 NULL,
	desc1 varchar(200) NULL
)
WITH (
	OIDS=FALSE
) ;
CREATE UNIQUE INDEX b2en_sc_func_cnv_pk ON public.b2en_sc_func_cnv (file_nm DESC,sql_id DESC,seq DESC) ;

CREATE TABLE public.b2en_sc_func_cnv_arg (
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	seq int4 NULL,
	fn_nm varchar(100) NULL,
	clsf varchar(50) NULL,
	clsf_seq int4 NULL,
	min_seq int4 NULL,
	max_seq int4 NULL
)
WITH (
	OIDS=FALSE
) ;
CREATE UNIQUE INDEX b2en_sc_func_cnv_arg_pk ON public.b2en_sc_func_cnv_arg (fn_nm DESC,sql_id DESC,seq DESC) ;

CREATE TABLE public.b2en_sc_job_log (
	job_log_seq int8 NOT NULL,
	job_dt varchar(8) NULL,
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	step_nm varchar(300) NULL,
	start_tm timestamp NULL,
	end_tm timestamp NULL,
	err_msg varchar(4000) NULL,
	CONSTRAINT b2en_sc_job_log_pk PRIMARY KEY (job_log_seq)
)
WITH (
	OIDS=FALSE
) ;

CREATE TABLE public.b2en_sc_qry_col_src (
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	set_lvl int4 NULL,
	seq int4 NULL,
	claus varchar(100) NULL,
	src_tab varchar(200) NULL,
	src_col varchar(200) NULL,
	col_alias varchar NULL,
	set_ord int4 NULL,
	mix_yn varchar(1) NULL
)
WITH (
	OIDS=FALSE
) ;

CREATE TABLE public.b2en_sc_qry_str (
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	st_seq int4 NULL,
	col_end_seq int4 NULL,
	end_seq int4 NULL,
	cont varchar(200) NULL,
	set_lvl int4 NULL,
	ct_clsf varchar(2) NULL,
	ct_seq int4 NULL,
	st_alias varchar(100) NULL,
	ct_nm varchar(200) NULL,
	alias varchar(100) NULL,
	nm_seq int4 NULL,
	rel_set int4 NULL,
	prior_set int4 NULL,
	mix_yn varchar(1) NULL
)
WITH (
	OIDS=FALSE
) ;

CREATE TABLE public.b2en_sc_rsrv_wrd (
	rsrv_wrd varchar(100) NOT NULL,
	"type" varchar(50) NULL,
	CONSTRAINT all_d_tun_con799500274 PRIMARY KEY (rsrv_wrd)
)
WITH (
	OIDS=FALSE
) ;
CREATE UNIQUE INDEX b2en_sc_rsrv_wrd_pk ON public.b2en_sc_rsrv_wrd (rsrv_wrd DESC) ;

CREATE TABLE public.b2en_sc_sql_list (
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	job_cl varchar(100) NULL,
	qry_cl varchar(100) NULL,
	wk_stat_cd varchar(1) NULL,
	rgs_dttm timestamp NULL
)
WITH (
	OIDS=FALSE
) ;
CREATE UNIQUE INDEX pk_b2en_sc_sql_list ON public.b2en_sc_sql_list (file_nm DESC,sql_id DESC) ;

CREATE TABLE public.b2en_sc_sql_text (
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	line int4 NULL,
	sql_text varchar(3000) NULL,
	job_cl varchar(4) NULL
)
WITH (
	OIDS=FALSE
) ;
CREATE UNIQUE INDEX b2en_sc_sql_text_pk ON public.b2en_sc_sql_text (file_nm DESC,sql_id DESC,line DESC) ;

CREATE TABLE public.b2en_sc_sql_text_cv (
	sql_id varchar(100) NULL,
	line int4 NULL,
	sql_text varchar(3000) NULL
)
WITH (
	OIDS=FALSE
) ;

CREATE TABLE public.b2en_sc_sql_text_rst (
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	line int4 NULL,
	sql_text varchar(3000) NULL,
	job_cl varchar(4) NULL
)
WITH (
	OIDS=FALSE
) ;

CREATE TABLE public.b2en_sc_sql_text_rst_bak (
	reg_dt varchar(8) NULL,
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	line int4 NULL,
	sql_text varchar(3000) NULL,
	job_cl varchar(4) NULL
)
WITH (
	OIDS=FALSE
) ;
CREATE INDEX b2en_sc_sql_text_rst_bak_pk ON public.b2en_sc_sql_text_rst_bak (reg_dt DESC,sql_id DESC,sql_text DESC,line DESC) ;

CREATE TABLE public.b2en_sc_sql_wrd (
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	line int4 NULL,
	seq int4 NULL,
	sql_text varchar(1500) NULL,
	cmnt_yn varchar(10) NULL,
	set_lvl int4 NULL,
	set_seq int4 NULL,
	select_cnt int4 NULL,
	bracket_pm int4 NULL,
	bracket_acm int4 NULL,
	bracket_stack int4 NULL,
	bracket_stack_desc varchar(200) NULL,
	desc1 varchar(200) NULL,
	desc2 varchar(200) NULL,
	pr_tab int4 NULL,
	tab varchar(50) NULL,
	tab_als varchar(50) NULL,
	tab_type varchar(10) NULL,
	col_alias_nm varchar(50) NULL,
	column_nm varchar(100) NULL,
	clsf varchar(50) NULL,
	tab_scm varchar(50) NULL,
	set_blk int4 NULL
)
WITH (
	OIDS=FALSE
) ;
CREATE UNIQUE INDEX b2en_sc_sql_wrd_pk ON public.b2en_sc_sql_wrd (file_nm DESC,sql_id DESC,seq DESC) ;

CREATE TABLE public.b2en_sc_sql_wrd_org (
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	line int4 NULL,
	seq int4 NULL,
	sql_text varchar(1500) NULL,
	cmnt_yn varchar(10) NULL,
	set_lvl int4 NULL,
	set_seq int4 NULL,
	select_cnt int4 NULL,
	bracket_pm int4 NULL,
	bracket_acm int4 NULL,
	bracket_stack int4 NULL,
	bracket_stack_desc varchar(200) NULL,
	desc1 varchar(200) NULL,
	desc2 varchar(200) NULL,
	pr_tab int4 NULL,
	tab varchar(50) NULL,
	tab_als varchar(50) NULL,
	tab_type varchar(10) NULL,
	col_alias_nm varchar(50) NULL,
	column_nm varchar(100) NULL,
	clsf varchar(50) NULL,
	tab_scm varchar(50) NULL
)
WITH (
	OIDS=FALSE
) ;

CREATE TABLE public.b2en_sc_sql_wrd_rst (
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	line int4 NULL,
	seq int4 NULL,
	sql_text varchar(1500) NULL,
	sql_text_rst varchar(1500) NULL,
	cmnt_yn varchar(10) NULL,
	set_lvl int4 NULL,
	set_seq int4 NULL,
	select_cnt int4 NULL,
	bracket_pm int4 NULL,
	bracket_acm int4 NULL,
	bracket_stack int4 NULL,
	bracket_stack_desc varchar(200) NULL,
	desc1 varchar(200) NULL,
	desc2 varchar(200) NULL,
	pr_tab int4 NULL,
	tab varchar(50) NULL,
	tab_als varchar(50) NULL,
	tab_type varchar(10) NULL,
	col_alias_nm varchar(50) NULL,
	column_nm varchar(100) NULL,
	clsf varchar(50) NULL,
	tab_scm varchar(50) NULL,
	set_blk int4 NULL
)
WITH (
	OIDS=FALSE
) ;
CREATE UNIQUE INDEX b2en_sc_sql_wrd_rst_pk ON public.b2en_sc_sql_wrd_rst (file_nm DESC,sql_id DESC,seq DESC) ;

CREATE TABLE public.b2en_sc_sql_wrd_rst_org (
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	line int4 NULL,
	seq int4 NULL,
	sql_text varchar(1500) NULL,
	sql_text_rst varchar(1500) NULL,
	cmnt_yn varchar(10) NULL,
	set_lvl int4 NULL,
	set_seq int4 NULL,
	select_cnt int4 NULL,
	bracket_pm int4 NULL,
	bracket_acm int4 NULL,
	bracket_stack int4 NULL,
	bracket_stack_desc varchar(200) NULL,
	desc1 varchar(200) NULL,
	desc2 varchar(200) NULL,
	pr_tab int4 NULL,
	tab varchar(50) NULL,
	tab_als varchar(50) NULL,
	tab_type varchar(10) NULL,
	col_alias_nm varchar(50) NULL,
	column_nm varchar(100) NULL,
	clsf varchar(50) NULL,
	tab_scm varchar(50) NULL
)
WITH (
	OIDS=FALSE
) ;

CREATE TABLE public.b2en_sc_tab (
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	set_lvl int4 NULL,
	set_seq int4 NULL,
	tab_scm varchar(100) NULL,
	tab varchar(100) NULL,
	tab_als varchar(100) NULL,
	view_alias varchar(100) NULL,
	clsf varchar(100) NULL,
	tab_type varchar(10) NULL
)
WITH (
	OIDS=FALSE
) ;
CREATE UNIQUE INDEX b2en_sc_tab_pk ON public.b2en_sc_tab (file_nm DESC,sql_id DESC,set_lvl DESC,set_seq DESC,tab DESC,tab_als DESC,view_alias DESC,clsf DESC,tab_type DESC) ;

CREATE TABLE public.b2en_sc_tab_map (
	asis_tab varchar(100) NULL,
	tobe_tab varchar(100) NULL,
	col_cnt int4 NULL,
	rgs_dttm timestamp NULL,
	asis_logical_tab varchar(100) NULL,
	tobe_logical_tab varchar(100) NULL
)
WITH (
	OIDS=FALSE
) ;
CREATE UNIQUE INDEX b2en_sc_tab_map_pk ON public.b2en_sc_tab_map (asis_tab DESC,tobe_tab DESC) ;

CREATE TABLE public.b2en_sc_tab_map_rst (
	seq int4 NULL,
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	asis_tab varchar(100) NULL,
	tobe_tab varchar(100) NULL,
	dup_cnt int4 NULL,
	dup_yn varchar(1) NULL,
	dup_cmmt varchar(1000) NULL,
	asis_tab_schm varchar(100) NULL,
	tobe_tab_schm varchar(100) NULL
)
WITH (
	OIDS=FALSE
) ;

CREATE TABLE public.b2en_sc_text_bak (
	reg_dt varchar(8) NULL,
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	line int4 NULL,
	asis_sql varchar(3000) NULL,
	conv_sql varchar(3000) NULL
)
WITH (
	OIDS=FALSE
) ;
CREATE INDEX b2en_sc_text_bak_pk ON public.b2en_sc_text_bak (reg_dt DESC,file_nm DESC,sql_id DESC,line DESC) ;

CREATE TABLE public.b2en_sc_view (
	file_nm varchar(100) NULL,
	sql_id varchar(100) NULL,
	set_lvl int4 NULL,
	set_seq int4 NULL,
	tab_scm varchar(100) NULL,
	tab varchar(100) NULL,
	tab_als varchar(100) NULL
)
WITH (
	OIDS=FALSE
) ;
