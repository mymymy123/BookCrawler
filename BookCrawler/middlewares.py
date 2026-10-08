# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import logging
import aiohttp
import requests

class ProxytunnelMiddleware(object):
    def __init__(self, proxytunnel_url):
        self.logger = logging.getLogger(__name__)
        self.proxytunnel_url = proxytunnel_url
    
    def process_request(self, request, spider):

        if request.meta.get('retry_times') and 1 <= request.meta.get('retry_times') <= 10:
            self.logger.debug('Using proxytunnel')
            request.meta['proxy'] = self.proxytunnel_url
    
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxytunnel_url=settings.get('PROXYTUNNEL_URL')
        )

class ProxypoolMiddleware(object):
    def __init__(self,proxypool_url):
        self.proxypool_url=proxypool_url
        self.loggger=logging.getLogger(__name__)
        
    @classmethod
    def from_crawler(cls,crawler):
        return cls(proxypool_url=crawler.settings.get('PROXYPOOL_URL'))

    def get_random_proxy(self):
        try:
            response=requests.get(self.proxypool_url,timeout=5)
            if response.status_code==200:
                proxy=response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self,request,spider):
        if request.meta.get('retry_times') and request.meta.get('retry_times')>10:
            proxy=self.get_random_proxy()
            self.loggger.debug('get proxy %s',proxy)
            if proxy:
                proxy_url=f'http://{proxy}'
                self.loggger.debug('using proxy %s',proxy_url)
                request.meta['proxy']=proxy_url




