## 插件开发说明

### 插件目录创建
```
$ cd plugins
# plugin_name为插件名
$ mkdir plugin_name
$ touch plugin_name/config.yaml
$ touch plugin_name/work.py
```

### 插件配置[config.yaml]
```
enable: true/false # 是否开启插件,false则不加载该插件
onerepeat: true/false # 是否重复执行,详情见下方
input: [] # 输入格式,root_domain/domain/ip
output: [] # 输出格式,root_domain/domain/ip
descript: # 插件描述
name: # 插件名,请与目录名一致
chinesename: # 插件中文名

onerepeat:
意思为一次重复，部分插件存在一种情况,如通过一个目标a得到结果集b，
那么将结果集B中的任意作为目标进行查理得到的还是结果集b，也就没必要多次调用
```

### 插件主文件[work.py]
* from core.plugin import Plugin
* 编写插件同名类,集成Plugin
* 必须重写__init__方法,参考icp插件
 * 在__init__里调用super(插件名, self).__init__('插件名')
* 类内必须存在start方法,参数必须为start(self, domain, domain_type, level)
  * domain str,插件执行目标
  * domain_type str,输入的目标类型(domain/root_domain/ip)
  * level int,当前执行的层数
  * 要求在start方法里调用super(插件名, self).start(domain, domain_type, level)
  * 要求在程序执行结束返回结果前调super(插件名, self).end()
* 插件执行结果返回
  * 如果没有结果则直接return self.result(不用赋值,默认值为None)
  * 如果有结果,按以下结构return结果(对self.result赋值)
  * 要求结果中存在root_domain/ip/domain三个key,值为list
  ```
    self.result = {
        'root_domain': root_domains,
        'ip': ips,
        'domain': domains
    }
  ```
  * 结果应该判断类型去重归入self.result.root_domain/ip/domain,可根据下方API说明使用方法

### 插件可使用API
* self.plugin_path 当前插件目录
* self.logger getLogger
* self.req,可以使用self.req.request进行网络请求
  * 禁止自引用其他网络请求模块进行网络请求
  * 封装的requests.Request
  * 使用参考http://www.python-requests.org/en/latest/api/?highlight=request#requests.request
* self.conf 对应config.yaml里的配置

### 可以使用的方法
* 具体参考comm目录下的文件与方法
* from comm.文件名 import 方法

### 插件测试用例
* 进入tests下对应单元或功能测试目录下创建对应插件目录,编写测试用例

### 要求
* config.yaml和work.py为必须文件
* work.py为入口文件,请按要求开发work.py文件,允许在插件目录下添加其他文件
* config.yaml文件为插件配置文件,所有配置项都必须并注意格式
