## 3102

* A domain/ip Fuzzing tool for vulnerability mining

### 简介
* A domain/ip Fuzzing tool for vulnerability mining
* 一个挖洞的辅助工具
* 通过各种手段，从url或者ip得到相关的所有site/ip等

### 架构介绍
* 基于gevent和threading,多线程+协程运行,高效快速
* 动态加载插件和结果输出模板,可自行根据文档开发插件和结果输出模板
* 动态调度,自动回收结果并做判断及下发新任务进行插件的执行处理
* 系统信号捕获,在某插件卡死情况下,可以Ctrl+C结束执行,可捕获并输出已有结果

### 安装与开发
#### 安装
```bash
$ sudo apt-get install python-virtualenv
$ sudo apt-get install python-setuptools
$ easy_install pip
```

```bash
$ git clone git@github.com:fooying/3102.git
$ cd 3102
$ virtualenv venv
$ source venv/bin/activate
$ pip install -U pip
$ pip install -r requirement.txt
```

#### 参与开发
```bash
$ cd 3102
$ source venv/bin/activate
```
* 插件开发:[docs/plugins/README.md](docs/plugins/README.md)
* 结果输出模板开发:[docs/output/README.md](docs/output/README.md)

* 测试用例开发
  * cd 3102/tests
  * 对应单元测试和功能测试进行开发测试用例
  * 不同的模块进入到对应目录进行开发

* 也欢迎参与主架构的改进和新功能的开发,直接发送Pull Requests

### 感谢
* 感谢名单 [docs/THANKS.md](docs/THANKS.md)

### 使用说明
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
  -h, --help            Show this help message and exit
  -V, --version         show program's version number and exit
  -t TARGET, --target TARGET
                        Target domain/rootdomain/ip
                          (DEFAULT: None)
  -m MAX_LEVEL, --max_level MAX_LEVEL
                        Max level to get domain/ip/rootdomain
                          (DEFAULT: 4)
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        File to ouput result
                          (DEFAULT: None)
  --format OUTPUT_FORMAT
                        The format to output result,
                        default list:
                        csv/txt/json/yaml/html
                          (DEFAULT: csv)
  --log_file LOG_FILE   Log file
                          (DEFAULT: None)
  --log_level {1,2,3,4}
                        Log level of output to file
                          1 - DEBUG
                          2 - INFO
                          3 - WARNING
                          4 - ERROR
                          (DEFAULT: 1)
  --proxy_file PROXY_FILE
                        Proxy file, one line one proxy, each line format:
                        schem,proxy url,
                        eg:http,http://1.1.1.1:123
                          (DEFAULT: None)
  --verify_proxy        If verify the proxy list
                          (DEFAULT: False)
  --timeout TIMEOUT     Request timeout
                          (DEFAULT: 10)
  --live_test           Turn off Domain live test
                          (DEFAULT: False)

```
