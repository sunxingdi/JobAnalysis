#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import demjson

class Parse:
    '''
    解析网页信息
    '''
    def __init__(self, htmlCode):
        self.htmlCode = htmlCode
        try:
            self.json = demjson.decode(htmlCode)
        except:
            print r"[ERROR]demjson.JSONDecodeError"
        pass

    def parseTool(self,content):
        '''
        清除html标签
        '''
        if type(content) != str: return content
        sublist = ['<p.*?>','</p.*?>','<b.*?>','</b.*?>','<div.*?>','</div.*?>',
                   '</br>','<br />','<ul>','</ul>','<li>','</li>','<strong>',
                   '</strong>','<table.*?>','<tr.*?>','</tr>','<td.*?>','</td>',
                   '\r','\n','&.*?;','&','#.*?;','<em>','</em>']
        try:
            for substring in [re.compile(string, re.S) for string in sublist]:
                content = re.sub(substring, "", content).strip()
        except:
            raise Exception('Error '+str(substring.pattern))
        return content

    def parsePage(self):
        '''
        解析并计算页面数量
        :return: 页面数量
        '''
        totalCount = self.json['content']['positionResult']['totalCount']      #职位总数量
        resultSize = self.json['content']['positionResult']['resultSize']      #每一页显示的数量
        pageCount = int(totalCount) // int(resultSize) + 1          #页面数量
        return pageCount

    def parseInfo(self):
        '''
        解析信息
        '''
        info = []
        for position in self.json['content']['positionResult']['result']:
            i = {}
            i['positionName']       = position['positionName']
            i['education']          = position['education']
            i['city']               = position['city']
            i['createTime']         = position['createTime']
            i['salary']             = position['salary']
            i['industryField']      = position['industryField']
            i['district']           = position['district']
            i['positionAdvantage']  = position['positionAdvantage']
            i['companySize']        = position['companySize']
            i['jobNature']          = position['jobNature']
            i['workYear']           = position['workYear']
            i['companyFullName']    = position['companyFullName']
            i['firstType']          = position['firstType']
            i['secondType']         = position['secondType']
            i['stationname']        = position['stationname']
            i['subwayline']         = position['subwayline']
            info.append(i)
        return info