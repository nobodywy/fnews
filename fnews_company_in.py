# !/home/wangy/anaconda3/bin/python
import pymysql
import datetime
import tushare as ts

def run():
    num = 100000000
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

    df = ts.get_today_all()

    # 连接数据库
    from my_config import MyConfig
    mycfg = MyConfig("service")
    service_host = mycfg.get('service_host')
    service_port = int(mycfg.get('service_port'))
    service_user = mycfg.get('service_user')
    service_passwd = mycfg.get('service_passwd')
    service_db = mycfg.get('service_db')
    service_charset = mycfg.get('service_charset')
    conn = pymysql.connect(host=service_host, port=service_port, user=service_user, passwd=service_passwd,
                           db=service_db, charset=service_charset)
    cur = conn.cursor()
    stringsql = []
    #SELECT company_code,company_name,section from Category
    stringsql.append("SELECT company_code,company_name,section from Category")
    for i in range(0,len(stringsql)):
        cur.execute(stringsql[i])
    conn.commit()
    result = cur.fetchall()
    stringsql = []
    nulm = -1000
    for i in range(0,result.__len__()):
        code = result[i][0]
        print(code)

        settlement = nulm
        openprice = nulm
        close = nulm
        volume = nulm
        turnoverration = nulm
        high = nulm
        low = nulm
        changepercent = nulm
        mktcap = nulm
        nmc = nulm
        maxdealtime = nulm
        maxdealvol = nulm
        maxdealprice = nulm
        ma5 = nulm
        ma10 = nulm
        ma20 = nulm
        amount = nulm

        try:
            df1 = df[df.code == code]
            df1 = df1.fillna(nulm)
            settlement = df1.loc[df1.index[0]]['settlement']
            turnoverration = df1.loc[df1.index[0]]['turnoverratio']
            changepercent = df1.loc[df1.index[0]]['changepercent']
            mktcap = df1.loc[df1.index[0]]['mktcap']
            nmc = df1.loc[df1.index[0]]['nmc']
        except Exception as e:
            print("basic data not find ,code = "+ code)

        try:
            maxdeal = ts.get_sina_dd(code, date=datenow)
            maxdeal = maxdeal.sort_values(by=['volume'], ascending=[0])
            maxdeal = maxdeal.fillna(nulm)
            maxdealtime = maxdeal.loc[maxdeal.index[0]]['time']
            maxdealprice = maxdeal.loc[maxdeal.index[0]]['price']
            maxdealvol = maxdeal.loc[maxdeal.index[0]]['volume']
        except Exception as e:
            print("maxdeal not find,code = "+ code)

        try:
            ma = ts.get_hist_data(code,start=datenow,end = datenow)
            ma = ma.fillna(nulm)
            ma5 =ma.loc[ma.index[0]]['ma5']
            ma10 = ma.loc[ma.index[0]]['ma10']
            ma20 = ma.loc[ma.index[0]]['ma20']
            openprice = ma.loc[ma.index[0]]['open']
            close = ma.loc[ma.index[0]]['close']
            high = ma.loc[ma.index[0]]['high']
            low = ma.loc[ma.index[0]]['low']
            volume = ma.loc[ma.index[0]]['volume']
        except Exception as e:
            print("ma not find ,code = "+code)

        try :
            cont =  ts.get_realtime_quotes(code)
            amount = round(float(cont.loc[0]['amount'])/num,2)
        except  Exception as e:
            print("amount not find,code = "+ code)

        stringsql.append("INSERT INTO Company VALUES (\'" + result[i][0] + "\',\'" + datenow
                         + "\',\'" + result[i][1] + "\',\'" + result[i][2] + "\'," + str(changepercent) + ","
                         + str(openprice) + "," + str(close) + "," +str(high) + "," + str(low) + "," + str(volume) + "," +
                         str(amount) + "," + str(nmc) + "," + str(mktcap) + "," + str(settlement) + ",\'" + str(maxdealtime) +
                         "\'," + str(maxdealvol) + "," + str(maxdealprice) + "," + str(ma5) + "," + str(ma10) + "," + str(ma20) + "," + str(turnoverration)
                         + ") ON DUPLICATE KEY UPDATE  company_name = \'" + result[i][1] + "\',section = \'" + result[i][2] +
                         "\',changeper = " + str(changepercent) + ",openprice = " + str(openprice) + ",closeprice = " + str(close)
                        + ",high = " + str(high) + ",low = " + str(low) + ",volume = " + str(volume) + ",amount = " + str(amount)
                         + ",nmc = " + str(nmc) + ",mktcap = " + str(mktcap) + ",settlement = " + str(settlement) + ",maxdealtime = \'"
                         + str(maxdealtime) + "\',maxdealvol = " + str(maxdealvol) + ",maxdealprice = " +
                         str(maxdealprice) + ",ma5 = " + str(ma5) + ",ma10 = " + str(ma10) + ",ma20 = " + str(ma20) + ",turnoverration = " + str(turnoverration)
                        )
    for i in range(0,len(stringsql)):
        cur.execute(stringsql[i])
    conn.commit()
    cur.close
    conn.close()


   # !/home/wangy/anaconda3/bin/python
