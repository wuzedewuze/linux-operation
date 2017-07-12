# -*- coding: utf-8 -*-

from conf import error_log_file, info_log_file
import logging

def log_init():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt = '%Y-%m-%dT%H:%M:%S',
                        filename = error_log_file,
                        filemode = 'a')
    return logging


def log_info():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt = '%Y-%m-%dT%H:%M:%S',
                        filename = info_log_file,
                        filemode = 'a')
    return logging


