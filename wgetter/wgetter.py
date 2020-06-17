from subprocess import DEVNULL, STDOUT, check_call,Popen
import os
from time import sleep
from urllib.parse import urlparse
import threading
from ndb import return_multiple_links_curl,return_db_conn,update_link_tbl
from datetime import datetime
import re

import zipfile
import shutil

from supload.supload import upload_file


#https://stackoverflow.com/a/1855118/3025905
from string import punctuation

def send_to_zip(input_file):
    
    uobj  = urlparse(input_file)
    input_file = uobj.netloc

    try:
        shutil.make_archive(input_file, 'zip', input_file)
    except FileNotFoundError:
        return None,None,False

    return input_file+'.zip',input_file,True
    



def link_verifier(url):
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None


def print_new(print_statemnt):
    ctime = datetime.utcnow()
    print(f'{ctime}:{print_statemnt}')


def download_with_wget(url):
    f_wget_string = f'wget -NmkEpnp -e robots=off {url}'
    Popen(f_wget_string,shell=True,stdout=DEVNULL, stderr=STDOUT)


def get_current_folder_size(folder_name):
    total_size = 0
    for root, dirs,files in os.walk(folder_name):
        for f in files:
            fp = os.path.join(root,f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size



def is_downloading(folder_name):
    should_keep_going = True
    while should_keep_going:
        size_diff = 0

        old_size = get_current_folder_size(folder_name)
        sleep(10)
        

        for _ in range(10):
            #wait for file to start download
            new_size = get_current_folder_size(folder_name)
            if new_size == 0:
                sleep(30)
            else:
                break


            

        size_diff = new_size - old_size

        


        if old_size != new_size:
            return True
        else:
            return False


import sys
def download_and_wait_wget(url):
    uobj  = urlparse(url)
    net_location = uobj.netloc

    download_with_wget(url)
    
    curr_status  = is_downloading(net_location)

    state_counter = 0
    
    while True:
        sleep(10)
        curr_status  = is_downloading(net_location)
        
        if curr_status == False:
            state_counter += 1
        else:
            state_counter = 0

        if state_counter >= 10:
            break
        print_new(f'is downloading : {curr_status}, {url}, {state_counter}')



def process_wget(link,cur,conn):
    valid_link = link_verifier(link)
    begin_time  = datetime.utcnow()
    
    if not valid_link:
        end_time  = datetime.utcnow()
        update_link_tbl(cur=cur,update_link=link,begin_time=begin_time,end_time=end_time,status='INVALIDURL',tablename='tbl_misc_links_ihs_energy')
        conn.commit()
        return
    try:
        download_and_wait_wget(link)
        end_time  = datetime.utcnow()

        zip_file,local_folder,success_stat = send_to_zip(link)

        if success_stat:
            upload_file(file_name=zip_file,in_sub_folder='kapowautostorerhoaiindia/wget_d',bucket_name='rhoaiautomationindias3')
            sleep(3)
            os.remove(zip_file)
            shutil.rmtree(local_folder)
            update_link_tbl(cur=cur,update_link=link,begin_time=begin_time,end_time=end_time,status='COMPLETE',tablename='tbl_misc_links_ihs_energy')
            conn.commit()
        else:
            update_link_tbl(cur=cur,update_link=link,begin_time=begin_time,end_time=end_time,status='ERROR',tablename='tbl_misc_links_ihs_energy')
            conn.commit()
            upload_file(file_name=zip_file,in_sub_folder='kapowautostorerhoaiindia/wget_d',bucket_name='rhoaiautomationindias3')
            

    except Exception as e:
        raise e
        end_time  = datetime.utcnow()
        update_link_tbl(cur=cur,update_link=link,begin_time=begin_time,end_time=end_time,status='ERROR',tablename='tbl_misc_links_ihs_energy')
        conn.commit()            







def downloader():

    while True:
        conn = return_db_conn()
        cur = conn.cursor()
        all_data = return_multiple_links_curl(cur=cur,tablename='tbl_misc_links_ihs_energy')
        conn.commit()

        if len(all_data) == 0:
            sys.exit(0)

        
        for link in all_data:
            print_new(link)
            process_wget(link,cur,conn)

        
        cur.close()
        conn.close()



def threaded_wget():
    num_thread = int(input('enter max number of thread'))
    threads= list()

    for _ in range(num_thread):
        gs = threading.Thread(target=downloader)
        threads.append(gs)
        gs.daemon = True
        gs.start()


    for thread in threads:
        thread.join()

    while True:
        sleep(10)
        print_new('running')

if __name__ == "__main__":
    threaded_wget()
    # downloader()
    # conn = return_db_conn()
    # cur = conn.cursor()

    # process_wget('http://www.example.com',cur,conn)

    # cur.close()
    # conn.close()
    