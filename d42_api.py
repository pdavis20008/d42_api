import urllib3
import requests
import base64
from pprint import pprint
from getpass import getpass
import sys
urllib3.disable_warnings()


class d42_api:
    def __init__(self,ipaddress,urluser,urlpass):
        self.ipaddress = ipaddress
        self.urluser = urluser
        self.urlpassword = urlpass
        self.base_url = f"https://{ipaddress}/api/"
        self.headers = {"Authorization": f"Basic {str(base64.b64encode(bytes(urluser+':'+urlpass,encoding='utf-8')),encoding='utf-8')}"}


    def get(self,url_path,params=None):
        req = requests.get(f'{self.base_url}{url_path}',verify=False,headers=self.headers,params=params)
        return req

    def post(self,url_path,params=None,data=None):
        req = requests.post(f'{self.base_url}{url_path}',verify=False,headers=self.headers,params=params,data=data)
        return req

    def update(self,url_path,params=None,data=None):
        req = requests.put(f'{self.base_url}{url_path}',verify=False,headers=self.headers,params=params,data=data)
        return req.status_code

    def delete(self,url_path):
        req = requests.delete(f'{self.base_url}{url_path}',verify=False,headers=self.headers)
        return req.status_code

    ## Working with IP Addresses ##
    def findIp(self,ipaddress):
        results = self.get(url_path='1.0/search/',params=f"query=ip&string={ipaddress}")
        return results.json()['ips']

    def assignIp(self,ipaddress,label):
        data = {
            "ipaddress": ipaddress,
            "available": "no",
            "label": label,
            "mac_address":"",
            "device":"",
            "type":"static"
        }
        results = self.post(url_path='1.0/ips/',data=data)
        if results.status_code == 200:
            return f"{ipaddress}/{label}: Configured successfully"
        else:
            return f"{ipaddress}/{label}: Something went wrong. Error {results.status_code}"

    def unassignIp(self,ipaddress,type):
        data = {
            "ipaddress": ipaddress,
            "available": "yes",
            "label": "",
            "mac_address":"",
            "device":"",
            "type":type
        }
        results = self.post(url_path='1.0/ips/',data=data)
        if results.status_code == 200:
            return f'{ipaddress} now set to available'
        else:
            return f'{ipaddress}: Something went wrong. Error {results.status_code}'

    ## Working with Devices ##
    def findDevice(self,devname):
        results = self.get(url_path=f'1.0/devices/name/{devname}')
        return results.json()

    def deleteDevice(self,devid):
        result = self.delete(url_path=f'1.0/devices/{devid}/')
        if result == 200:
            return f"{devid}: Successfully deleted"
        else:
            return f"{devid}: Something went wrong. Error {result}"

    ## General Deployment information/health ##
    def listAutoDiscovery(self,type='pingsweep'):
        results = self.get(f'1.0/auto_discovery/{type}')
        return results.json()['jobs']

    def getHealthStats(self):
        results = requests.get(f'https://{self.ipaddress}:4343/healthstats/',verify=False)
        return results.json()
