一个挖洞的辅助工具
通过各种手段，从url或者ip得到相关的所有site/ip等
欢迎参与项目
```

                 _____  __  _____  _____
                |____ |/  ||  _  |/ __  \
                    / /`| || |/' |`' / /'
                    \ \ | ||  /| |  / /
                .___/ /_| |\ |_/ /./ /___
                \____/ \___/\___/ \_____/

        Domain/ip Fuzzing tool for vulnerability mining
               By Fooying(www.fooying.com)

usage:
  eg1: python run3102.py --target

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -t TARGET, --target TARGET
                        Target domain/rootdomain/ip
                          (DEFAULT: None)
  -m MAX_LEVEL, --max_level MAX_LEVEL
                        max level to get domain/ip/rootdomain
                          (DEFAULT: 10)
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        file to ouput result
                          (DEFAULT: result.txt)
  --log_file LOG_FILE   log file
                          (DEFAULT: None)
  --log_level {1,2,3,4}
                        level of logging
                          1 - DEBUG
                          2 - INFO
                          3 - WARNING
                          4 - ERROR
                          (DEFAULT: 1)
  --proxy_file PROXY_FILE
                        proxy file, one line one proxy, each line format:schem,proxy url,eg:http,http://1.1.1.1:123
                          (DEFAULT: None)
  --verify_proxy        if verify the proxy list
                          (DEFAULT: False)
  --timeout TIMEOUT     request timeout
                          (DEFAULT: 10)

```
