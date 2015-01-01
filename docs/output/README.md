## 结果输出

### 插件目录创建
```
$ cd core/output/templates
$ touch output_format.py
format为结果输出的格式化类型,如txt
```

### 代码编写
* 引用sdk,from template import Output
* 添加类,OutputName(Output)
  * Name为format的格式,要求首字母大写,如txt,就是OutputTxt
  * 继承Output
* 添加save方法,def save(self, output_file):
    * 先调用super(OutputTxt, self).save(output_file)
    * output_file为要输出结果的文件路径
* 然后根据实际的情况编写代码

### API
* self.logger getLogger
* self.result attrdict类型,存在三个子属性ip/domain/root_domain
  * 子属性类型为attrdict
  * 每个结果以dict存储在self.rsult.domain/ip/root_domain
  * 结果结构,{'target':str, 'module':str, 'level':int, 'parent_target':str}

### 结果结构[self.result]
```
self.result.ip = [
    {
        domain,:{# str,具体domain,值同下方domain
            'domain': str, 当前的domain/ip
            'module': str, 处理的插件
            'level': int, 所在level
            'parent_domain': str, 父domain
            }
    },
    ...
]
self.result.domain 与self.result.root_domain结构同上
```
