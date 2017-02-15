#!/usr/bin/python
#coding:utf-8

# this is add line

import os
import json
import psutil
import urllib
import urllib2
from subprocess import Popen, PIPE


class Server:
    def __init__(self, url='', res_data={}):
        self.res_data = res_data
        self.url = url

    def __getHostname(self):
        try:
            p = Popen('hostname', stdout=PIPE)
            hostname = p.communicate()[0].strip()
            return hostname
        except:
            return 'None'

    def __getAddress(self, mode):
        addresslist = {}
        # maclist = {}
        ipdata = psutil.net_if_addrs()
        for ip in ipdata.keys():
            if ip != 'lo':
                if mode == 'ip':
                    try:
                        addresslist[ip] = ipdata[ip][0].address
                    except:
                        addresslist[ip] = 'None'
                elif mode == 'mac':
                    try:
                        addresslist[ip] = ipdata[ip][2].address
                    except:
                        addresslist[ip] = 'None'

        return addresslist

    def __getSys(self):
        system = os.popen('uname -o').read()
        kernel = os.popen('uname -r').read().strip()
        return system,kernel

    def __getCpu(self):
        cpuname = os.popen('grep  "model name" /proc/cpuinfo | head -1 | cut -d: -f2').read().strip()
        cpunum = psutil.cpu_count()
        return cpuname, cpunum

    def __getMem(self):
        mem = psutil.virtual_memory().total/1000/1000
        if mem > 1024:
            memtotal = str(mem/1000)+"G"
        else:
            memtotal = str(mem)+"M"
        return memtotal

    def __getSwap(self):
        swap = psutil.swap_memory().total/1000/1000
        if swap > 1024:
            swaptotal = str(swap/1000) + "G"
        elif swap > 0:
            swaptotal = str(swap) + "M"
        else:
            swaptotal = '0'
        return swaptotal

    def run(self):
        self.res_data['hostname'] = self.__getHostname()
        self.res_data['showname'] = self.__getHostname()
        self.res_data['ipaddress'] = self.__getAddress('ip')
        self.res_data['macaddress'] = self.__getAddress('mac')
        self.res_data['system'], self.res_data['kernel'] = self.__getSys()
        self.res_data['cpuname'], self.res_data['cpunum'] = self.__getCpu()
        self.res_data['memory'] = self.__getMem()
        self.res_data['swap'] = self.__getSwap()

        return self.res_data

    def send_data(self):
        server_url = self.url
        header = {
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2739.0 Safari/537.36'
        }
        data = self.run()
        sdata = urllib.urlencode(data)
        req = urllib2.Request(url=server_url, headers=header, data=sdata)
        res = urllib2.urlopen(req)
        
        return res.read()


if __name__ == '__main__':
    url = "http://192.168.223.1:8000/api/serverbasicinfo/"
    s = Server(url=url)
    #result = s.send_data()
    result = s.run()
    header = { 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2739.0 Safari/537.36' }
    #data = json.dumps(result)
    data = urllib.urlencode(result)
    req = urllib2.Request(url=url, headers=header, data=data)
    res = urllib2.urlopen(req)
    print(res.read())
    
    print(data)




