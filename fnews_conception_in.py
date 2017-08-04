#!/home/wangy/anaconda3/bin/python
import tushare as ts
import pymysql

def run():
    df = ts.get_concept_classified()
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
    cur.execute("DELETE FROM Conception")
    conn.commit()
    stringsql = []
    for i in range(0,len(df)):
        code = str(df.loc[df.index[i]][0])
        conception = str(df.loc[df.index[i]][2])
        stringsql.append("INSERT INTO Conception VALUES ( \'" + code + "\',\'" + conception + "\')")
    for i in range(0,len(stringsql)):
        cur.execute(stringsql[i])
    conn.commit()
    cur.close
    conn.close()
