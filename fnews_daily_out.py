# !/home/wangy/anaconda3/bin/python
import datetime
import pymysql
import pandas
import os

dict_time = {}

currentDir = os.path.dirname(__file__)
join_path = lambda p: os.path.join(currentDir, p)

from my_config import MyConfig
mycfg = MyConfig("service")
service_host = mycfg.get('service_host')
service_port = int(mycfg.get('service_port'))
service_user = mycfg.get('service_user')
service_passwd = mycfg.get('service_passwd')
service_db = mycfg.get('service_db')
service_charset = mycfg.get('service_charset')
#conn = pymysql.connect(host=service_host, port=service_port, user=service_user, passwd=service_passwd, db=service_db,charset=service_charset)
def date(d):
    # 获取时间
    now = datetime.datetime.strptime(d,'%Y-%m-%d')
    year = int(now.strftime('%Y'), 10)
    day = int(now.strftime('%d'), 10)
    month = int(now.strftime('%m'), 10)
    last_season = int((month - 1) / 3)
    dict_time['day'] = day
    dict_time['month'] = month
    dict_time['year'] = year
    dict_time['date'] = d
    if now.weekday() == 0 :  #当周一时，上一交易日为上周五
        ysterday = (now - datetime.timedelta(days=3)).strftime('%Y-%m-%d')
    else:
        ysterday = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    dict_time['yesterday'] = str(ysterday)

def mor_out():
    #连接数据库
    conn = pymysql.connect(host=service_host, port=service_port, user=service_user, passwd=service_passwd,
                           db=service_db, charset=service_charset)
    cur = conn.cursor()
    stringsql = []
    stringsql.append("SELECT changeper,opends FROM ShanghaiIndex WHERE date = \'" + dict_time['date'] + "\' and type = 1")
    stringsql.append("SELECT changeper,opends FROM ShenzhenIndex WHERE date = \'" + dict_time['date'] + "\' and type = 1")
    stringsql.append("SELECT changeper,opends FROM CYSection WHERE date = \'" + dict_time['date'] + "\' and type = 1")
    result = ()
    for i in range(0,len(stringsql)):
        cur.execute(stringsql[i])
        result = result + cur.fetchall()
    conn.commit()
    cur.close
    conn.close()


    #处理从sql中读出的数据
    tmp_num = [0,0,0]
    string = [0,0,0]
    for i in range(0,3):
        tmp_num[i] = result[i][0]
        if tmp_num[i] <= 0:
            string[i] = '跌幅'+ str(abs(tmp_num[i]))
        else:
            string[i] = '涨幅'+ str(tmp_num[i])

    dict_mor = {}
    dict_mor['hszf'] = string[0] #沪市涨幅
    dict_mor['hsds'] = result[0][1] #沪市点数
    dict_mor['szczzf'] = string[1] #深圳成指涨幅
    dict_mor['szczds'] = result[1][1] #深圳成指点数
    dict_mor['cybzf'] = string[2] #创业板涨幅
    dict_mor['cybds'] = result[2][1] #创业板点数

    datalist = []
    datalist.append(dict_time)
    datalist.append(dict_mor)

    #读文本，整合文章
    f = open('fnews_mor.txt','r')
    result_file = open('result_news.txt','w+')
    news = ''
    for line in f.readlines():
        line  = line.strip('\n')
        if line[0] == '{':
            gap_index = line.index(':')
            inta = int(line[1:gap_index])
            strb = line[gap_index+1:]
            print(datalist[inta][strb],end='')
            news = news + str(datalist[inta][strb])
            result_file.write(str(datalist[inta][strb]))
        elif line[0] == '#':
            print('\n',end='')
            news = news + '\n'
        else:
            line = line.strip('\n')
            print(line,end='')
            news  = news +  line
            result_file.write(line)
    f.close()
    result_file.close()
    return news

