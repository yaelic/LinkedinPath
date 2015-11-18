__author__ = 'yaelcohen'

import simplejson as json

from crunchBase import crunchbase


c = crunchbase("m5e4brk7xfyajfpcz5ztyyfv")

def getComapnyInfo(companyName):
    companyInfo ={}
    response, response_dic = c.getCompanyData(companyName)
    if (response_dic.has_key('category_code')):
        companyInfo["category"] = response_dic['category_code']
    if (response_dic.has_key('number_of_employees')):
        companyInfo["number_of_employees"] = response_dic['number_of_employees']
    if (response_dic.has_key('founded_year')):
        companyInfo["founded_year"] = response_dic['founded_year']
    if (response_dic.has_key('total_money_raised')):
        try:
            companyInfo["total_money_raised"] = response_dic['total_money_raised'].encode("ascii")
        except:
            companyInfo["total_money_raised"] = response_dic['total_money_raised']
    if (response_dic.has_key('ipo')):
        if response_dic['ipo']!= None:
            companyInfo["is_public"] = True
            if (response_dic["ipo"].has_key("valuation_amount")):
                companyInfo["valuation_amount"] = response_dic['ipo']["valuation_amount"]
            if (response_dic["ipo"].has_key("pub_year")):
                companyInfo["public_year"] = response_dic['ipo']["pub_year"]
        else:
            companyInfo["is_public"] = False
    if not response_dic.has_key('ipo'):
        companyInfo["is_public"] = False
    if (response_dic.has_key('acquisition')):
        if response_dic['acquisition']!= None:
            companyInfo["is_acquired"] = True
            if (response_dic['acquisition'].has_key('price_amount')):
                    companyInfo["acquisition_price"] = response_dic['acquisition']['price_amount']
        else:
            companyInfo["is_acquired"] = False
    if not response_dic.has_key('acquisition'):
        companyInfo["is_acquired"] = False

    return companyInfo

#cInfo = getComapnyInfo("smore")
#print cInfo


