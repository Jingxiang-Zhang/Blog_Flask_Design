该目录下所有的内容均用于测试使用，在 /manager.py中使用：
from app.test import load_test_blueprint
load_test_blueprint(app) 
即可导入测试模块
目前的测试模块为：

用于安全测试的 /test/web_safety

可以在 manager.py中列出所有测试的路径
from scripts.testing_route import get_route
get_route(app=app, route_group=("/test/web_safety/",), show=True)

test模块还在 /app/webapp/templates 目录下建立了test目录，
以及/app/webapp/static 目录下建立了test目录，
正式版上线后可以将其删除。