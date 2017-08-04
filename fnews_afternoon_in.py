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
    indexlist.append(cont[cont.code == '399005'].index[0])
    indexlist.append(cont[cont.code == '399006'].index[0])


    hsopends = cont.loc[indexlist[0]]['open']
    hscloseds = cont.loc[indexlist[0]]['close']
    hschangeper = cont.loc[indexlist[0]]['change']
    hsamount = cont.loc[indexlist[0]]['amount']
    hsvolume = cont.loc[indexlist[0]]['volume']
    hshigh = cont.loc[indexlist[0]]['high']
    hslow = cont.loc[indexlist[0]]['low']

    ssopends = cont.loc[indexlist[1]]['open']
    sscloseds = cont.loc[indexlist[1]]['close']
    sschangeper = cont.loc[indexlist[1]]['change']
    ssamount = cont.loc[indexlist[1]]['amount']
    ssvolume = cont.loc[indexlist[1]]['volume']
    sshigh = cont.loc[indexlist[1]]['high']
    sslow = cont.loc[indexlist[1]]['low']

    zxopends = cont.loc[indexlist[2]]['open']
    zxcloseds = cont.loc[indexlist[2]]['close']
    zxchangeper = cont.loc[indexlist[2]]['change']
    zxamount = cont.loc[indexlist[2]]['amount']
    zxvolume = cont.loc[indexlist[2]]['volume']
    zxhigh = cont.loc[indexlist[2]]['high']
    zxlow = cont.loc[indexlist[2]]['low']

    cyopends = cont.loc[indexlist[3]]['open']
    cycloseds = cont.loc[indexlist[3]]['close']
    cychangeper = cont.loc[indexlist[3]]['change']
    cyamount = cont.loc[indexlist[3]]['amount']
    cyvolume = cont.loc[indexlist[3]]['volume']
    cyhigh = cont.loc[indexlist[3]]['high']
    cylow = cont.loc[indexlist[3]]['low']


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
    stringsql.append("INSERT INTO ShanghaiIndex VALUES (\'"
                     + datenow + "\',3," + str(hsopends) + ","
                     + str(hscloseds) + "," + str(hschangeper) + "," + str(hsamount) + "," + str(hsvolume) + ","
                     + str(hshigh) + "," + str(hslow) + ") ON DUPLICATE KEY UPDATE  opends = " + str(hsopends) +
                     ",closeds = " + str(hscloseds) + ",changeper = " + str(hschangeper) + ",high = " +
                     str(hshigh) + ",low = " + str(hslow)
                     + ",volume = " + str(hsvolume) + ",amount = " + str(hsamount)
                     )
    stringsql.append("INSERT INTO ShenzhenIndex  VALUES ( \'"
                     + datenow + "\',3," + str(ssopends) + ","
                     + str(sscloseds) + "," + str(sschangeper) + "," + str(ssamount) + "," + str(ssvolume) + ","
                     + str(sshigh) + "," + str(sslow) + ") ON DUPLICATE KEY UPDATE  opends = " + str(ssopends) +
                     ",closeds = " + str(sscloseds) + ",changeper = " + str(sschangeper) + ",high = " +
                     str(sshigh) + ",low = " + str(sslow)
                     + ",volume = " + str(ssvolume) + ",amount = " + str(ssamount)
                     )
    stringsql.append("INSERT INTO ZXSection VALUES (\'"
                     + datenow + "\',3," + str(zxopends) + ","
                     + str(zxcloseds) + "," + str(zxchangeper) + "," + str(zxamount) + "," + str(zxvolume) + ","
                     + str(zxhigh) + "," + str(zxlow) + ") ON DUPLICATE KEY UPDATE  opends = " + str(zxopends) +
                     ",closeds = " + str(zxcloseds) + ",changeper = " + str(zxchangeper) + ",high = " +
                     str(zxhigh) + ",low = " + str(zxlow)
                     + ",volume = " + str(zxvolume) + ",amount = " + str(zxamount)
                     )
    stringsql.append("INSERT INTO CYSection VALUES (\'"
                     + datenow + "\',3," + str(cyopends) + ","
                     + str(cycloseds) + "," + str(cychangeper) + "," + str(cyamount) + "," + str(cyvolume) + ","
                     + str(cyhigh) + "," + str(cylow) + ") ON DUPLICATE KEY UPDATE  opends = " + str(cyopends) +
                     ",closeds = " + str(cycloseds) + ",changeper = " + str(cychangeper) + ",high = " +
                     str(cyhigh) + ",low = " + str(cylow)
                     + ",volume = " + str(cyvolume) + ",amount = " + str(cyamount)
                     )
    for i in range(0,len(stringsql)):
        cur.execute(stringsql[i])
    conn.commit()
    cur.close
    conn.close()
