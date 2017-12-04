# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 16:27:30 2017

@author: perus
"""
from browsermobproxy import Server
from selenium import webdriver
import json


class CreateHar(object):
    """create HTTP archive file"""

    def __init__(self, mob_path):
        """initial setup"""
        self.browser_mob = mob_path
        self.server = self.driver = self.proxy = None

    @staticmethod
    def __store_into_file(title, result):
        """store result"""
        har_file = open('HARs/' + title + '.har', 'w')
        har_file.write(str(result))
        har_file.close()

    def __start_server(self):
        """prepare and start server"""
        self.server = Server(self.browser_mob)
        self.server.start()
        self.proxy = self.server.create_proxy()

    def __start_driver(self):
        """prepare and start driver"""
        profile = webdriver.FirefoxProfile()
        profile.set_proxy(self.proxy.selenium_proxy())
        self.driver = webdriver.Firefox(firefox_profile=profile)

    def start_all(self):
        """start server and driver"""
        self.__start_server()
        self.__start_driver()

    def create_har(self, title, url):
        """start request and parse response"""
        self.proxy.new_har(title)
        self.driver.get(url)
        result = json.dumps(self.proxy.har, ensure_ascii=False)
        self.__store_into_file(title, result)

    def stop_all(self):
        """stop server and driver"""
        self.server.stop()
        self.driver.quit()


if __name__ == '__main__':
    path = "C:\\Users\\perus\\OneDrive\\Documents\\GitHub\\cy-automation-library\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy"
    RUN = CreateHar(path)
    RUN.start_all()
    RUN.create_har('google', 'http://google.com')
    RUN.create_har('stackoverflow', 'http://stackoverflow.com')
    RUN.stop_all()