from subprocess import DEVNULL, STDOUT, check_call,Popen
import os
from time import sleep
from urllib.parse import urlparse
import threading
from ndb import return_multiple_links_curl,return_db_conn,update_link_tbl
from datetime import datetime
import re


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
        for _ in range(10):
            old_size = get_current_folder_size(folder_name)
            sleep(10)
            new_size = get_current_folder_size(folder_name)

            #set the size if same then increase the counter
            #else reset the counter

            if old_size != new_size:
                size_diff = new_size - old_size
                print_new(f'folder : {folder_name}, old size : {old_size} , new size {new_size}, difference {size_diff}')
                return True
            else:
                print_new(f'folder : {folder_name}, old size : {old_size} , new size {new_size}, difference {size_diff}')
    return False


import sys
def download_and_wait_wget(url):
    uobj  = urlparse(url)
    net_location = uobj.netloc

    download_with_wget(url)
    curr_status  = is_downloading(net_location)


    state_counter = 0
    """ download the file and wait to know if website is downloaded or now

    """

    while True:
        sleep(30)
        curr_status  = is_downloading(net_location)
        if curr_status == False:
            state_counter += 1
        else:
            state_counter = 0

        if state_counter >= 10:
            break


def downloader():

    while True:
        conn = return_db_conn()
        cur = conn.cursor()
        all_data = return_multiple_links_curl(cur=cur,tablename='tbl_misc_links_ihs_energy')
        for link in all_data:
            print_new(link)
            valid_link = link_verifier(link)

            if not valid_link:
                update_link_tbl(cur=cur,update_link=link,begin_time=begin_time,end_time=end_time,status='INVALIDURL',tablename='tbl_misc_links_ihs_energy')
                continue

            begin_time  = datetime.utcnow()
            try:
                download_and_wait_wget(link)
                end_time  = datetime.utcnow()
                update_link_tbl(cur=cur,update_link=link,begin_time=begin_time,end_time=end_time,status='ERROR',tablename='tbl_misc_links_ihs_energy')
                conn.commit()

            except Exception:
                end_time  = datetime.utcnow()
                update_link_tbl(cur=cur,update_link=link,begin_time=begin_time,end_time=end_time,status='COMPLETE',tablename='tbl_misc_links_ihs_energy')
                conn.commit()



            

        input('done')
        cur.close()
        conn.close()



def threaded_wget():

    threads= list()

    for _ in range(10):
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
    # print(link_verifier('https://www.gogle.com'))
