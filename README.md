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

### 使用与开发
#### 使用
* 3102暂时只支持Python版本2.6.x和2.7.x  
* 3102需要gevent库的支持,使用前请先使用`pip install gevent`进行安装  
* 查看帮助信息  
```bash
$ python run3102.py -h
```
* 使用例子
  * 基本用法  
  ```bash
  $ python run3102.py -t 目标domain/ip
  ```
  * 扫描www.example.com相关的站点/ip,使用html保存结果:  
  ```bash
  $ python run3102.py -t www.example.com --format html
  ```
  * 扫描www.example.com相关的站点/ip,结果保存在当前文件夹下output.csv中(默认format为csv):  
  ```bash
  $ python run3102.py -t www.example.com -o ./output
  $ python run3102.py -t www.example.com -o ./output.csv
  ```
  * 扫描www.example.com相关的站点/ip,结果保存在当前文件夹下output.html中:  
  ```bash
  $ python run3102.py -t www.example.com -o ./output.html
  $ python run3102.py -t www.example.com -o ./output --format html
  ```
  * 指定只执行`domain2ip`,`domain2root`,`icp`三个插件,结果保存在当前文件夹下output.csv中:  
  ```bash
  $ python run3102.py -t www.example.com -p domain2ip domain2root icp -o ./output.csv
  ```

#### 参与开发
* 请将使用的第三方模块库置于thirdparty目录

* 插件开发:[docs/plugins/README.md](docs/plugins/README.md)
* 结果输出模板开发:[docs/output/README.md](docs/output/README.md)

* 测试用例开发
  * cd 3102/tests
  * 对应单元测试和功能测试进行开发测试用例
  * 不同的模块进入到对应目录进行开发

* 也欢迎参与主架构的改进和新功能的开发,直接发送Pull Requests

### 感谢
* 感谢名单 [docs/THANKS.md](docs/THANKS.md)

### 详细选项说明
```

                 _____  __  _____  _____
                |____ |/  ||  _  |/ __  \
                    / /`| || |/' |`' / /'
                    \ \ | ||  /| |  / /
                .___/ /_| |\ |_/ /./ /___
                \____/ \___/\___/ \_____/       {2.1-ef7e093}

        Domain/ip Fuzzing tool for vulnerability mining
            By Fooying (http://www.fooying.com)

usage:
  eg1: python run3102.py -t www.example.com

optional arguments:
  -h, --help            Show this help message and exit
  -V, --version         show program's version number and exit
  -t TARGET, --target TARGET
                        Target domain/rootdomain/ip
                          (DEFAULT: None)
  -p plugin [plugin ...], --plugins plugin [plugin ...]
                        Specify the plugins
                        avaliable: domain2ip domain2root icp dnszonetransfer
                        ip2domain subdomain subdomain_brute
                          (DEFAULT: None)
  -m MAX_LEVEL, --max_level MAX_LEVEL
                        Max level to get domain/ip/rootdomain
                          (DEFAULT: 4)
  --pool_size POOL_SIZE
                        Max number of Thread pool size
                          (DEFAULT: 500)
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        File to ouput result
                          (DEFAULT: None)
  --format OUTPUT_FORMAT
                        The format to output result,
                        default list:
                        txt/yaml/json/csv/html
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
  --alive_check         Check alive and accessible status of domain
                          (DEFAULT: False)

```
