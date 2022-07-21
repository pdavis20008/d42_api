import urllib3
import requests
import base64
urllib3.disable_warnings()


class d42_api:
    def __init__(self,ipaddress,urluser,urlpass):
        self.ipaddress = ipaddress
        self.urluser = urluser
        self.urlpassword = urlpass
        self.base_url = f"https://{ipaddress}/api/1.0/"
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

    def findIp(self,ipaddress):
        results = self.get(url_path='search/',params=f"query=ip&string={ipaddress}")
        return results.json()['ips']

    def assignIp(self,ipaddres):
        return 'Method not complete'

    def listAutoDiscovery(self,type='pingsweep'):
        req = self.get(f'auto_discovery/{type}')
        return req.json()['jobs']

    def getHealthStats(self):
        results = requests.get(f'https://{self.ipaddress}:4343/healthstats/',verify=False)
        return results.json()
