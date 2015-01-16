#!/usr/bin/env python
# coding=utf-8


"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import sys
import logging

FORMAT = ("$BOLD[%(asctime)s] [%(levelname)s] %(message)s$RESET")
SIMPLE_FORMATER = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')


class CUSTOM_LOGGING:
    good = 99


class ColorFormatter(logging.Formatter):

    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

    COLOR_SEQ = "\033[1;%dm[%s] %s\033[1;m"

    COLORS = {
        'DEBUG': BLUE,
        'INFO': WHITE,
        'WARNING': YELLOW,
        'ERROR': RED,
        'CRITICAL': RED,
        'GOOD': GREEN,
    }

    SYMBOLS = {
        'DEBUG': '~',
        'INFO': '*',
        'WARNING': '-',
        'ERROR': '!',
        'CRITICAL': '!',
        'GOOD': '+',
    }

    def __init__(self, use_color=True, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)
        self.use_color = use_color

    def format(self, record):
        format_str = logging.Formatter.format(self, record)
        levelname = record.levelname
        if self.use_color and levelname in self.COLORS:
            fore_color = 30 + self.COLORS[levelname]
            fore_symbol = self.SYMBOLS[levelname]
            format_str = self.COLOR_SEQ % (fore_color, fore_symbol, format_str)
        return format_str


def init_logger(name='3102', log_file_path=None, show_color=True,
                log_level=logging.DEBUG):

    logging.addLevelName(CUSTOM_LOGGING.good, "GOOD")
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    color_stream_handler = logging.StreamHandler(sys.stdout)
    color_stream_handler.setFormatter(SIMPLE_FORMATER)
    color_stream_handler.setLevel(logging.DEBUG)
    if show_color:
        color_stream_handler.setFormatter(ColorFormatter())
    logger.addHandler(color_stream_handler)

    if log_file_path:
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(SIMPLE_FORMATER)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)
    return logger
