# -*-coding:utf-8-*-
'''
Created on 2015年12月10日

@author: maricoliu
'''

import logging
import sys, os


class Log():
    logger = logging.getLogger('LogHandler')
    fmt = logging.Formatter('%(asctime)s - %(message)s')
    shdlr = logging.StreamHandler(sys.stdout)
    shdlr.setFormatter(fmt)
    logger.addHandler(shdlr)

    @classmethod
    def debug(cls, msg):
        cls.logger.setLevel(logging.DEBUG)
        cls.logger.debug(msg)

    @classmethod
    def error(cls, msg):
        cls.logger.setLevel(logging.ERROR)
        cls.logger.error(msg)

    @classmethod
    def info(cls, msg):
        cls.logger.setLevel(logging.INFO)
        cls.logger.info(msg)


if __name__ == "__main__":
    Log.debug('debug')
    Log.error('error')
