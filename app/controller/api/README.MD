为确保兼容性，老版本api不应当删除
请求格式为：
http://邮箱:密码@服务器地址:服务器端口/api/api版本号/地址

例如：
邮箱123@qq.com，密码888
服务器地址为本地服务器，127.0.0.1
服务器端口5000
api版本号为1.0
请求获取tokens
则正确的请求为：发送post请求
http://123@qq.com:888@127.0.0.1:5000/api/v1.0/tokens/
返回结果：
{
    "expiration": 3600,
    "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTYzMzE3OTMxOSwiZXhwIjoxNjMzM
            TgyOTE5fQ.eyJpZCI6MX0.OC00FA3waPlzf26Fr-_6PBcVXXF_v_BRsk18eJMxyY8"
}

或者直接携带token访问，获取某用户信息，正确的请求为：
发送get请求
http://eyJhbGciOiJIUzI1NiIsImlhdCI6MTYzMzE3OTkxOSwiZXhwIjoxNjMzMTgzNTE5fQ.e
        yJpZCI6MX0.CUPBxvkgWUJrtUbrfaGeVrtnDdkMpCGcnyHzWmZga5U
        @127.0.0.1/api/v1.0/users/1

json数据post与put的方法：
res = requests.post("http://token值:@服务器地址:服务器端口/api/v1.0/posts/",
                    json={"body":"待发表的post内容"})
使用postman测试，
1. 请发送json请求，在请求栏中的Body中选择raw，
    下方框输入{"body":"待发表的post内容"}，
2. 选择JSON，不是Text，或者选择Header，找到Content-Type，
    将后面的值改为 application/json，
3. 将Header中的Accept值改为application/json
（这步用于 /app/controller/errors.py 中对于请求类型的判断


