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

    dict_noon = {}
    dict_noon['hszf'] = tmp_num[0]  # 沪市涨幅
    dict_noon['hsds'] = round(cont.loc[indexlist[0], 'close'], 2)  # 沪市点数
    dict_noon['hscj'] = round(cont.ix[indexlist[0],'amount'],3) #沪市成交
    dict_noon['szczzf'] = tmp_num[1]  # 深圳成指涨幅
    dict_noon['szczds'] = round(cont.loc[indexlist[1], 'close'], 2)  # 深圳成指点数
    dict_noon['szczcj'] = round(cont.ix[indexlist[1],'amount'],3) #深圳成指成交
    dict_noon['cybzf'] = tmp_num[2] # 创业板涨幅
    dict_noon['cybds'] = round(cont.loc[indexlist[2], 'close'], 2)  # 创业板点数
    dict_noon['cybcj'] = round(cont.ix[indexlist[2],'amount'],3) #c创业板成交

    #将数据依次存入list
    datalist = []
    datalist.append(dict_time)
    datalist.append(dict_noon)


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
    stringsql.append("INSERT INTO ShanghaiIndex (changeper,closeds,date,type,amount) VALUES ("
                     + str(dict_noon['hszf']) + "," + str(dict_noon['hsds']) + ",\""
                     + datenow + "\",2," + str(dict_noon['hscj']) + ") ON DUPLICATE KEY UPDATE changeper ="
                     + str(dict_noon['hszf']) + ",closeds = " + str(dict_noon['hsds']) + ",amount = " + str(dict_noon['hscj'])
                     )
    stringsql.append("INSERT INTO ShenzhenIndex (changeper,closeds,date,type,amount) VALUES ("
                     + str(dict_noon['szczzf']) + "," + str(dict_noon['szczds']) + ",\""
                     + datenow + "\",2," + str(dict_noon['szczcj']) +") ON DUPLICATE KEY UPDATE changeper ="
                     + str(dict_noon['szczzf']) + ",closeds = " + str(dict_noon['szczds']) + ",amount = " + str(dict_noon['szczcj'])
                     )
    stringsql.append("INSERT INTO CYSection (changeper,closeds,date,type,amount) VALUES ("
                     + str(dict_noon['cybzf']) + "," + str(dict_noon['cybds']) + ",\""
                     + datenow + "\",2," + str(dict_noon['cybcj']) + ") ON DUPLICATE KEY UPDATE changeper ="
                     + str(dict_noon['cybzf']) + ",closeds = " + str(dict_noon['cybds']) + ",amount = " + str(dict_noon['cybcj'])
                     )
    for i in range(0,len(stringsql)):
        cur.execute(stringsql[i])
    conn.commit()
    cur.close
    conn.close()
