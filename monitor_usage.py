#!/usr/bin/python                                                                                                  
# coding:utf-8                                                                                                     
                                                                                                                   
from jinja2 import Environment, FileSystemLoader                                                                   
import Adafruit_ADS1x15                                                                                            
from time import strftime                                                                                          
import cgitb                                                                                                       
#import pandas as pd                                                                                               
import csv                                                                                                         
from datetime import datetime                                                                                      
#from ftplib import FTP
from paramiko import SSHClient, AutoAddPolicy
                                                                                                                   
# raspberry pi--------------------------------------                                                               
CHANNEL = 0 # setting gor the channel pair to detect                                                               
GAIN = 8 # setting for the voltage range to detect                                                                 
                                                                                                                   
adc = Adafruit_ADS1x15.ADS1015()                                                                                   
                                                                                                                   
voltage = adc.read_adc_difference(CHANNEL, gain=GAIN)                                                              
log = []                                                                                                           
if abs(voltage) > 200:                                                                                             
    using = True
    log.append(voltage)                                                         
    log.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))                                                         
    with open('usage_history.csv', 'a') as f1:                                                                        
        writer = csv.writer(f1)                                                                                         
        writer.writerows([log])                                                                                          
else:                                                                                                              
    using = False

# register to csv-----------------------------------                                                               
usage_history = []
with open('usage_history.csv', 'r') as f:
    reader = csv.reader(f)
    #header = next(reader)  # ヘッダーを読み飛ばしたい時                                                       
    for row in reader:
        usage_history.append(row)
        #print row          # 1行づつ取得できる                                                                    
# below lines is the way using panda                             
#df = pd.read_csv('usage_history.csv')
#data_used = pd.DataFrame([[ voltage, datetime.now().strftime('%Y/%m/%d %H:%M:%S') ]])
#data_used.tocsv('usage_history.csv', index=False, encoding="utf-8", mode='a', header=False)
#print df       # show all column
#print df['A']  # show 'A' column
 
# rendering-----------------------------------------                                                               
env = Environment(loader=FileSystemLoader('./', encoding='utf8'))                                                  
tpl = env.get_template('monitor_usage.tpl.html')                                                                   
html = tpl.render({'using':using, 'voltage':voltage, 'history': usage_history })                                   
print "Content-Type: text/html\r\n"                                                                                
print html.encode('utf-8')                                                                                         
if True:
#    ftp = FTP(
#        "192.168.1.227",
#        "centos",
#        passwd="linuxpass"
#    )
    with SSHClient() as ssh:
        ssh.set_missing_host_key_policy(AutoAddPolicy())
	ssh.connect(hostname='192.168.100.91', port=22, username='user', password='password')
	sftp = ssh.open_sftp()
	sftp.put('./usage_history.csv', '/Users/user-mbp/Documents/usage_history.csv')
	sftp.close()
	ssh.close()
#    ftp = FTP(
#        host="192.168.100.91",
#        user="user",
#        passwd="password",
#        timeout=10
#    )
#    with open('usage_history.csv', "rb") as f2:
#        ftp.storlines("STOR /Users/user-mbp/Documents/usage_history.csv", f2)
#    ftp.quit()
cgitb.enable()
