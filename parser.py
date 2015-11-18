__author__ = 'yaelcohen'

from bs4 import BeautifulSoup
import re
import data_enrich


def parseFile(path, firstID):
    f = open(path,"r")
    data = f.read()
    soup = BeautifulSoup(data)
    ## summery = soup.find('p',{'class':'description'}).text ## bit used right now
    all_exp = soup.find('div', {'id':'background-experience'})
    cv = []
    index = 1
    if all_exp is None:
        print "Didn't find content in " , path
        return cv, firstID

    for son in all_exp.children:
        pos = {}

        ## getting the company name
        #if not son.find('hgroup'):
        if not (son.find('header') or son.find('hgroup')):
            continue
        #for h in son.find('hgroup').find_all('h5'):
        if son.find('header'):
            for h in son.find('header').find_all('h5'):
                if h.find('a'):
                    company =  h.find('a').text
                    try:
                        pos['company'] = company.encode("ascii")
                    except:
                        pos['company'] = company
                    #print pos['company']
                    try:
                        cInfo = data_enrich.getComapnyInfo(pos['company'])
                        pos.update(cInfo)
                    except:
                        pos['company']
                else:
                    continue;

        if son.find('hgroup'):
            for h in son.find('hgroup').find_all('h5'):
                if h.find('a'):
                    company =  h.find('a').text
                    try:
                        pos['company'] = company.encode("ascii")
                    except:
                        pos['company'] = company
                    #print pos['company']
                    try:
                        cInfo = data_enrich.getComapnyInfo(pos['company'])
                        pos.update(cInfo)
                    except:
                        pos['company']
                else:
                    continue;

        ## parsing the job title
        job_title = son.find('h4').text
        try:
            pos['job_title'] = job_title.encode("ascii")
        except:
            pos['job_title'] = job_title
        ## Adding index
        pos['index'] = index
        index += 1

        ## Adding Global ID
        pos["ID"] = firstID
        firstID += 1

        ## Parsing place
        if son.find('span', {'class':'experience-date-locale'}).find('span', {'class':'locality'}):
            place =  son.find('span', {'class':'experience-date-locale'}).find('span', {'class':'locality'}).text
            try:
                pos['location'] = place.encode("ascii")
            except:
                pos['location'] = place

        ## Parsing time
        time_string = ""
        for t in son.find('span', {'class':'experience-date-locale'}).find_all('time'):
            time_string += t.text
            time_string += '&&'
        ##pos['time']=time_string ## if I want the exact date
        period_in_months = 0
        ##print time_string + "PPPP"
        try:
            period_string = time_string.split('(')[1].split(')')[0].encode("ascii")
            month_pattern = re.compile('(\d+) month')
            year_pattern = re.compile('(\d+) year')
            month_finder = month_pattern.search(period_string)
            year_finder = year_pattern.search(period_string)
            if(month_finder):
                period_in_months += int(month_finder.group(1))
            if(year_finder):
                period_in_months += int(year_finder.group(1))*12
        except:
            print "AAAAAAAAAAAA", time_string
        pos['period']=period_in_months
        cv.append(pos)
    print "The id now is ", firstID
    return cv, firstID


#cv, lastID = parseFile("/Users/yaelcohen/Documents/cvs/cvs_out/Iftach Bar   LinkedIn.html",0);
#print summery
##print " ______________________________________________"
#print cv
##print " ______________________________________________"
##print lastID
##print "Done!!!"