def noon_out():
    # 连接数据库
    conn = pymysql.connect(host=service_host, port=service_port, user=service_user, passwd=service_passwd,
                           db=service_db, charset=service_charset)
    cur = conn.cursor()
    stringsql = []
    stringsql.append("SELECT changeper,closeds,amount FROM ShanghaiIndex WHERE date = \'" + dict_time['date'] + "\' and type = 2")
    stringsql.append("SELECT changeper,closeds,amount FROM ShenzhenIndex WHERE date = \'" + dict_time['date'] + "\' and type = 2")
    stringsql.append("SELECT changeper,closeds,amount FROM CYSection WHERE date = \'" + dict_time['date'] + "\' and type = 2")
    result = ()
    for i in range(0, len(stringsql)):
        cur.execute(stringsql[i])
        result = result + cur.fetchall()
    conn.commit()
    cur.close
    conn.close()

    # 从result中读取数据z
    tmp_num = [0, 0, 0]
    string = [0, 0, 0]
    for i in range(0, 3):
        tmp_num[i] = result[i][0]
        if tmp_num[i] <= 0:
            string[i] = '跌幅' + str(abs(tmp_num[i]))
        else:
            string[i] = '涨幅' + str(tmp_num[i])

    dict_noon = {}
    dict_noon['hszf'] = string[0]  # 沪市涨幅
    dict_noon['hsds'] = result[0][1]  # 沪市点数
    dict_noon['hscj'] = result[0][2]  # 沪市成交
    dict_noon['szczzf'] = string[1]  # 深圳成指涨幅
    dict_noon['szczds'] = result[1][1]  # 深圳成指点数
    dict_noon['szczcj'] = result[1][2]  # 深圳成指成交
    dict_noon['cybzf'] = string[2]  # 创业板涨幅
    dict_noon['cybds'] = result[2][1]  # 创业板点数
    dict_noon['cybcj'] = result[2][2]  # c创业板成交

    # 将数据依次存入list
    datalist = []
    datalist.append(dict_time)
    datalist.append(dict_noon)

    # 读文本，整合文章
    f = open('fnews_noon.txt', 'r')
    result_file = open('result_news.txt', 'w+')
    news = ''
    for line in f.readlines():
        line = line.strip('\n')
        if line[0] == '{':
            gap_index = line.index(':')
            inta = int(line[1:gap_index])
            strb = line[gap_index + 1:]
            print(datalist[inta][strb], end='')
            news = news + str(datalist[inta][strb])
            result_file.write(str(datalist[inta][strb]))
        elif line[0] == '#':
            print('\n', end='')
            news = news + '\n'
        else:
            line = line.strip('\n')
            print(line, end='')
            news = news + line
            result_file.write(line)
    f.close()
    result_file.close()
    return news


