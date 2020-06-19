from subprocess import DEVNULL, STDOUT, check_call,Popen
import subprocess
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





def send_to_zip(input_file):
 
    uobj  = urlparse(input_file)
    input_file = uobj.netloc

    try:
        shutil.make_archive(input_file, 'zip', input_file)
    except FileNotFoundError as e:
        try:
            shutil.rmtree(input_file)
        except Exception:
            print(f'could not remove {input_file}')
        return None,None,False

    try:
        shutil.rmtree(input_file)
    except Exception:
        print(f'could not remove {input_file}')

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
    # f_wget_string = f'wget -NmkEpnp -e robots=off {url}'
    # f_wget_string = """wget -NmkEpnp -e robots=off -A .asp,.aspx,.axd,.asx,.asmx,.ashx,.html,.htm,.xhtml,.jhtml,.jsp,.jspx,.wss,.do,.action,.js,.php,.php4,.php3,.phtml,.rss,.cgi,.asp,.axd,.asx,.asmx,.ashx,.aspx,.net,.js,.html,.htm,.xhtml,.cgi,.aspx,.ascx,.asmx,.erb,.rjs,.hta,.htc,.htmls,.rhtml,.pdf,.ASP,.ASPX,.AXD,.ASX,.ASMX,.ASHX,.HTML,    .HTM,.XHTML,.JHTML,.JSP,.JSPX,.WSS,.DO,.ACTION,.JS,.PHP,.PHP4,.PHP3,.PHTML,.RSS,.CGI,.ASP,.AXD,.ASX,.ASMX,.ASHX,.ASPX,.NET,.JS,.HTML,.HTM,.XHTML,.CGI,.ASPX,.ASCX,.ASMX,.ERB,.RJS,.HTA,.HTC,.HTMLS,.RHTML,.PDF {0}""".format(url)
    # Popen(f_wget_string,shell=True,stdout=DEVNULL, stderr=STDOUT)
    
    f_wget_string = ['wget', '-NmkEpnp', '-A', '.asp,.aspx,.axd,.asx,.asmx,.ashx,.html,.htm,.xhtml,.jhtml,.jsp,.jspx,.wss,.do,.action,.js,.php,.php4,.php3,.phtml,.rss,.cgi,.asp,.axd,.asx,.asmx,.ashx,.aspx,.net,.js,.html,.htm,.xhtml,.cgi,.aspx,.ascx,.asmx,.erb,.rjs,.hta,.htc,.htmls,.rhtml,.pdf,.ASP,.ASPX,.AXD,.ASX,.ASMX,.ASHX,.HTML,.HTM,.XHTML,.JHTML,.JSP,.JSPX,.WSS,.DO,.ACTION,.JS,.PHP,.PHP4,.PHP3,.PHTML,.RSS,.CGI,.ASP,.AXD,.ASX,.ASMX,.ASHX,.ASPX,.NET,.JS,.HTML,.HTM,.XHTML,.CGI,.ASPX,.ASCX,.ASMX,.ERB,.RJS,.HTA,.HTC,.HTMLS,.RHTML,.PDF','-e','robots=off',url]
    process = subprocess.Popen(f_wget_string,stdout=DEVNULL,stderr=DEVNULL)
    print_new(process.args)
    return process

def download_wget_full_web(url):
    f_wget_string = ['wget', '-NmkEpnp', '-R','.mp3','.mp4','.jpg','.jpeg','.gif' ,'-e','robots=off',url]
    process = subprocess.Popen(f_wget_string,stdout=DEVNULL,stderr=DEVNULL)
    print_new(process.args)
    return process




def get_current_folder_size(folder_name):
    total_size = 0
    for root, dirs,files in os.walk(folder_name):
        for f in files:
            fp = os.path.join(root,f)
            if not os.path.islink(fp):
                try:
                    total_size += os.path.getsize(fp)
                except FileNotFoundError:
                    pass
    return total_size



def is_downloading(folder_name):
    should_keep_going = True
    while should_keep_going:
        size_diff = 0
        new_size = 0
        old_size = get_current_folder_size(folder_name)
        sleep(10)


        for _ in range(5):
            #wait for file to start download
            new_size = get_current_folder_size(folder_name)
            size_in_mb= int(new_size / (1024 * 1024))
            
            if size_in_mb >500:
                raise ValueError('maximum size rached for website')

            if new_size == 0:
                return False
            else:
                break

        size_diff = new_size - old_size


        if old_size != new_size:
            return True
        else:
            return False


