### Introduction

### Introduction

This project was my work as a research assistant (RA). <!-- outline-start -->It is a blog framework, programmed by Python, Flask, and MySQL as database.<!-- outline-end --> My mentor gave me the permission to publicize this project, which has no private information about my group.

My research group is working on food security. Each student in our group research on different part of job, which include bacterial detection by biological major student, data acquisition and transmission by EE major student, back-end design by myself. So, my work is to design a data receiving, processing, and showing platform, which is a blog like system.

My project has the following feature:

- A complete program framework, and MVC (Model-View-Controller) framework
- High security:
  - Dynamically validate form input, prevent XSS attack
  - Operate Database by model, defense SQL injection
  - Test upload file, defense file uploading attack
  - Secure password and dynamic token management system, prevent CSRF attack
  - Dynamic web page generation, prevent file inclusion vulnerability
  - Login detection and authorization management by role, prevent unauthorized access
  - HTTP secure (HTTPs) support, but you will need to apply for a secret key
- Easy database management
  - Monitor database execution status, giving timeout information
  - Fake data generate
  - Export data model to database, and database migration
  - Create initial configuration file
- Performance optimization
  - Load small Icons in batches by base64
  - Asynchronous data loading by ajax 
  - Multimedia data is stored by using hash paths
- Error handling system
- Email sending function
- API interface with multi-version support

Extendable Function (not implemented):
- Limit control, to prevent DDOS attack
- Multi language support

To understand the full edition of the project structure illustration, please read the [manual](https://github.com/Jingxiang-Zhang/Blog_Flask_Design/blob/main/manual.pdf).

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

#### Project Structure

ER diagram:

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Blog_Flask_Design/blob/main/img/ER.png">
</div>

Web access process:

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Blog_Flask_Design/blob/main/img/structure.png">
</div>

#### Before Login

Blog frontpage:

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Blog_Flask_Design/blob/main/img/frontpage.png">
</div>

Comments of the post:

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Blog_Flask_Design/blob/main/img/comment.png">
</div>

Click user avatar to get in the personal page:

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Blog_Flask_Design/blob/main/img/personal_page.png">
</div>

Check the follower and followed of user:

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Blog_Flask_Design/blob/main/img/followed.png">
</div>

#### Login as Administrator

User login:

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Blog_Flask_Design/blob/main/img/login.png">
</div>

You can edit other person's profile

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Blog_Flask_Design/blob/main/img/edit_profile.png">
</div>

You can also edit other user's post

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Blog_Flask_Design/blob/main/img/root_frontpage.png">
</div>

Everyone can put a new post.

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Blog_Flask_Design/blob/main/img/new_post.png">
</div>