def afternoon_out():
    # 连接数据库
    conn = pymysql.connect(host=service_host, port=service_port, user=service_user, passwd=service_passwd,
                           db=service_db, charset=service_charset)
    cur = conn.cursor()
    stringsql = []
    stringsql.append("SELECT changeper,closeds,amount FROM ShanghaiIndex WHERE date = \'" + dict_time['date'] + "\' and type = 3")
    stringsql.append("SELECT changeper,closeds,amount FROM ShenzhenIndex WHERE date = \'" + dict_time['date'] + "\' and type = 3")
    stringsql.append("SELECT changeper,closeds,amount FROM ZXSection WHERE date = \'" + dict_time['date'] + "\' and type = 3")
    stringsql.append("SELECT changeper,closeds,amount FROM CYSection WHERE date = \'" + dict_time['date'] + "\' and type = 3")
    result = ()
    for i in range(0, len(stringsql)):
        cur.execute(stringsql[i])
        result = result + cur.fetchall()
    conn.commit()
    cur.close
    conn.close()

    tmp_num = [0, 0, 0, 0]
    string = [0, 0, 0, 0]
    for i in range(0, 4):
        tmp_num[i] = result[i][0]
        if tmp_num[i] <= 0:
            string[i] = '跌幅' + str(abs(tmp_num[i]))
        else:
            string[i] = '涨幅' + str(tmp_num[i])

    dict_afnoon = {}
    dict_afnoon['hszf'] = string[0]  # 沪市涨幅
    dict_afnoon['hsds'] = result[0][1]  # 沪市点数
    a = result[0][2]
    dict_afnoon['hscj'] = a  # 沪市成交
    dict_afnoon['szczzf'] = string[1]  # 深圳成指涨幅
    dict_afnoon['szczds'] = result[1][1]  # 深圳成指点数
    b = result[1][2]
    dict_afnoon['szczcj'] = b  # 深圳成指成交
    dict_afnoon['hscjzh'] = round(a + b, 2)  # 沪深两市总成交

    dict_afnoon['zxbzf'] = string[2]  # 中小板涨幅
    dict_afnoon['zxbds'] = result[2][1]  # 中小板点数
    dict_afnoon['cybzf'] = string[3]  # 创业板涨幅
    dict_afnoon['cybds'] = result[3][1]  # 创业板点数

    # 将数据依次存入list
    datalist = []
    datalist.append(dict_time)
    datalist.append(dict_afnoon)


    # 读文本，整合文章
    f = open('fnews_afternoon.txt', 'r')
    result_file = open('result_news.txt', 'w+')
    news = ''
    for line in f.readlines():
        line = line.strip('\n')
        if line[0] == '{':
            gap_index = line.index(':')
            inta = int(line[1:gap_index])
            strb = line[gap_index + 1:]
            print(datalist[inta][strb], end='')
            news = news + str(datalist[inta][strb])
            result_file.write(str(datalist[inta][strb]))
        elif line[0] == '#':
            print('\n', end='')
            news = news + '\n'
        else:
            line = line.strip('\n')
            print(line, end='')
            news = news + line
            result_file.write(line)
    f.close()
    result_file.close()
    return news

def company_amount_out():
    # 连接数据库
    conn = pymysql.connect(host=service_host, port=service_port, user=service_user, passwd=service_passwd,
                           db=service_db, charset=service_charset)
    cur = conn.cursor()
    stringsql = []
    #SELECT * FROM Company where (date = '2017-07-21')AND(section = 'ss' OR section = 'hs') ORDER BY amount DESC LIMIT 0,3
    stringsql.append("SELECT company_name,company_code,amount FROM Company where (date = \'" + dict_time['date'] + "\')AND(section = \'ss\' OR section =  \'hs\') ORDER BY amount DESC LIMIT 0,3"  )
    stringsql.append("SELECT company_name,company_code,amount FROM Company where (date = \'" + dict_time['date'] + "\')AND(section = \'zx\' ) ORDER BY amount DESC LIMIT 0,3")  #中小板
    stringsql.append("SELECT company_name,company_code,amount FROM Company where (date = \'" + dict_time['date'] + "\')AND(section = \'cy\') ORDER BY amount DESC LIMIT 0,3")   # 创业板
    result = ()
    for i in range(0, len(stringsql)):
        cur.execute(stringsql[i])
        result = result + cur.fetchall()
    conn.commit()
    cur.close
    conn.close()

    # 从result中读取数据z
    dict_company_amount = {}
    #  沪深股市成交前三数据
    dict_company_amount['hs_01_name'] = result[0][0]
    dict_company_amount['hs_01_code'] = result[0][1]
    dict_company_amount['hs_01_amount'] = result[0][2]
    dict_company_amount['hs_02_name'] = result[1][0]
    dict_company_amount['hs_02_code'] = result[1][1]
    dict_company_amount['hs_02_amount'] = result[1][2]
    dict_company_amount['hs_03_name'] = result[2][0]
    dict_company_amount['hs_03_code'] = result[2][1]
    dict_company_amount['hs_03_amount'] = result[2][2]

    #  中小板成交前三数据
    dict_company_amount['zx_01_name'] = result[3][0]
    dict_company_amount['zx_01_code'] = result[3][1]
    dict_company_amount['zx_01_amount'] = result[3][2]
    dict_company_amount['zx_02_name'] = result[4][0]
    dict_company_amount['zx_02_code'] = result[4][1]
    dict_company_amount['zx_02_amount'] = result[4][2]
    dict_company_amount['zx_03_name'] = result[5][0]
    dict_company_amount['zx_03_code'] = result[5][1]
    dict_company_amount['zx_03_amount'] = result[5][2]

    #  创业板成交前三数据
    dict_company_amount['cy_01_name'] = result[6][0]
    dict_company_amount['cy_01_code'] = result[6][1]
    dict_company_amount['cy_01_amount'] = result[6][2]
    dict_company_amount['cy_02_name'] = result[7][0]
    dict_company_amount['cy_02_code'] = result[7][1]
    dict_company_amount['cy_02_amount'] = result[7][2]
    dict_company_amount['cy_03_name'] = result[8][0]
    dict_company_amount['cy_03_code'] = result[8][1]
    dict_company_amount['cy_03_amount'] = result[8][2]

    # 将数据依次存入list
    datalist = []
    datalist.append(dict_time)
    datalist.append(dict_company_amount)

    # 读文本，整合文章
    f = open('fnews_company.txt', 'r')
    result_file = open('result_news.txt', 'w+')
    news = ''
    for line in f.readlines():
        line = line.strip('\n')
        if line[0] == '{':
            gap_index = line.index(':')
            inta = int(line[1:gap_index])
            strb = line[gap_index + 1:]
            print(datalist[inta][strb], end='')
            news = news + str(datalist[inta][strb])
            result_file.write(str(datalist[inta][strb]))
        elif line[0] == '#':
            print('\n', end='')
            news = news + '\n'
        else:
            line = line.strip('\n')
            print(line, end='')
            news = news + line
            result_file.write(line)
    f.close()
    result_file.close()
    return news

