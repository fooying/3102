#!/usr/bin/env python
# coding=utf-8
# Fooying@2014-10-20 10:58:36

"""
相关配置文件
"""

PROXY = {
    #"http"："http://user:password@host"
    "http": "http://121.12.255.212:8086"
}


ICP_API_CONFIG= {
    "icpchaxun":{
        "get_zt": (
            "http://www.icpchaxun.com/yuming/%s/",
            """
            <a\starget="_blank"\shref="/zhuti/.*?">.*?
            \s*?([^\s]*?)</a>''',
            """
        ),
        "get_domains": (
            "http://www.icpchaxun.com/zhuti/%s/",
            """
            """
        )
        '''
    }
}
