配置文件加密与解密
===================
## 1. xml文件编写
**示例代码如下:**
```
from config.write_file import Write

xml = Write(key="abcde")  # key为用于配置文件加密、解密，不提供key值则不进行加密
xml.add_item("key", "SECRET_KEY", "????")  # add_item第一参数为组别名称、后两个参数为键值对
xml.add_item("sql_url", "SQLALCHEMY_DATABASE_URI", "mysql+pymysql://***:***@***:3306/***E?charset=utf8")
xml.add_item("emile", "MAIL_SERVER", "smtp.**.com")
xml.add_item("emile", "MAIL_PORT", "465")
xml.write("config.txt")  # 写入文件
```
执行上述代码，会生成如下结构的xml文件，并加密存储（也可以不提供key值，不进行加密）
```
<?xml version="1.0" encoding="utf-8"?>
<server_ini>
 <key id="SECRET_KEY">????</key>
 <sql_url id="SQLALCHEMY_DATABASE_URI">mysql+pymysql://***:***@***:3306/***E?charset=utf8</sql_url>
 <emile id="MAIL_SERVER">smtp.**.com</emile>
 <emile id="MAIL_PORT">465</emile>
</server_ini>
```

<br>

------

## 2. xml文件读取

**示例代码如下:**

```
from config.read_file import Read

reader = Read(key="abcde")  # key为用于配置文件加密、解密，创建一个reader
xml = reader.read("config.txt")  # 用reader读取配置文件，返回xml对象
tile = Read.tile(xml, element_list=("key", "emile"), interpret=True)
# 从xml对象中取出key分组和emile分组的全部键值对，返回字典
# 当interpret为True的时候会翻译键值对中的值，若值为"T"则会替换为True，"F"替换为False
#    整数被替换为int型，小数被替换为float型
print(tile)
```

输出结果为：

```
{
    'SECRET_KEY': '????', 
    'MAIL_SERVER': 'smtp.**.com', 
    'MAIL_PORT': 465
}
```

<br>

-----

## 3. 快速使用

通过以下函数可以在命令行界面强制用户输入解密密码，密码错误会退出程序，
密码正确时读取文件，并进行tile操作，取出key和emile分组，返回值与上一个
程序相同

```
from config.check_pwd import CheckPwd

tile = CheckPwd.check_pwd_input_with_force("config.txt"),
        group=("key", "emile"))
 ```
 
<br>
<br>
遇到问题请联系zjx