def industry_out():
    # 连接数据库
    conn = pymysql.connect(host=service_host, port=service_port, user=service_user, passwd=service_passwd,
                           db=service_db, charset=service_charset)
    cur = conn.cursor()
    stringsql = []
    # SELECT DISTINCT industry FROM Category
    stringsql.append("SELECT DISTINCT industry FROM Category ")
    result = ()
    for i in range(0, len(stringsql)):
        cur.execute(stringsql[i])
        result = result + cur.fetchall()

    # 从result中读取数据
    df = pandas.DataFrame(columns=['name', 'rate'])
    for i in range(0, result.__len__()):
        str_industry = str(result[i])
        str_industry = str_industry.strip(')')
        str_industry = str_industry.strip('(')
        str_industry = str_industry.strip(',')
        str_industry = str_industry.strip('\'')
        result_nmc = ()
        t_nmc = 0.0
        y_nmc = 0.0
        strsql = (
        "SELECT nmc FROM Company ,Category WHERE Company.company_code = Category.company_code AND Category.industry = \'" +
        str_industry + "\' AND Company.date = \'" + dict_time['date'] + "\'")
        cur.execute(strsql)
        result_nmc = cur.fetchall()
        for j in range(0, result_nmc.__len__()):
            float_nmc = str(result_nmc[j]).strip(')')
            float_nmc = float_nmc.strip('(')
            float_nmc = float_nmc.strip(',')
            float_nmc = float(float_nmc)
            t_nmc = t_nmc + float_nmc
        strsql = (
        "SELECT nmc FROM Company ,Category WHERE Company.company_code = Category.company_code AND Category.industry = \'" +
        str_industry + "\' AND Company.date = \'" + dict_time['yesterday'] + "\'")
        cur.execute(strsql)
        result_nmc = cur.fetchall()
        for j in range(0, result_nmc.__len__()):
            float_nmc = str(result_nmc[j]).strip(')')
            float_nmc = float_nmc.strip('(')
            float_nmc = float_nmc.strip(',')
            float_nmc = float(float_nmc)
            y_nmc = y_nmc + float_nmc
        rate = (t_nmc - y_nmc) / y_nmc
        df.loc[i] = [str_industry, rate]
    df = df.sort_values(by=['rate'], ascending=[0])
    cur.close
    conn.close()

    dict_industry = {}
    df_len = len(df)
    dict_industry['p_01_name'] = str(df.loc[df.index[0]]['name'])  # positive 涨幅  negative  跌幅
    dict_industry['p_02_name'] = str(df.loc[df.index[1]]['name'])
    dict_industry['p_03_name'] = str(df.loc[df.index[2]]['name'])
    dict_industry['p_04_name'] = str(df.loc[df.index[3]]['name'])
    dict_industry['p_05_name'] = str(df.loc[df.index[4]]['name'])
    dict_industry['n_01_name'] = str(df.loc[df_len - 1]['name'])  # positive 涨幅  negative  跌幅
    dict_industry['n_02_name'] = str(df.loc[df_len - 2]['name'])
    dict_industry['n_03_name'] = str(df.loc[df_len - 3]['name'])
    dict_industry['n_04_name'] = str(df.loc[df_len - 4]['name'])
    dict_industry['n_05_name'] = str(df.loc[df_len - 5]['name'])
    # 将数据依次存入list
    datalist = []
    datalist.append(dict_time)
    datalist.append(dict_industry)

    # 读文本，整合文章
    f = open(join_path(os.path.join('marketIndustry', 'fnews_industry_B.txt')), 'r')
    result_file = open('result_news.txt', 'w+')
    news = ''
    for line in f.readlines():
        line = line.strip('\n')
        if line[0] == '{':
            gap_index = line.index(':')
            inta = int(line[1:gap_index])
            strb = line[gap_index + 1:]
            print(datalist[inta][strb], end='')
            news = news + str(datalist[inta][strb])
            result_file.write(str(datalist[inta][strb]))
        elif line[0] == '#':
            print('\n', end='')
            news = news + '\n'
        else:
            line = line.strip('\n')
            print(line, end='')
            news = news + line
            result_file.write(line)
    f.close()
    result_file.close()
    return news


