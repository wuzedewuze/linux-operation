# -*- coding: utf-8 -*-

from conf import error_log
import logging

def logOut():
    logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt = '%Y-%m-%dT%H:%M:%S',
                        filename = error_log,
                        filemode = 'a')
    return logging