import sys
def download_and_wait_wget_full(url):

    print('secondary downloader fired')
    uobj  = urlparse(url)
    net_location = uobj.netloc

    proc = download_wget_full_web(url)


    state_counter = 0

    while True:
        sleep(10)

        try:
            curr_status  = is_downloading(net_location)
        except ValueError as ve:
            proc.terminate()
            shutil.rmtree(net_location)
            raise ve
            break

        if curr_status == False:
            state_counter += 1
        else:
            state_counter = 0


        if state_counter >= 5:
            f_size = get_current_folder_size(net_location)
            size_in_mb = int(f_size / (124.0*1024.0))
            return size_in_mb
            break            
        
        print_new(f'is downloading retry : {curr_status}, {url}, {state_counter}')




def download_and_wait_wget(url):
    uobj  = urlparse(url)
    net_location = uobj.netloc

    proc = download_with_wget(url)
    

    state_counter = 0

    while True:
        sleep(10)

        try:
            curr_status  = is_downloading(net_location)
        except ValueError as ve:        
            proc.terminate()
            shutil.rmtree(net_location)
            raise ve
            break


        if curr_status == False:
            state_counter += 1
        else:
            state_counter = 0


        if state_counter >= 5:
            f_size = get_current_folder_size(net_location)
            size_in_mb = int(f_size / (124.0*1024.0))
            return size_in_mb
            break           
        
        print_new(f'is downloading base: {curr_status}, {url}, {state_counter}')



def process_wget(link,cur,conn):
    valid_link = link_verifier(link)
    begin_time  = datetime.utcnow()
    success_stat = None
    if not valid_link:
        end_time  = datetime.utcnow()
        update_link_tbl(cur=cur,update_link=link,begin_time=begin_time,end_time=end_time,
                        status='INVALIDURL',tablename='tbl_misc_links_ihs_energy',sthree_link='INVALIDURL')
        conn.commit()
        return

    f_size = 0
    
    try:
        f_size = download_and_wait_wget(link)
    except ValueError:
        end_time  = datetime.utcnow()
        update_link_tbl(cur=cur,update_link=link,begin_time=begin_time,end_time=end_time,
                        status='MAXSIZE',tablename='tbl_misc_links_ihs_energy',sthree_link='ERROR')
        conn.commit()
        return
    
    if f_size <= 10:
        try:
            print_new('less than 10 , retrying with full')
            f_size = download_and_wait_wget_full(link)
        except ValueError:
            end_time  = datetime.utcnow()
            update_link_tbl(cur=cur,update_link=link,begin_time=begin_time,end_time=end_time,
                            status='MAXSIZE',tablename='tbl_misc_links_ihs_energy',sthree_link='ERROR')
            conn.commit()
            return

    


    end_time  = datetime.utcnow()
    zip_file,local_folder,success_stat = send_to_zip(link)
    end_time  = datetime.utcnow()


    if success_stat:
        correct_upload,s3_uploaded_link = upload_file(file_name=zip_file,in_sub_folder='kapowautostorerhoaiindia/wget_d',bucket_name='rhoaiautomationindias3')

        update_link_tbl(cur=cur,update_link=link,begin_time=begin_time,end_time=end_time,
        status='COMPLETE',tablename='tbl_misc_links_ihs_energy',sthree_link=s3_uploaded_link)
        conn.commit()
        os.remove(zip_file)
    else:
        update_link_tbl(cur=cur,update_link=link,begin_time=begin_time,end_time=end_time,
                        status='ERROR',tablename='tbl_misc_links_ihs_energy',sthree_link='ERROR')
        conn.commit()
        #upload_file(file_name=zip_file,in_sub_folder='kapowautostorerhoaiindia/wget_d',bucket_name='rhoaiautomationindias3')









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
    num_thread = int(input('enter max number of thread: '))
    threads= list()

    for _ in range(num_thread):
        gs = threading.Thread(target=downloader)
        threads.append(gs)
        gs.daemon = True
        gs.start()


    dead_thread_count = 0
    while True:
        #keep the main threadr running for ctr+c
        dead_threads =  num_thread - (threading.active_count() - 1 ) # -1 to exclude main thread
        print(f'total thread:{threading.active_count()} , dead thread: {dead_threads}')
        sleep(10)

if __name__ == "__main__":
    # threaded_wget()
    # downloader()
    conn = return_db_conn()
    cur = conn.cursor()

    # process_wget('https://www.grupoenergiabogota.com',cur,conn)
    
    # process_wget('https://www.isa.com.co',cur,conn)
    process_wget('https://www.example.com',cur,conn)
    cur.close()
    conn.close()
    # download_with_wget('http://www.example.com')