def name2code(strl):
    # 连接数据库
    conn = pymysql.connect(host=service_host, port=service_port, user=service_user, passwd=service_passwd,
                           db=service_db, charset=service_charset)
    cur = conn.cursor()
    stringsql = []
    if strl == '':
        #SELECT company_code,company_name FROM Category LIMIT 20
        stringsql.append("SELECT company_name,company_code FROM Category LIMIT 20")
    else :
        #SELECT company_code,company_name FROM Category where (company_name  REGEXP "^深深*")OR (company_code REGEXP "^6039*")
        stringsql.append("SELECT company_name,company_code FROM Category where (company_name  REGEXP \'^" + str(strl) +
                         "*\')OR (company_code REGEXP \'" + str(strl) + "*\')"  )
    result = ()
    for i in range(0, len(stringsql)):
        cur.execute(stringsql[i])
        result = result + cur.fetchall()
    conn.commit()
    cur.close
    conn.close()
    return result

def company_combine_out(company_code):
    # 连接数据库
    conn = pymysql.connect(host=service_host, port=service_port, user=service_user, passwd=service_passwd,
                           db=service_db, charset=service_charset)
    cur = conn.cursor()
    stringsql = []
    # SELECT company_name,section,changeper,openprice,closeprice,high,low,volume,amount,nmc,mktcap,settlement,maxdealtime,maxdealvol,maxdealprice,ma5,ma10,ma20 FROM Company WHERE (company_code = '000001') AND (date = '2017-07-27')
    stringsql.append("SELECT company_name,section,changeper,openprice," +
                     "closeprice,high,low,volume,amount,nmc,mktcap,settlement,maxdealtime,maxdealvol,maxdealprice,ma5,ma10,ma20,turnoverration" +
                     " FROM Company WHERE (company_code = \'" + str(company_code) + "\') AND (date = \'" + dict_time[
                         'date'] +
                     "\')"
                     )
    # SELECT area,time2market,industry,totals,outstanding,totalassets,fixedassets,liquidassets,holders,lsincome,lsnetprofits,lsesp,lsmbrg,lsnprg,lsnav,lstarg FROM Category WHERE company_code = '000001'
    stringsql.append(
        "SELECT area,time2market,industry,totals,outstanding,totalassets,fixedassets,liquidassets,holders" +
        ",lsincome,lsnetprofits,lsesp,lsmbrg,lsnprg,lsnav,lstarg FROM Category WHERE company_code = \'" + str(
            company_code) + "\'")
    result = ()
    for i in range(0, len(stringsql)):
        cur.execute(stringsql[i])
        result = result + cur.fetchall()
    conn.commit()
    tag = result[0][1]
    section = ''
    section_name = ''
    section_code = ''
    if tag == 'ss':
        section = 'ShenzhenIndex'
        section_name = '深圳成指'
        section_code = '399001'
    elif tag == 'hs':
        section = 'ShanghaiIndex'
        section_name = '上证指数'
        section_code = '000001'
    elif tag == 'zx':
        section = 'ZXSection'
        section_name = '中小板'
        section_code = '399005'
    elif tag == 'cy':
        section = 'CYSection'
        section_name = '创业板'
        section_code = '399006'
    # SELECT opends,closeds,high,low,volume,amount FROM ShenzhenIndex WHERE (date = '2017-07-27')AND (type=3)
    strsql = "SELECT opends,closeds,high,low,volume,amount FROM ShenzhenIndex WHERE (date = \'" + dict_time[
        'date'] + "\') AND (type = 3)"
    cur.execute(strsql)
    result = result + cur.fetchall()
    conn.commit()
    cur.close
    conn.close()

    # 数据存入字典
    dict_company = {}
    dict_section = {}
    dict_company['company_name'] = result[0][0]
    dict_company['company_code'] = company_code
    dict_company['settlement'] = result[0][11]
    dict_company['openprice'] = result[0][3]
    dict_company['closeprice'] = result[0][4]
    dict_company['volume'] = result[0][7]
    dict_company['turnoverration'] = result[0][18]
    dict_company['high'] = result[0][5]
    dict_company['low'] = result[0][6]
    dict_company['changeper'] = result[0][2]
    dict_company['mktcap'] = result[0][10] / 10000
    dict_company['nmc'] = result[0][9] / 10000
    dict_company['maxdealtime'] = result[0][12]
    dict_company['maxdealvol'] = result[0][13]
    dict_company['maxdealprice'] = result[0][14]
    dict_company['ma5'] = result[0][15]
    dict_company['ma10'] = result[0][16]
    dict_company['ma20'] = result[0][17]
    dict_company['area'] = result[1][0]
    dict_company['time2market'] = result[1][1]
    dict_company['industry'] = result[1][2]
    dict_company['totals'] = result[1][3]
    dict_company['outstanding'] = result[1][4]
    dict_company['totalassets'] = result[1][5]
    dict_company['fixedassets'] = result[1][6]
    dict_company['liquidassets'] = result[1][7]
    dict_company['holders'] = result[1][8]
    dict_company['income'] = result[1][9]
    dict_company['netprofits'] = result[1][10]
    dict_company['esp'] = result[1][11]
    dict_company['mbrg'] = result[1][12]
    dict_company['nprg'] = result[1][13]
    dict_company['nav'] = result[1][14]
    dict_company['targ'] = result[1][15]

    dict_section['section_name'] = section_name
    dict_section['section_code'] = section_code
    dict_section['opends'] = result[2][0]
    dict_section['closeds'] = result[2][1]
    dict_section['high'] = result[2][2]
    dict_section['low'] = result[2][3]
    dict_section['volume'] = result[2][4]
    dict_section['amount'] = result[2][5]

    # 将数据依次存入list
    datalist = []
    datalist.append(dict_time)
    datalist.append(dict_company)
    datalist.append(dict_section)
    # 读文本，整合文章
    f = open('fnews_company_combine.txt', 'r')
    result_file = open('result_news.txt', 'w+')
    news = ''
    for line in f.readlines():
        line = line.strip('\n')
        if line[0] == '{':
            gap_index = line.index(':')
            inta = int(line[1:gap_index])
            strb = line[gap_index + 1:]
            print(datalist[inta][strb], end='')
            news = news + str(datalist[inta][strb])
            result_file.write(str(datalist[inta][strb]))
        elif line[0] == '#':
            print('\n', end='')
            news = news + '\n'
        else:
            line = line.strip('\n')
            print(line, end='')
            news = news + line
            result_file.write(line)
    f.close()
    result_file.close()
    return news

