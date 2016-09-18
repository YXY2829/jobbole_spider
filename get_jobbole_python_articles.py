
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
import MySQLdb
from multiprocessing.dummy import Pool as ThreadPool
# from multiprocessing import Pool
import time

# sql='create table jobbole(title char(100),text_type char(20),time char(16),content text);'

def get_single_page_info(url):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='rootroot',db='mydb',charset='utf8')
    cursor=conn.cursor()
    start=time.time()
#     ua=UserAgent()
#     print ua.random
    dcap=dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.userAgent']='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
#     dcap['phantomjs.page.settings.userAgent']=ua.random
    driver=webdriver.PhantomJS(desired_capabilities=dcap)
#     driver=webdriver.PhantomJS()
    driver.get(url)
    titles=driver.find_elements_by_class_name('archive-title')
    types=driver.find_elements_by_xpath('//a[@rel="category tag"]')
    times=driver.find_elements_by_xpath('//*[@id="archive"]/div/div/p[1]')
    contents=driver.find_elements_by_class_name('excerpt')
    for t,y,i,c in zip(titles,types,times,contents):
#         print t.text,'-------',y.text,'-------',(re.search(r'\d{4}/\d{2}/\d{2}',i.text)).group()
        title=t.text
        text_type=y.text
        pub_time=(re.search(r'\d{4}/\d{2}/\d{2}',i.text)).group()
        content=c.text
        sql='insert into jobbole1(title,text_type,time,content) values("%s","%s","%s","%s");'%(title,text_type,pub_time,content)
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception,e:
            print e
        print title,'---',text_type,'---',pub_time,'++++++++++++'
    print url
    print time.time()-start
    driver.close()
    cursor.close()
    conn.close()

starttime=time.time()
urls=('http://python.jobbole.com/all-posts/page/%s'% i for i in range(1,51))
pool=ThreadPool(4)
pool.map(get_single_page_info, urls)
pool.close()
pool.join()
print time.time()-starttime
print '--------Over--------'
