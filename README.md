### Introduction


### Project Environment Configuration

#### 1. Download Configuration File

`
pip install -r requirements.txt
`

#### Config flask-bootstrap and flask-moment

This process can be skip if the server is not in China. If the server is developed in China, you should subsitute the source, in order to improve the connection speed.

Open bootstrap.init in site-packages, change the text below:

```
bootstrap = lwrap(
    WebCDN('//cdn.bootcss.com/bootstrap/%s/' % BOOTSTRAP_VERSION), local)
jquery = lwrap(
    WebCDN('//cdn.bootcss.com/jquery/%s/' % JQUERY_VERSION), local)
html5shiv = lwrap(
    WebCDN('//cdn.bootcss.com/html5shiv/%s/' % HTML5SHIV_VERSION))
respondjs = lwrap(
    WebCDN('//cdn.bootcss.com/respond.js/%s/' % RESPONDJS_VERSION))
```

Open moment.py in site-packages, change the text below:

`
https://cdn.bootcss.com/moment.js/2.18.1/locale/af.js
`

or change the moment function usage as follow (more recommended):

`
{{ moment.include_moment(local_js="https://cdn.bootcss.com/moment.js/2.22.1/moment.min.js") }}
`

Open pagedown.py，subsitute cdn address into the following text:

`
//cdn.bootcdn.net/ajax/libs/pagedown/1.0/Markdown.Converter.min.js
//cdn.bootcdn.net/ajax/libs/pagedown/1.0/Markdown.Sanitizer.min.js
`

#### 3. Config parameter file

In the path /scripts/start_config.py，Change database url，i.e., sql_dev line, change email related items

In line 8, t = Write(key="****"), key is the AES code
In line 35, AVATAR_PATH is the user profile image path, you need to appoint an empty folder.

Run start_config.py directly, it will create a config.data file in the root directory, i.e., server startup configuration.

#### 4. Generate fake data

If you don't want to generate fake data, please skip this step.

First, you will need to choose the what fake data you want to generate, in /manager.py line 42

Second, you will need a folder full with image, as fake user avatar. change the path in /manager.py line 50

Then, type the command below, and wait a few second:

`python manager.py db generate_fake`

#### 5. Config server ip address and port

Open manager.py, modify the parameter in 'run' function

If you running in localhost, modify the port into `127.0.0.1`

If you running in the server side, then use `0.0.0.0`

#### 6. Start the Server

You can use `python manager.py run` to start the server, however, it will occupy current terminal (or cmd). If you want to run it in linux server, you can use  `sh start.sh`, this will help you run the server in the background





### Demonstration
