#!/home/wangy/anaconda3/bin/python
import os, sys,configparser, platform
import logging
import logging.handlers
from logging import config

path = "production.ini"
if 'Windows' == platform.system():
    path = 'test.ini'
configFile = os.path.join(os.path.dirname(__file__), path)
cp = configparser.ConfigParser()
cp.read(configFile, encoding='utf-8')
config.fileConfig(cp)

class MyConfig():
    def __init__(self, confHead):
        self.path = configFile
        self.confHead = confHead
        self.cf = configparser.ConfigParser()
        self.cf.read(self.path, 'utf-8')

    def get(self, name, default=[]):
        try:
            return self.cf.get(self.confHead, name)
        except:
            if default == []:
                raise ValueError("not key %s" % name)
            return default

    def set(self, key, value, head=None):
        if not head:
            head = self.confHead
        try:
            self.cf.set(head, key, str(value))
            self.cf.write(open(self.path, 'w'))
        except:
            return False
        return True

    def reload(self):
        try:
            self.cf.read(self.path)
            return True
        except:
            return False

mycfg = MyConfig("service")