def marketIndustry_out(type):
    # 连接数据库
    marketname = ['hs','ss','cy','zx']
    tablename = ['ShanghaiIndex','ShenzhenIndex','CYSection','ZXSection']
    conn = pymysql.connect(host=service_host, port=service_port, user=service_user, passwd=service_passwd,
                           db=service_db, charset=service_charset)
    cur = conn.cursor()
    type = int(type)
    if type != 3:
        stringsql = []
        # SELECT DISTINCT industry FROM Category
        stringsql.append("SELECT DISTINCT industry FROM Category WHERE Category.section = \'" + marketname[type] +"\'")
        result = ()
        for i in range(0, len(stringsql)):
            cur.execute(stringsql[i])
            result = result + cur.fetchall()

        # 从result中读取数据
        df = pandas.DataFrame(columns=['name', 'rate'])
        for i in range(0, result.__len__()):
            str_industry = str(result[i])
            str_industry = str_industry.strip(')')
            str_industry = str_industry.strip('(')
            str_industry = str_industry.strip(',')
            str_industry = str_industry.strip('\'')
            result_nmc = ()
            t_nmc = 0.0
            y_nmc = 0.0
            strsql = (
            "SELECT nmc FROM Company ,Category WHERE Company.company_code = Category.company_code AND Category.industry = \'" +
            str_industry + "\' AND Company.date = \'" + dict_time['date'] + "\'")
            cur.execute(strsql)
            result_nmc = cur.fetchall()
            for j in range(0, result_nmc.__len__()):
                float_nmc = str(result_nmc[j]).strip(')')
                float_nmc = float_nmc.strip('(')
                float_nmc = float_nmc.strip(',')
                float_nmc = float(float_nmc)
                t_nmc = t_nmc + float_nmc
            strsql = (
            "SELECT nmc FROM Company ,Category WHERE Company.company_code = Category.company_code AND Category.industry = \'" +
            str_industry + "\' AND Company.date = \'" + dict_time['yesterday'] + "\' AND Category.section = \'" + str(marketname[type]) + "\'")
            cur.execute(strsql)
            result_nmc = cur.fetchall()
            for j in range(0, result_nmc.__len__()):
                float_nmc = str(result_nmc[j]).strip(')')
                float_nmc = float_nmc.strip('(')
                float_nmc = float_nmc.strip(',')
                float_nmc = float(float_nmc)
                y_nmc = y_nmc + float_nmc
            rate = (t_nmc - y_nmc) / y_nmc
            df.loc[i] = [str_industry, rate]
        df = df.sort_values(by=['rate'], ascending=[0])

        #获取该板块总体数据
        result_section = ()
        #SELECT closeds,changeper FROM ShanghaiIndex WHERE date = '2017-08-03' AND type = 3
        strsql = (
            "SELECT closeds,changeper FROM " + str(tablename[type]) + " WHERE date = \'" + dict_time['date'] +
            "\' AND type = 3"
            )
        cur.execute(strsql)
        result_section = cur.fetchall()
        txt_name = marketname[type] + "_"
        if result_section[0][1] > 0:
            txt_name = txt_name + "a.txt"
        else:
            txt_name = txt_name + "b.txt"
        cur.close
        conn.close()

        dict_industry = {}
        dict_industry['ds'] = str(result_section[0][0])
        dict_industry['zf'] = str(abs(float(result_section[0][1])))
        df_len = len(df)
        dict_industry['p_01_name'] = str(df.loc[df.index[0]]['name'])  # positive 涨幅  negative  跌幅
        dict_industry['p_02_name'] = str(df.loc[df.index[1]]['name'])
        dict_industry['p_03_name'] = str(df.loc[df.index[2]]['name'])
        dict_industry['p_04_name'] = str(df.loc[df.index[3]]['name'])
        dict_industry['n_01_name'] = str(df.loc[df_len - 1]['name'])  # positive 涨幅  negative  跌幅
        dict_industry['n_02_name'] = str(df.loc[df_len - 2]['name'])
        dict_industry['n_03_name'] = str(df.loc[df_len - 3]['name'])
    else:
        stringsql = []
        #SELECT * FROM ZXSection WHERE date = '2017-08-03' AND type =3
        stringsql.append("SELECT opends,closeds,changeper,amount FROM ZXSection WHERE date = \'"  + dict_time['date']
                        + "\' AND type = 3 "
                         )
        stringsql.append("SELECT amount FROM ZXSection WHERE date = \'" + dict_time['yesterday']
                         + "\' AND type = 3 "
                         )
        result = ()
        for i in range(0, len(stringsql)):
            cur.execute(stringsql[i])
            result = result + cur.fetchall()

        # 获取该板块涨幅前五的股票数据
        result_company = ()
        # SELECT company_name,company_code FROM Company WHERE (date='2017-08-03')AND(section = 'zx') ORDER BY changeper DESC LIMIT 5
        strsql = (
            "SELECT company_name,company_code FROM Company WHERE (date=\'" +
            dict_time['date'] + "\')AND(section = 'zx') ORDER BY changeper DESC LIMIT 5"
        )
        cur.execute(strsql)
        result_company = cur.fetchall()
        txt_name = 'zxb.txt'
        cur.close
        conn.close()

        dict_industry = {}
        dict_industry['zxb_closeds'] = str(result[0][1])
        dict_industry['zxb_opends'] = str(result[0][0])
        if result[0][2] > 0:
            dict_industry['zxbzf'] = "涨幅为"+str(abs(result[0][2]))
        else:
            dict_industry['zxbzf'] = "跌幅为" + str(abs(result[0][2]))
        dict_industry['zxb_amount']  = str(result[0][3])
        changenum = round(result[0][3]-result[1][0],2)
        if changenum>0:
            dict_industry['zxb_change'] = '增加'
        else:
            dict_industry['zxb_change'] = '减少'
        dict_industry['zxb_amount_change'] = str(abs(changenum))

        dict_industry['p_01_name'] = result_company[0][0]
        dict_industry['p_01_code'] = result_company[0][1]
        dict_industry['p_02_name'] = result_company[1][0]
        dict_industry['p_02_code'] = result_company[1][1]
        dict_industry['p_03_name'] = result_company[2][0]
        dict_industry['p_03_code'] = result_company[2][1]
        dict_industry['p_04_name'] = result_company[3][0]
        dict_industry['p_04_code'] = result_company[3][1]
        dict_industry['p_05_name'] = result_company[4][0]
        dict_industry['p_05_code'] = result_company[4][1]
    # 将数据依次存入list
    datalist = []
    datalist.append(dict_time)
    datalist.append(dict_industry)

    # 读文本，整合文章
    f = open(join_path(os.path.join('marketIndustry', txt_name)), 'r')
    result_file = open('result_news.txt', 'w+')
    news = ''
    for line in f.readlines():
        line = line.strip('\n')
        if line[0] == '{':
            gap_index = line.index(':')
            inta = int(line[1:gap_index])
            strb = line[gap_index + 1:]
            print(datalist[inta][strb], end='')
            news = news + str(datalist[inta][strb])
            result_file.write(str(datalist[inta][strb]))
        elif line[0] == '#':
            print('\n', end='')
            news = news + '\n'
        else:
            line = line.strip('\n')
            print(line, end='')
            news = news + line
            result_file.write(line)
    f.close()
    result_file.close()
    return news
