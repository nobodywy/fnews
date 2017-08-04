#!/home/wangy/anaconda3/bin/python
#获取每个公司的所属板块，行业信息，每周运行一次即可
import pymysql
import datetime
import tushare as ts
import time

def run():
    # 获取时间
    now = datetime.datetime.now()
    year = int(now.strftime('%Y'), 10)
    day = int(now.strftime('%d'), 10)
    month = int(now.strftime('%m'), 10)
    datenow = now.strftime('%Y-%m-%d')  # 年月日
    last_season = int((month - 1) / 3)


    #获取沪深、创业板、中小板股票代码以及名称
    dfbf = ts.get_stock_basics()
    df = dfbf[['name','industry']]  #备份数据
    df.loc[:,'section'] = 'null'


    for index in df.index:
        code = int(index)
        if (code>=600000)and(code<=603999):
            df.loc[index]['section'] = 'hs'
        elif (code>=1)and(code<=1999):
            df.loc[index]['section'] = 'ss'
        elif (code>=2001)and(code<=2999):
            df.loc[index]['section'] = 'zx'
        elif (code>=300001)and(code<=300999):
            df.loc[index]['section'] = 'cy'

    #cont = ts.get_concept_classified()

    dfb = ts.get_profit_data(year,last_season)
    dfc = ts.get_growth_data(year,last_season)

    dfbf = dfbf.fillna(-1000)
    dfb = dfb.fillna(-1000)
    dfc = dfc.fillna(-1000)

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
    #"INSERT INTO Category VALUES (code,'name','section','industry')  ON DUPLICATE KEY UPDATE name = 'name',section = 'section,industry = ' "
    for index in df.index:
        #code = int(index)
        company_name = df.loc[index]['name']
        section = df.loc[index]['section']
        industry = df.loc[index]['industry']

        timetomarket = dfbf.loc[index]['timeToMarket']
        d = str(timetomarket)
        try:
            t = time.strptime(d, "%Y%m%d")
            timetomarket = str(t[0]) + '-' + str(t[1]).zfill(2) + "-" + str(t[2])
        except Exception as e:
            timetomarket = '0000-00-00'

        area = dfbf.loc[index]['area']
        totals = dfbf.loc[index]['totals']
        outstanding = dfbf.loc[index]['outstanding']
        totalsassets = dfbf.loc[index]['totalAssets']
        fixedassets = dfbf.loc[index]['fixedAssets']
        liquidassets = dfbf.loc[index]['liquidAssets']
        holders = dfbf.loc[index]['holders']

        try:
            indexb = dfb[dfb.code == index].index[0]
            lsincome = dfb.loc[indexb]['business_income']
            lsnetprofits = dfb.loc[indexb]['net_profits']
            lsesp = dfb.loc[indexb]['eps']
        except Exception as e:
            lsincome = -1000 #-1000代表该数据不存在
            lsnetprofits = -1000
            lsesp = -1000

        try:
            indexc = dfc[dfc.code == index].index[0]
            lsmbrg = dfc.loc[indexc]['mbrg']
            lsnprg = dfc.loc[indexc]['nprg']
            lstarg = dfc.loc[indexc]['targ']
            lsnav = dfc.loc[indexc]['nav']
        except Exception as e:
            lsmbrg = -1000
            lsnprg = -1000
            lstarg = -1000
            lsnav = -1000

        stringsql.append("INSERT INTO Category " +
                         "(company_code,company_name,area,section,industry,totals,outstanding,totalassets,fixedassets,liquidassets,holders,lsincome,lsnetprofits,lsesp,lsmbrg,lsnprg,lstarg,lsnav,time2market) "+
                         "VALUES (\'" + index + "\',\'" + company_name + "\',\'" +
                         area + "\',\'" + section + "\',\'" + industry + "\'," + str(totals) +
                         "," + str(outstanding) + "," + str(totalsassets) + "," + str(fixedassets) + "," +
                         str(liquidassets) + "," + str(holders) + "," + str(lsincome) +
                         "," + str(lsnetprofits) + "," + str(lsesp) + "," + str(lsmbrg) + "," +
                         str(lsnprg) + "," + str(lstarg) + "," + str(lsnav) + ",\'" + str(timetomarket) + "\') ON DUPLICATE KEY UPDATE company_name = \'" +
                         company_name + "\',section = \'" + section + "\',area = \'" + area + "\',industry = \'" + industry +
                         "\',totals = " + str(totals) + ",outstanding = " + str(outstanding) + ",totalassets = " +
                         str(totalsassets) + ",fixedassets = " + str(fixedassets) + ",liquidassets = " +
                         str(liquidassets) + ",holders = " + str(holders) + ",lsincome = " + str(lsincome) +
                         ",lsnetprofits = " + str(lsnetprofits) + ",lsesp = " + str(lsesp) + ",lsmbrg = " +
                         str(lsmbrg) + ",lsnprg = " + str(lsnprg) + ",lstarg = " + str(lstarg) + ",lsnav = " +
                         str(lsnav) + ",time2market = \'" + timetomarket + "\'"
                         )
    for i in range(0,len(stringsql)):
        cur.execute(stringsql[i])
    conn.commit()
    cur.close
    conn.close()
