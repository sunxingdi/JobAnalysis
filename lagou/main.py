#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys,os,re

from https import Https
from parse import Parse
from config import headers as hd
import logging
import pymysql
import time

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s Process%(process)d:%(thread)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='diary.log',
                    filemode='a')

def processInfo(info, para):
    """
    信息存储
    """
    logging.error('Process start')
    try:
        conn = pymysql.connect(host='localhost', user=r'root', passwd=r'root', db='lagoujob')  # 连接数据库

        if not conn:
            logging.error('Databases connect error')
            return None
        #获取游标
        cursor = conn.cursor()

        #每次执行获取的数据放到一张表中，表以时间命名
        tablename = "lagoujob" \
                    + str(time.localtime().tm_year) \
                    + str(time.localtime().tm_mon) \
                    + str(time.localtime().tm_mday)
                    #+ str(time.localtime().tm_hour)
                    #+ str(time.localtime().tm_min) \
                    #+ str(time.localtime().tm_sec)
        #print 'create table:', tablename

        SQL = "CREATE TABLE IF NOT EXISTS " \
                        + tablename \
                        + "(Id INT PRIMARY KEY AUTO_INCREMENT," \
                        + "companyFullName     VARCHAR(100)," \
                        + "positionName        VARCHAR(100)," \
                        + "education           VARCHAR(100)," \
                        + "city                VARCHAR(100)," \
                        + "createTime          VARCHAR(100)," \
                        + "salary              VARCHAR(100)," \
                        + "salarymin           VARCHAR(100)," \
                        + "salarymax           VARCHAR(100)," \
                        + "industryField       VARCHAR(100)," \
                        + "district            VARCHAR(100)," \
                        + "positionAdvantage   VARCHAR(100)," \
                        + "companySize         VARCHAR(100)," \
                        + "jobNature           VARCHAR(100)," \
                        + "workYear            VARCHAR(100)," \
                        + "firstType           VARCHAR(100)," \
                        + "secondType          VARCHAR(100)," \
                        + "stationname         VARCHAR(100)," \
                        + "subwayline          VARCHAR(100))"

        #print "SQL:",SQL

        #创建表单
        cursor.execute(SQL)

        ColumnNameList = r"companyFullName,positionName,education,city,createTime," \
                       + r"salary,salarymin,salarymax,industryField,district,positionAdvantage," \
                       + r"companySize,jobNature,workYear,firstType,secondType,stationname,subwayline"

        #print 'info',info

        for job in info:
            # 将salary字段分解为最大值和最小值存储，便于分析

            print 'salary:',str(job['salary'])

            if '-' in str(job['salary']):
                print 'find-'
                salarymin = str(job['salary']).split('-')[0]
                salarymax = str(job['salary']).split('-')[1]
            else:
                salarymin = str(job['salary'])
                salarymax = ''
            #print 'salarymin:',salarymin
            #print 'salarymax:',salarymax

            SQL = "INSERT INTO " + tablename + "(" + ColumnNameList + ") VALUE (" \
                            + "'"   + str(job['companyFullName']) \
                            + "','" + str(job['positionName']) \
                            + "','" + str(job['education']) \
                            + "','" + str(job['city']) \
                            + "','" + str(job['createTime']) \
                            + "','" + str(job['salary']) \
                            + "','" + str(salarymin) \
                            + "','" + str(salarymax) \
                            + "','" + str(job['industryField']) \
                            + "','" + str(job['district']) \
                            + "','" + str(job['positionAdvantage']) \
                            + "','" + str(job['companySize']) \
                            + "','" + str(job['jobNature']) \
                            + "','" + str(job['workYear']) \
                            + "','" + str(job['firstType']) \
                            + "','" + str(job['secondType']) \
                            + "','" + str(job['stationname']) \
                            + "','" + str(job['subwayline']) \
                            + "'"   + ")"
            #print "SQL:", SQL
            cursor.execute(SQL)

        # 提交，不然无法保存新建或者修改的数据
        conn.commit()

        # 关闭游标
        cursor.close()

        # 关闭连接
        conn.close()

        return True

    except Exception, e:
        logging.error('Process except')
        print 'str(Exception):\t', str(Exception)
        print 'str(e):\t\t', str(e)
        print 'repr(e):\t', repr(e)
        print 'e.message:\t', e.message
        return None

def getInfo(url, para):
    """
    获取信息
    """
    generalHttps = Https()
    htmlCode = generalHttps.post(url, para=para, headers=hd)
    #print htmlCode
    generalParse = Parse(htmlCode)
    pageCount = generalParse.parsePage()

    info = []
    for i in range(1, pageCount+1):
        print('第%s页开始爬取' % i)
        para['pn'] = str(i)
        htmlCode = generalHttps.post(url, para=para, headers=hd)
        generalParse = Parse(htmlCode)
        info = getInfoDetail(generalParse)
        if info:
            flag = processInfo(info, para)
            if flag is None:
                print('存储异常')
                return None
            print('第%s页存储完成' % i)
        else:
            print('第%s页内容为空，不存储' % i)
        time.sleep(2)
    return flag

def getInfoDetail(generalParse):
    """
    信息解析
    """
    info = generalParse.parseInfo()
    return info

def main(url, para):
    """
    主函数逻辑
    """
    logging.error('Main start')
    if url:
        flag = getInfo(url, para)             # 获取信息
        return flag
    else:
        return None

if __name__ == '__main__':
    print '启动时间：',time.asctime( time.localtime(time.time()) )
    kdList = [u'']
    cityList = [u'成都']
    url = 'https://www.lagou.com/jobs/positionAjax.json'
    for city in cityList:
        print('爬取%s' % city)
        para = {'first': 'true','pn': '1', 'kd': kdList[0], 'city': city}
        flag = main(url, para)
        if flag: print('%s爬取成功' % city)
        else: print('%s爬取失败' % city)
    print '结束时间：', time.asctime( time.localtime(time.time()) )