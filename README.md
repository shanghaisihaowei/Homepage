# HomePage
HomePage

```python
1、先建好虚拟环境

2、pip安装equirements.txt包依赖
pip install -r requirements.txt
阿里云源
-i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
3、迁移数据库

python manage.py makemigrations

python manage.py migrate

4、启动命令
方式一：
python manage.py runserver 127.0.0.1:8000

方式二：
内网启动命令：
daphne -p 8000 HomePage.asgi:application

订单号命令
snowflake_start_server --address=127.0.0.1 --port=8910

## 注意：worker的启动命令: celery -A celery_task  worker -l info -P eventlet

celery -A celery_task beat -l info


```
python manage.py createsuperuser
更新依赖命令
pip freeze >requirements.txt
## settings.py配置

