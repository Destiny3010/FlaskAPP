"""
开发应用服务，用户登录的时候获取到用户id，云服务器中数据库内查到PIN码并返回
使用Flask框架，需要先安装Flask：pip install flask
启动Flask服务，如果文件名为‘app.py’的时候，直接使用:flask run,否则需要更新服务启动文件(Mac和Linux)：export FLASK_APP=xxx.py，(windows)set FLASK_APP=xxx.py
"""
from flask import Flask
import pymysql.cursors
from flask import request
from pywchat import Sender
import requests
from config.config import config

app = Flask(__name__)

# 测试用接口
@app.route('/')
def hello():
    return 'Hello!'

@app.route('/getCardNumber')
def getCardNumber():
    # 企业微信信息配置
    app = Sender(config.wechat_info['corpid'],config.wechat_info['corpsecret'],config.wechat_info['agentid'])

    ACCESS_TOKEN = app.get_token()
    CODE = request.args.get('code')

    chat_api = {
        'USER_INFO': 'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token={}&code={}'
    }

    rsp = requests.get(chat_api.get('USER_INFO').format(ACCESS_TOKEN,CODE))

    userId = rsp.json().get("UserId")

    # 连接数据库
    connect = pymysql.Connect(
        host='8.142.152.43',
        port=3306,
        user='sjg',
        passwd='Shenjunguang123.',
        db='wechat',
        charset='utf8'
    )
    # 获取游标
    cursor = connect.cursor()
    
    # 查询数据
    sql = "SELECT papercut_pin FROM wechat.papercut_info where wechat_id='{}';".format(userId)
    
    cursor.execute(sql)

    # 关闭连接
    cursor.close()
    connect.close()
    return '''
    <h1 style="text-align: center;">个人ID编号:</h1><h1 style="text-align: center;">'+ str(cursor.fetchone())[2:8] + '</h1>
    '''
    # return '<h1 style="text-align: center;">个人ID编号:</h1><h1 style="text-align: center;">'+ str(sql) + '</h1>'

if __name__ =='__main__':
   app.run(host = '0.0.0.0' ,port = 3000)