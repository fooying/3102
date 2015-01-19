#!/usr/bin/env python
# coding=utf-8

"""
Copyright (c) 2014 Fooying (http://www.fooying.com)
Mail:f00y1n9[at]gmail.com
"""

import sys
import os

from config.settings import START_STR
from comm.utils import weAreFrozen, getUnicode

def modulePath():
    """
    This will get us the program's directory, even if we are frozen using py2exe

    copy from sqlmap. (sqlmapproject/sqlmap)[https://github.com/sqlmapproject/sqlmap]
    """

    try:
        _ = sys.executable if weAreFrozen() else __file__
    except NameError:
        _ = inspect.getsourcefile(modulePath)

    return os.path.dirname(os.path.realpath(getUnicode(_, sys.getfilesystemencoding())))


def main(args=None):
    print(START_STR)
    ROOT_PATH = modulePath()
    sys.path.insert(0, os.path.join(ROOT_PATH, 'thirdparty'))
    try:
        from core.parser import parse
        from core.controllers.controller import start

        args = parse()
        start(args)
    except Exception, e:
        print e
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
