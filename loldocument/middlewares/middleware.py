from selenium import webdriver
from scrapy.http import HtmlResponse
import time

class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        print("PhantomJS is starting...")
        driver = webdriver.PhantomJS()  # 指定使用的浏览器
        # driver = webdriver.Firefox()
        driver.get(request.url)
        time.sleep(1)
        if 'PhantomJS' in request.meta :
            js = "var q=document.documentElement.scrollTop=1000"
            driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
            time.sleep(1)
            body = driver.page_source
            print("访问详情页" + request.url)
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        else:
            js = "var q=document.documentElement.scrollTop=1000"
            driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
            time.sleep(1)
            body = driver.page_source
            print("访问:" + request.url)
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)


    def process_exception(self, exception):
        print('''56555555555555555555555555''')