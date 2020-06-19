
import psycopg2
import json
from psycopg2 import sql
import os
import socket
from pathlib import Path
import sys
from time import sleep


#keep the dbdata json file in home folder instead of site package
current_path =Path.home()
sys_name = socket.gethostname()
sys_platform = sys.platform


def create_db_file():
    d_list = ['dbname','user','host','password','ApplicationName']
    jobj = None

    if sys_platform == 'linux':
        config_file_path = 'dbdata.json'
    else:
        config_file_path = os.path.join(current_path,'dbdata.json')
 
    if os.path.exists(config_file_path):
        with open(config_file_path,'r',encoding='utf-8') as f:
            jobj = json.load(f)
            all_keys = jobj.keys()
            for element in d_list:
                if not element in all_keys:
                    jobj[element] = input(f'enter value for {element} :')

        #put the new data in config file
        with open(config_file_path,'w',encoding='utf-8') as fp:
            json.dump(jobj,fp)
        return jobj
    else:
        #if file does not exists
        jobj = dict()
        all_keys = jobj.keys()
        for element in d_list:
            if not element in all_keys:
                jobj[element] = input(f'enter value for {element} :')
        with open(config_file_path,'w',encoding='utf-8') as fp:       
            json.dump(jobj,fp)
        return jobj

create_db_file()


def return_db_conn(ApplicationName = "gscrap"):
    
    dbname=None
    user=None
    host=None
    password=None

    if sys_platform == 'linux':
        config_file_path = 'dbdata.json'
    else:
        config_file_path = os.path.join(current_path,'dbdata.json')

    for _ in range(5):
        try:
            with open(config_file_path,'r') as f:
                db_data = json.load(f)
                dbname=db_data['dbname']
                user=db_data['user']
                host=db_data['host']
                password=db_data['password']
                break
        except:
            print('error reading db file')
            sleep(4)

            pass

    
    #logging.debug("Creating new connection")
    conn = None
    conn = psycopg2.connect(f"dbname={dbname} user={user} host={host} password={password} application_name={ApplicationName} connect_timeout=10 options='-c statement_timeout=5s'")
    return conn


def return_multiple_links_curl(cur,tablename):
    #cur.execute("select pg_sleep(6)") testing sleep
    cur.execute('select * from public.return_ihs_data()')
    rows = cur.fetchall()
    
    rows_returned = len(rows)

    if rows_returned == 0:
        return  []
    rlink_list = list()
    for rwdata in rows:
        tlink = rwdata[0]
        rlink_list.append(tlink)



    return rlink_list
    

def update_link_tbl(cur,update_link,begin_time,end_time,status,tablename,sthree_link):
    update_tuple = (status,begin_time,end_time,sys_name,sthree_link,update_link)
    sql = """Update {} set t_status = %s ,begintime = %s , endtime = %s,sysname=%s ,awsurl=%s where t_link = %s""".format(tablename)
    cur.execute(sql,update_tuple)


if __name__ == "__main__":
    #print(scandb(tablename='tbl_misc_links'))
    #create_return_table()
    #copy_file_to(current_path +'\dbdata.json')
    conn = return_db_conn()
    cur = conn.cursor()
    ts = return_multiple_links_curl(cur=cur,tablename='uchecker')
    print(ts)
    conn.commit()
    cur.close()
    conn.close()
