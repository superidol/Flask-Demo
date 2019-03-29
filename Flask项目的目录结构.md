# Flask-Demo

## 1、Flask项目目录结构
```
| - projectName
	| - app  //程序包
		| - templates //jinjia2模板
		|- static //css,js 图片等静态文件
		| - main  //py程序包 ，可以有多个这种包，每个对应不同的功能
			| - __init__.py
			|- errors.py
			|- forms.py
			|- views.py
		|- __init__.py
		|- email.py //邮件处理程序
		|- models.py //数据库模型
	|- migrations //数据迁移文件夹
	| - tests  //单元测试
		|- __init__.py
		|- test*.py //单元测试程序，可以包含多个对应不同的功能点测试
	|- venv  //虚拟环境
	|- requirements.txt //列出了所有依赖包以及版本号，方便在其他位置生成相同的虚拟环境以及依赖
	|- config.py //全局配置文件，配置全局变量
	|- manage.py //启动程序
```
由上图可以看出，项目主要包含四个子目录.。

1.全局config配置文件
系统经常要用到很多全局配置变量以及多套环境（开发，测试，生产）配置变量，因此单独的使用配置文件来进行配置可以做到方便管理。本示例项目主要包含加密使用的SECRET_KEY，发送邮件的相关配置，数据库配置等

```
import os
basedir = os.path.abspath(os.path.dirname(__file__))
 
class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
	
	@staticmethod //此注释可表明使用类名可以直接调用该方法
	def init_app(app): //执行当前需要的环境的初始化
		pass
		
class DevelopmentConfig(Config): //开发环境
	DEBUG = True
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
 
class TestingConfig(Config): //测试环境
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
 
class ProductionConfig(Config): //生产环境
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
 
config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}
```
2.app程序包

如果所有的程序都写在一个文件中，程序在执行的时候配置数据就在程序实例执行之前就导入了，但是为了能够动态的修改配置文件，需要在程序实例初始化之前留时间或者或是留加载空隙给配置文件，需要采用程序实例延迟初始化。因此单独创建一个app_create()函数实现程序实例初始化。在app的__init__.py文件中新建方法app_create():

```
from flask import Flask, render_template from flask.ext.bootstrap
import Bootstrap from flask.ext.mail import Mail from flask.ext.moment
import Moment from flaskext.sqlalchemy import SQLAlchemy from config
import conifg
 
 
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
 
 
def app_create(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name]) //可以直接把对象里面的配置数据转换到app.config里面
    config[config_name].init_app(app)
  
    bootstrap.app_init(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    #路由和其他处理程序定义
    #...
    return app
```


当然这个初始化只是初始化了扩展程序。路由和错误页面还没有定义，由于现在程序是在运行的时候创建而不是在解释的时候，只有在调用了app_create()之后才能使用app_route装饰器定义路由，但是这时定义路由就太晚了。因此Flask提供了蓝本功能，在蓝本中定义的路由跟程序实例延迟初始化类似，定义的路由是处于休眠的状态的，只有在蓝本注册到程序之后，路由才真正成为程序的一部分
所有的蓝本可以定义在一个文件中，也可以分模块单独定义。下面定义main包中的蓝本app/main/__init__.py

```
from flask import Blueprint main = Blueprint('main', __name__)
 
from . import views, errors //由于路由和错误处理页面定义在这个文件里面，导入到蓝本把他们关联起来，又因为views.py，error.py需要导入蓝本main，防止循环导入所以放到最后
```

修改app_create函数，注册蓝本 
```
def app_create(config_name): #... from
.main import main as main_blueprint //从当前目录下面的main子目录导入main
app.register_blueprint(main_blueprint)
 
 
    #...
    return app
```
蓝本中定义的路由 
```
from datetime import datetime from flask import
render_template, session, redirect, url_for
 
from . import main
from .forms import NameForm
from .. import db
from ..models import User
 
 
@main.route('/', methods =['GET', 'POST']) //不同的蓝本装饰器不同
def  index():
    form = NameForm()
    if form.validate_on_submit():
    #...
        return redirect(url('main.index')) //每个蓝本都有一个命令空间，生成url需要加上命名空间前缀
    return render_template('index.html', form = form, name = session.get('name'), known = session.get('known', False), current_time = datetime.utcnow())
```


3.启动脚本

顶层的manage.py用于启动程序 
```
#!/usr/bin/env python import os from app
import create_app, db from app.models import User, Role from
flask.ext.script import Manager, Shell from flask.ext.migrate import
Migrate, MigrateCommand
 
 
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
 
 
def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
 
 
if __name__ == '__main__':
manager.run()
```

4.需求文件requirements.txt


程序中必须包含一个requirements.txt 文件，用于记录所有依赖包及其精确的版本号。如果要在另一台电脑上重新生成虚拟环境，这个文件的重要性就体现出来了，例如部署程序时使用的电脑。pip 可以使用如下命令自动生成这个文件：

```(venv) $ pip freeze >requirements.txt```


如果你要创建这个虚拟环境的完全副本，可以创建一个新的虚拟环境，并在其上运行以下命令：

```(venv) $ pip install -r requirements.txt```


5.单元测试

tests包包含了单元测试，也可以分功能模板，建立单独的单元测试文件


6.创建数据库

使用数据迁移命令创建数据库 

```(venv) $ python manage.py db upgrade```