# !/home/wangy/anaconda3/bin/python
import gevent
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from gevent.pool import Pool
from flask import Flask, request
from multiprocessing import cpu_count
import time, logging, logging.handlers, json, platform, hashlib,sys
import fnews_daily_out
import datetime

#获取时间
datet = {}
def get_date():
    now = datetime.datetime.now()
    datet['year'] = int(now.strftime('%Y'),10)
    datet['day'] = int(now.strftime('%d'),10)
    datet['month'] = int(now.strftime('%m'),10)
    datet['today'] = now.strftime('%Y-%m-%d') #年月日
    datet['last_season'] = int((datet['month']-1)/3)


app = Flask(__name__)
route = app.route




mylog = logging.getLogger('service')



from fnews_mor_in import run as a1
from fnews_noon_in import run as a2
from fnews_afternoon_in import run as a3
from fnews_company_in import run as a4
from fnews_category_in import run  as a5
from fnews_conception_in import run as a6
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(a1, 'cron', day_of_week='0-6', hour=17,  minute=14)       #每天9：35触发run方法
scheduler.add_job(a2, 'cron', day_of_week='0-6', hour=11,  minute=35)
scheduler.add_job(a3, 'cron', day_of_week='0-6', hour=15,  minute=5)
scheduler.add_job(a4, 'cron', day_of_week='0-6', hour=15,  minute=8)
scheduler.add_job(a5, 'cron', day_of_week='0', hour=12,  minute=8)
scheduler.add_job(a6, 'cron', day_of_week='0', hour=12,  minute=18)
scheduler.start()

@route('/')
def index():
    return '''hello world!'''

@route('/fnews_daily',methods = ['POST','GET'])
def fnews_daily():
    data = {}
    result = {}
    try:
        type = request.values['type']
        date = request.values['date']
        if date == '':
            get_date()
            date = datet['today']
        fnews_daily_out.date(date)
        if type == '1':
            news =  fnews_daily_out.mor_out()
        elif type == '2':
            news = fnews_daily_out.noon_out()
        elif type == '3':
            news  = fnews_daily_out.afternoon_out()
        result['news'] = news
        data['msg'] = '操作成功'
        data['status'] = 'true'
    except Exception as e:
        mylog.exception(e)
        data['msg'] = str(e)
        data['status'] = 'false'
    data['result'] = result
    return json.dumps(data)

@route('/fnews_amountRank',methods = ['POST','GET'])
def fnews_amountRank():
    data = {}
    result = {}
    try:
        date = request.values['date']
        if date == '':
            get_date()
            date = datet['today']
        fnews_daily_out.date(date)
        news = fnews_daily_out.company_amount_out()
        result['news'] = news
        data['msg'] = '操作成功'
        data['status'] = 'true'
    except Exception as e:
        mylog.exception(e)
        data['msg'] = str(e)
        data['status'] = 'false'
    data['result'] = result
    return json.dumps(data)

@route('/fnews_marketIndustry',methods = ['POST','GET'])
def fnews_marketIndustry():
    data = {}
    result = {}
    try:
        date = request.values['date']
        if date == '':
            get_date()
            date = datet['today']
        fnews_daily_out.date(date)
        news = fnews_daily_out.industry_out()
        result['news'] = news
        data['msg'] = '操作成功'
        data['status'] = 'true'
    except Exception as e:
        mylog.exception(e)
        data['msg'] = str(e)
        data['status'] = 'false'
    data['result'] = result
    return json.dumps(data)

@route('/fnews_search',methods = ['POST','GET'])
def fnews_search():
    data = {}
    result = {}
    try:
        name = request.values['name']
        news = fnews_daily_out.name2code(name)
        news = [{'code': d[1], 'name': d[0]} for d in news]
        result['news'] = news
        data['msg'] = '操作成功'
        data['status'] = 'true'
    except Exception as e:
        mylog.exception(e)
        data['msg'] = str(e)
        data['status'] = 'false'
    data['result'] = result
    return json.dumps(data)


@route('/fnews_companyCombine',methods = ['POST','GET'])
def fnews_companyCombine():
    data = {}
    result = {}
    try:
        date = request.values['date']
        code = request.values['code']
        if date == '':
            get_date()
            date = datet['today']
        fnews_daily_out.date(date)
        news = fnews_daily_out.company_combine_out(code)
        result['news'] = news
        data['msg'] = '操作成功'
        data['status'] = 'true'
    except Exception as e:
        mylog.exception(e)
        data['msg'] = str(e)
        data['status'] = 'false'
    data['result'] = result
    return json.dumps(data)
@route('/fnews_markets',methods = ['POST','GET'])
def fnews_markets():
    data = {}
    result = {}
    try:
        date = request.values['date']
        type = request.values['type']
        if date == '':
            get_date()
            date = datet['today']
        fnews_daily_out.date(date)
        news = fnews_daily_out.marketIndustry_out(type)
        result['news'] = news
        data['msg'] = '操作成功'
        data['status'] = 'true'
    except Exception as e:
        mylog.exception(e)
        data['msg'] = str(e)
        data['status'] = 'false'
    data['result'] = result
    return json.dumps(data)


if __name__ == "__main__":
    host, port = '0.0.0.0', int(sys.argv[1]) if len(sys.argv) == 2 else 9001
    mylog.info("%s:%s service start..." % (host, port))
    WSGIServer((host, port), app, spawn=Pool(1000)).serve_forever()



