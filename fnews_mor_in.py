#!/home/wangy/anaconda3/bin/python
import pymysql
import datetime
import tushare as ts

def run():
    #获取时间
    now = datetime.datetime.now()
    year = int(now.strftime('%Y'),10)
    day = int(now.strftime('%d'),10)
    month = int(now.strftime('%m'),10)
    datenow = now.strftime('%Y-%m-%d') #年月日
    last_season = int((month-1)/3)
    dict_time = {}
    dict_time['day'] = day
    dict_time['month'] = month
    dict_time['year'] = year

    #
    cont = ts.get_index()
    indexlist = []
    indexlist.append(cont[cont.code == '000001'].index[0])
    indexlist.append(cont[cont.code == '399001'].index[0])
    indexlist.append(cont[cont.code == '399006'].index[0])

    tmp_num = [0,0,0]

    for i in range(0,3):
        tmp_num[i] = cont.loc[indexlist[i],'change']


    dict_mor = {}
    dict_mor['hszf'] = tmp_num[0] #沪市涨幅
    dict_mor['hsds'] = round(cont.loc[indexlist[0],'open'],2) #沪市点数
    dict_mor['szczzf'] = tmp_num[1] #深圳成指涨幅
    dict_mor['szczds'] = round(cont.loc[indexlist[1],'open'],2) #深圳成指点数
    dict_mor['cybzf'] = tmp_num[2] #创业板涨幅
    dict_mor['cybds'] = round(cont.loc[indexlist[2],'open'],2) #创业板点数


    #连接数据库
    from my_config import MyConfig
    mycfg = MyConfig("service")
    service_host = mycfg.get('service_host')
    service_port = int(mycfg.get('service_port'))
    service_user = mycfg.get('service_user')
    service_passwd = mycfg.get('service_passwd')
    service_db = mycfg.get('service_db')
    service_charset = mycfg.get('service_charset')
    conn = pymysql.connect(host = service_host,port = service_port,user = service_user,passwd = service_passwd ,db = service_db,charset = service_charset)
    cur = conn.cursor()
    stringsql = []
    #"INSERT INTO ShanghaiIndex (change,open,date,type) VALUES ()"
    stringsql.append("INSERT INTO ShanghaiIndex (changeper,opends,date,type) VALUES (" + str(dict_mor['hszf']) + "," + str(dict_mor['hsds']) +
                     ",\"" + datenow + "\",1) ON DUPLICATE KEY UPDATE changeper = " + str(dict_mor['hszf']) + ",opends = " + str(dict_mor['hsds']) )
    stringsql.append("INSERT INTO ShenzhenIndex (changeper,opends,date,type) VALUES (" + str(dict_mor['szczzf']) + "," + str(dict_mor['szczds']) +
                     ",\"" + datenow + "\",1) ON DUPLICATE KEY UPDATE changeper = " + str(dict_mor['szczzf']) + ",opends = " + str(dict_mor['szczds']))
    stringsql.append("INSERT INTO CYSection (changeper,opends,date,type) VALUES (" + str(dict_mor['cybzf']) + "," + str(dict_mor['cybds']) +
                     ",\"" + datenow + "\",1) ON DUPLICATE KEY UPDATE changeper = " + str(dict_mor['cybzf']) + ",opends = " + str(dict_mor['cybds']))
    for i in range(0,len(stringsql)):
        cur.execute(stringsql[i])
    conn.commit()
    cur.close
    conn.close()
