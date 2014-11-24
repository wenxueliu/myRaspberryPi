#!/bin/env python
# -*- coding:utf-8 -*-
# Comment: in order to make it boot you must user rc.local instead of
# /etc/rc.local of your raspberrry
# -------------------------------

import os
import time
import socket
import fcntl
import struct
import smtplib
from email.mime.text import MIMEText

mail_host = 'smtp.163.com'
mail_user = '[MYUSER]@163.com'
mail_pwd = '[MYPASSWORD]'
mail_to = '[MYUSER]@163.com'

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
         )[20:24])
    except IOError, e:
        return e

def mail_send(content, mailto, get_sub):
    msg = MIMEText(content.encode('utf8'), _subtype='html',  _charset='utf8')
    msg['From'] = mail_user
    msg['Subject'] = u'%s' % get_sub
    msg['To'] = mailto
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pwd)
        s.sendmail(mail_user,[mailto],msg.as_string())
        s.close()
        send = "OK"
    except Exception ,e:
        send = "ERROR! %s" % e
    return send

def main():
    _count_loop = 0
    while 1:
        ip_list = []
        if _count_loop == 0:
	    pass
            os.system('sudo wpa_supplicant -B -Dwext -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf')
            time.sleep(1)
            os.system('sudo dhclient wlan0')
        try:
            ip_list.append(get_ip_address('eth0'))
        except:
            pass
        try:
            ip_list.append(get_ip_address('wlan0'))
        except Except,e:
            pass
        _get_send_status =  mail_send('my pi ip', mail_to, '%s' % ip_list)
        _count_loop +=1
        if (_get_send_status == "OK") or (_count_loop == 3):
            break
        time.sleep(3)

if __name__ == "__main__":
    main()
